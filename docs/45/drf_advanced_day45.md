# Django Performance Optimization - Día 45

## 🎯 Objetivos del Día
- Dominar query optimization y database performance
- Implementar caching strategies efectivas
- Usar profiling tools para identificar bottlenecks
- Configurar Django Debug Toolbar y monitoring
- Prepararse para preguntas sobre escalabilidad

---

## 📚 HORA 1: TEORÍA DE PERFORMANCE

### 1. Database Query Optimization

#### N+1 Query Problem y Soluciones
```python
# ❌ PROBLEMA: N+1 Queries
def bad_post_list(request):
    posts = Post.objects.all()  # 1 query
    for post in posts:
        print(post.author.username)  # N queries adicionales!
        print(post.category.name)   # N queries más!

# ✅ SOLUCIÓN: select_related para ForeignKey
def optimized_post_list(request):
    posts = Post.objects.select_related('author', 'category').all()  # 1 query con JOINs
    for post in posts:
        print(post.author.username)  # No query adicional
        print(post.category.name)    # No query adicional

# ✅ SOLUCIÓN: prefetch_related para ManyToMany/Reverse ForeignKey
def posts_with_comments(request):
    posts = Post.objects.prefetch_related(
        'comments__author'  # Nested prefetch
    ).select_related('author', 'category')
    
    for post in posts:
        for comment in post.comments.all():  # No queries adicionales
            print(f"{comment.author.username}: {comment.content}")
```

#### Query Analysis y Optimization
```python
# Analyzing query performance
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def analyze_queries():
    # Reset query log
    connection.queries_log.clear()
    
    # Your code here
    posts = Post.objects.select_related('author').all()[:10]
    list(posts)  # Force evaluation
    
    # Analyze queries
    print(f"Number of queries: {len(connection.queries)}")
    for query in connection.queries:
        print(f"Time: {query['time']} - SQL: {query['sql'][:100]}...")

# Custom QuerySet for optimization
class PostQuerySet(models.QuerySet):
    def with_author_and_category(self):
        return self.select_related('author', 'category')
    
    def with_comments_count(self):
        return self.annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True))
        )
    
    def published(self):
        return self.filter(status='published')
    
    def for_api(self):
        """Optimized queryset for API responses"""
        return (self.with_author_and_category()
                   .with_comments_count()
                   .published()
                   .order_by('-created_at'))

class Post(models.Model):
    # ... fields ...
    objects = PostQuerySet.as_manager()
```

### 2. Caching Strategies

#### Django Cache Framework
```python
# settings.py - Redis Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Cache decorators and manual caching
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Function-based view caching
@cache_page(60 * 15)  # Cache for 15 minutes
def post_list(request):
    posts = Post.objects.for_api()
    return render(request, 'posts/list.html', {'posts': posts})

# Manual cache management
def get_popular_posts():
    cache_key = 'popular_posts_week'
    posts = cache.get(cache_key)
    
    if posts is None:
        # Expensive query
        posts = Post.objects.annotate(
            week_views=Count('views', filter=Q(views__created_at__gte=timezone.now() - timedelta(days=7)))
        ).order_by('-week_views')[:10]
        
        cache.set(cache_key, posts, timeout=60*60)  # Cache for 1 hour
    
    return posts

# Cache invalidation
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def invalidate_post_cache(sender, **kwargs):
    cache.delete_many([
        'popular_posts_week',
        'featured_posts',
        f'post_detail_{kwargs["instance"].slug}'
    ])
```

#### Template Fragment Caching
```python
# In templates
{% load cache %}

{% cache 500 post_sidebar post.id %}
    <!-- Expensive sidebar content -->
    <div class="sidebar">
        {% include "includes/related_posts.html" %}
        {% include "includes/popular_tags.html" %}
    </div>
{% endcache %}

# Conditional caching
{% cache 500 post_detail post.id post.updated_at %}
    <!-- Post content that changes when post is updated -->
{% endcache %}
```

### 3. Database Optimization

#### Database Indexes
```python
# models.py - Strategic indexing
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)  # Automatically indexed
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        # Composite indexes for common query patterns
        indexes = [
            models.Index(fields=['status', 'created_at']),  # For published posts by date
            models.Index(fields=['author', 'status']),      # For user's posts
            models.Index(fields=['category', 'featured']),  # For featured posts by category
        ]
        ordering = ['-created_at']

# Raw SQL for complex queries
from django.db import connection

def get_post_statistics():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.name as category_name,
                COUNT(*) as post_count,
                AVG(LENGTH(p.content)) as avg_content_length
            FROM blog_post p
            JOIN blog_category c ON p.category_id = c.id
            WHERE p.status = 'published'
            GROUP BY c.name
            ORDER BY post_count DESC
        """)
        return cursor.fetchall()
```

### 4. Memory Optimization

#### Lazy Loading y Iterators
```python
# For large datasets, use iterator()
def process_all_posts():
    # ❌ Loads all posts in memory
    for post in Post.objects.all():
        process_post(post)
    
    # ✅ Uses iterator to avoid memory issues
    for post in Post.objects.iterator(chunk_size=100):
        process_post(post)

# Lazy evaluation with only()
def get_post_titles():
    return Post.objects.only('title', 'slug').values_list('title', flat=True)

# Bulk operations for performance
def bulk_update_posts(post_data):
    posts_to_update = []
    for data in post_data:
        post = Post.objects.get(id=data['id'])
        post.title = data['title']
        posts_to_update.append(post)
    
    Post.objects.bulk_update(posts_to_update, ['title'], batch_size=100)
```

---

## ⚡ HORA 2: IMPLEMENTACIÓN Y PROFILING

### Proyecto: Performance Dashboard y Optimization

#### 1. Django Debug Toolbar Setup
```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]

# Debug toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'SHOW_COLLAPSED': True,
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = [
    '127.0.0.1',
]
```

#### 2. Custom Performance Monitoring
```python
# middleware.py
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('performance')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log slow requests
            if duration > 1.0:  # Slower than 1 second
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.2f}s"
                )
            
            # Add performance header
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response

# Performance decorator for views
from functools import wraps
import time

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        print(f"{func.__name__} executed in {duration:.3f}s")
        return result
    return wrapper
```

#### 3. Advanced Caching Implementation
```python
# cache_utils.py
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
import hashlib
import json

class CacheManager:
    @staticmethod
    def get_or_set_complex(cache_key, callable_func, timeout=300, version=None):
        """Advanced cache get/set with version support"""
        data = cache.get(cache_key, version=version)
        if data is None:
            data = callable_func()
            cache.set(cache_key, data, timeout=timeout, version=version)
        return data
    
    @staticmethod
    def cache_key_with_params(**params):
        """Generate consistent cache keys from parameters"""
        sorted_params = sorted(params.items())
        param_string = json.dumps(sorted_params, sort_keys=True)
        return hashlib.md5(param_string.encode()).hexdigest()

# Cached API responses
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def cached_post_stats(request):
    cache_key = CacheManager.cache_key_with_params(
        endpoint='post_stats',
        user_role=request.user.profile.role if request.user.is_authenticated else 'anonymous'
    )
    
    def get_stats():
        return {
            'total_posts': Post.objects.count(),
            'published_posts': Post.objects.filter(status='published').count(),
            'draft_posts': Post.objects.filter(status='draft').count(),
            'categories': Category.objects.count(),
        }
    
    stats = CacheManager.get_or_set_complex(cache_key, get_stats, timeout=600)
    return Response(stats)
```

#### 4. Query Optimization Patterns
```python
# optimization_patterns.py
from django.db.models import Prefetch, Count, Q, F

class OptimizedPostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category')
        
        # Conditional prefetching based on action
        if self.action == 'list':
            # For list view, only prefetch comment count
            queryset = queryset.annotate(
                comment_count=Count('comments', filter=Q(comments__is_approved=True))
            )
        elif self.action == 'retrieve':
            # For detail view, prefetch full comment tree
            approved_comments = Prefetch(
                'comments',
                queryset=Comment.objects.filter(is_approved=True)
                                       .select_related('author')
                                       .order_by('created_at')
            )
            queryset = queryset.prefetch_related(approved_comments)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Optimized trending posts calculation"""
        cache_key = 'trending_posts_24h'
        
        def calculate_trending():
            # Complex aggregation query
            return Post.objects.filter(
                status='published',
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).annotate(
                score=F('views_count') + Count('comments') * 2 + Count('likes') * 3
            ).order_by('-score')[:10]
        
        trending_posts = CacheManager.get_or_set_complex(
            cache_key, calculate_trending, timeout=3600
        )
        
        serializer = PostListSerializer(trending_posts, many=True, context={'request': request})
        return Response(serializer.data)

# Bulk operations optimization
def bulk_create_posts(posts_data):
    """Efficient bulk creation with validation"""
    posts_to_create = []
    
    for data in posts_data:
        post = Post(
            title=data['title'],
            content=data['content'],
            author_id=data['author_id'],
            category_id=data['category_id']
        )
        posts_to_create.append(post)
    
    # Bulk create in batches
    Post.objects.bulk_create(posts_to_create, batch_size=100)
```

### 2. Advanced Caching Patterns

#### Multi-Level Caching Strategy
```python
# caching_strategies.py
from django.core.cache import caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# Multiple cache backends
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'TIMEOUT': 86400,  # 24 hours
    },
    'long_term': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/3',
        'TIMEOUT': 86400 * 7,  # 1 week
    }
}

class SmartCacheManager:
    def __init__(self):
        self.default_cache = caches['default']
        self.long_term_cache = caches['long_term']
    
    def get_user_permissions(self, user_id):
        """Cache user permissions with smart invalidation"""
        cache_key = f'user_permissions_{user_id}'
        
        permissions = self.long_term_cache.get(cache_key)
        if permissions is None:
            user = User.objects.get(id=user_id)
            permissions = list(user.get_all_permissions())
            self.long_term_cache.set(cache_key, permissions, timeout=86400)
        
        return permissions
    
    def cache_expensive_calculation(self, func, *args, **kwargs):
        """Generic expensive calculation caching"""
        # Create cache key from function name and arguments
        cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
        
        result = self.default_cache.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            self.default_cache.set(cache_key, result, timeout=1800)  # 30 min
        
        return result

# Cache warming strategy
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Warm up critical caches'
    
    def handle(self, *args, **options):
        self.stdout.write("Starting cache warming...")
        
        # Warm popular content
        popular_posts = Post.objects.filter(
            status='published'
        ).order_by('-views_count')[:20]
        
        for post in popular_posts:
            cache_key = f'post_detail_{post.slug}'
            if not cache.get(cache_key):
                # Trigger cache population
                serializer = PostDetailSerializer(post)
                cache.set(cache_key, serializer.data, timeout=3600)
        
        self.stdout.write(self.style.SUCCESS('Cache warming completed'))
```

### 3. Database Connection Optimization

```python
# settings.py - Database optimization
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myapp_db',
        'USER': 'myapp_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,
        },
        'CONN_MAX_AGE': 60,  # Connection pooling
    }
}

# Database routing for read/write splitting
class DatabaseRouter:
    """Route reads and writes to different databases"""
    
    def db_for_read(self, model, **hints):
        """Suggest database to read from"""
        if model._meta.app_label == 'blog':
            return 'blog_read'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """Suggest database to write to"""
        if model._meta.app_label == 'blog':
            return 'blog_write'
        return 'default'
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure migrations go to correct database"""
        return True
```

---

## 🔧 HORA 2: PROFILING Y OPTIMIZATION PRÁCTICA

### 1. Django Debug Toolbar Integration
```python
# Analyzing performance with debug toolbar
# In your view, add comprehensive logging

import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger('performance')

class PerformanceAnalysisMixin:
    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG:
            queries_before = len(connection.queries)
            start_time = time.time()
        
        response = super().dispatch(request, *args, **kwargs)
        
        if settings.DEBUG:
            queries_after = len(connection.queries)
            end_time = time.time()
            
            logger.info(
                f"View: {self.__class__.__name__} | "
                f"Queries: {queries_after - queries_before} | "
                f"Time: {end_time - start_time:.3f}s"
            )
        
        return response
```

### 2. Custom Performance Metrics
```python
# performance_metrics.py
from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
import time
import statistics

class APIPerformanceTester:
    def __init__(self):
        self.client = Client()
        self.user = User.objects.first()
    
    def test_endpoint_performance(self, endpoint, iterations=10):
        """Test API endpoint performance"""
        times = []
        
        for i in range(iterations):
            start = time.time()
            response = self.client.get(endpoint)
            end = time.time()
            
            if response.status_code == 200:
                times.append(end - start)
        
        if times:
            return {
                'endpoint': endpoint,
                'avg_time': statistics.mean(times),
                'median_time': statistics.median(times),
                'max_time': max(times),
                'min_time': min(times),
                'iterations': len(times)
            }
        return None
    
    def run_performance_suite(self):
        """Run complete performance test suite"""
        endpoints = [
            '/api/v1/posts/',
            '/api/v1/posts/1/',
            '/api/v1/comments/?post_id=1',
        ]
        
        results = []
        for endpoint in endpoints:
            result = self.test_endpoint_performance(endpoint)
            if result:
                results.append(result)
        
        return results

# Command to run performance tests
class Command(BaseCommand):
    help = 'Run API performance tests'
    
    def handle(self, *args, **options):
        tester = APIPerformanceTester()
        results = tester.run_performance_suite()
        
        for result in results:
            self.stdout.write(
                f"Endpoint: {result['endpoint']}\n"
                f"  Avg: {result['avg_time']:.3f}s\n"
                f"  Median: {result['median_time']:.3f}s\n"
                f"  Range: {result['min_time']:.3f}s - {result['max_time']:.3f}s\n"
            )
```

### 3. Production-Ready Optimization
```python
# optimized_views.py
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page

@method_decorator(vary_on_headers('Authorization'), name='dispatch')
@method_decorator(cache_page(60 * 5), name='list')  # 5 min cache for list
class OptimizedPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Aggressive optimization for list view
        if self.action == 'list':
            return Post.objects.select_related('author', 'category')\
                              .annotate(comment_count=Count('comments'))\
                              .filter(status='published')\
                              .order_by('-created_at')
        
        # Full optimization for detail view
        return Post.objects.select_related('author', 'category')\
                          .prefetch_related(
                              Prefetch('comments', 
                                     queryset=Comment.objects.select_related('author')
                                                           .filter(is_approved=True))
                          )
    
    def list(self, request, *args, **kwargs):
        # Custom pagination for performance
        page_size = min(int(request.GET.get('page_size', 20)), 100)
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# Background task optimization
from celery import shared_task

@shared_task
def update_post_stats():
    """Background task to update post statistics"""
    posts = Post.objects.filter(status='published')
    
    for post in posts.iterator(chunk_size=100):
        # Update view counts, engagement metrics, etc.
        post.engagement_score = calculate_engagement_score(post)
        
    # Bulk update
    Post.objects.bulk_update(posts, ['engagement_score'], batch_size=100)
```

---

## 📊 EJERCICIOS DE PROFILING

### Ejercicio 1: Identificar N+1 Queries
```python
# Create a view that deliberately has N+1 problem
# Then optimize it step by step
def problematic_view(request):
    posts = Post.objects.all()[:10]
    data = []
    for post in posts:
        data.append({
            'title': post.title,
            'author': post.author.username,  # N+1 here
            'category': post.category.name,  # N+1 here
            'comment_count': post.comments.count()  # N+1 here
        })
    return JsonResponse({'posts': data})

# Your task: Optimize to use only 1 query
```

### Ejercicio 2: Cache Strategy Implementation
```python
# Implement caching for this expensive operation
def get_user_dashboard_data(user):
    """This function is called frequently and is expensive"""
    return {
        'recent_posts': user.post_set.all()[:5],
        'total_views': sum(post.views_count for post in user.post_set.all()),
        'follower_count': user.followers.count(),
        'engagement_rate': calculate_engagement_rate(user),
    }

# Your task: Add appropriate caching with invalidation
```

### Ejercicio 3: Memory Usage Optimization
```python
# Optimize this memory-heavy operation
def export_all_posts_to_csv():
    posts = Post.objects.all()  # Could be millions of records
    
    csv_data = []
    for post in posts:
        csv_data.append([
            post.title,
            post.author.username,
            post.created_at.strftime('%Y-%m-%d'),
            len(post.content)
        ])
    
    return csv_data

# Your task: Make this memory-efficient for large datasets
```

---

## 🏆 CHECKPOINTS DE PERFORMANCE

### Métricas Objetivo:
- [ ] **API Response Time**: < 200ms para endpoints principales
- [ ] **Query Count**: < 5 queries por request típico
- [ ] **Memory Usage**: < 50MB para operations normales
- [ ] **Cache Hit Rate**: > 80% para content estático
- [ ] **Database Connection Pool**: Efficiently managed

### Tools Mastery:
- [ ] Django Debug Toolbar configurado y usado efectivamente
- [ ] Query analysis con `connection.queries`
- [ ] Memory profiling con `memory_profiler`
- [ ] Cache monitoring con Redis CLI
- [ ] Database query EXPLAIN plans

---

## 🎯 PREGUNTAS DE ENTREVISTA - PERFORMANCE

### 1. Database Performance
**P:** "Tu API está lenta. ¿Cómo identificarías y solucionarías el problema?"

**R:** Proceso sistemático:
1. **Identify**: Django Debug Toolbar para ver queries
2. **Analyze**: Buscar N+1 queries y queries lentas
3. **Optimize**: select_related/prefetch_related appropriados
4. **Index**: Agregar indexes para common filters
5. **Cache**: Implementar caching strategy
6. **Monitor**: Setup continuous monitoring

### 2. Caching Strategy
**P:** "¿Cuándo usarías cada tipo de cache en Django?"

**R:** 
- **Per-site cache**: Contenido completamente estático
- **Per-view cache**: Views que no cambian frecuentemente
- **Template fragment cache**: Partes específicas expensive de templates
- **Low-level cache API**: Control granular, invalidation compleja
- **Database query cache**: Results de queries expensive

### 3. Scaling Challenges
**P:** "Tu aplicación Django necesita manejar 10x más tráfico. ¿Qué harías?"

**R:**
1. **Database**: Read replicas, connection pooling, query optimization
2. **Caching**: Redis cluster, CDN para static files
3. **Application**: Load balancers, horizontal scaling
4. **Code**: Async views, background tasks con Celery
5. **Monitoring**: Metrics, alerting, performance tracking

---

## 📈 PROYECTO DEL DÍA: Performance Dashboard

### Implementar un dashboard que muestre:
1. **Real-time metrics**: Response times, query counts
2. **Cache statistics**: Hit rates, memory usage
3. **Database health**: Connection pool status, slow queries
4. **Application metrics**: Active users, error rates

### Entregables:
- Dashboard funcional con métricas en tiempo real
- Performance baseline establecido
- Optimization recommendations documented
- Cache strategy implementada y tested

---

## 🚀 PREPARACIÓN PARA DÍA 46

**Mañana cubriremos:**
- Monitoring y Logging avanzado
- Sentry integration para error tracking
- Security best practices
- Production deployment strategies

### Pre-study:
- Revisa Django logging configuration
- Familiarízate con Sentry documentation
- Estudia Django security checklist

---

## 💡 TIPS PARA SUCCESS

1. **Profile First**: Nunca optimices sin medir primero
2. **Cache Wisely**: No todo necesita cache, choose strategically
3. **Database First**: 80% de performance issues son database-related
4. **Monitor Always**: Setup monitoring desde day 1, no después
5. **Test Performance**: Include performance tests en tu CI/CD

¡Excelente progreso! El performance optimization es lo que separa developers junior de senior. ¡Sigue así! 🔥