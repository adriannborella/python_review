# blog/querysets.py - QuerySets optimizados
from django.db import models
from django.db.models import Count, Avg, Q, F, Prefetch
from django.utils import timezone

class OptimizedPostQuerySet(models.QuerySet):
    """QuerySet optimizado para Posts con técnicas avanzadas"""
    
    def published(self):
        """Posts publicados optimizado"""
        return self.filter(
            status='published',
            published_date__lte=timezone.now()
        ).select_related('author', 'category')
    
    def with_full_relations(self):
        """Carga todas las relaciones de una vez"""
        return self.select_related(
            'author', 
            'author__profile',
            'category'
        ).prefetch_related(
            'tags',
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(is_approved=True).select_related('author')
            )
        )
    
    def with_stats(self):
        """Añade estadísticas calculadas"""
        return self.annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True)),
            tag_count=Count('tags'),
            avg_rating=Avg('comments__rating', filter=Q(comments__is_approved=True)),
            total_words=Count('content')  # Aproximación
        )
    
    def popular(self, days=30):
        """Posts populares en los últimos N días"""
        date_threshold = timezone.now() - timezone.timedelta(days=days)
        return self.filter(
            published_date__gte=date_threshold
        ).order_by('-views_count', '-comment_count')
    
    def by_category_optimized(self, category_slug):
        """Posts por categoría con optimización"""
        return self.filter(
            category__slug=category_slug,
            category__is_active=True
        ).select_related('category')
    
    def search(self, query):
        """Búsqueda básica en título y contenido"""
        if not query:
            return self.none()
        
        return self.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    def featured_posts(self, limit=5):
        """Posts destacados con límite"""
        return self.filter(is_featured=True)[:limit]
    
    def recent_posts(self, days=7):
        """Posts recientes"""
        date_threshold = timezone.now() - timezone.timedelta(days=days)
        return self.filter(published_date__gte=date_threshold)
    
    def bulk_update_views(self, post_ids):
        """Actualización en lote de vistas (más eficiente)"""
        return self.filter(id__in=post_ids).update(
            views_count=F('views_count') + 1
        )

# blog/managers.py - Managers personalizados
from django.db import models

class CategoryManager(models.Manager):
    """Manager para categorías con métodos optimizados"""
    
    def get_queryset(self):
        return super().get_queryset().select_related()
    
    def active_with_posts(self):
        """Categorías activas que tienen posts"""
        return self.filter(
            is_active=True,
            posts__isnull=False
        ).annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0).distinct()
    
    def popular_categories(self, limit=10):
        """Categorías más populares por número de posts"""
        return self.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0).order_by('-post_count')[:limit]

class PostManager(models.Manager):
    """Manager principal para Posts"""
    
    def get_queryset(self):
        return OptimizedPostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def with_full_relations(self):
        return self.get_queryset().with_full_relations()
    
    def with_stats(self):
        return self.get_queryset().with_stats()
    
    def popular(self, days=30):
        return self.get_queryset().popular(days)
    
    def search(self, query):
        return self.get_queryset().search(query)

# blog/services.py - Servicios para lógica de negocio compleja
from django.db import transaction
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class BlogService:
    """Servicio para operaciones complejas del blog"""
    
    @staticmethod
    def get_popular_posts(limit=10, cache_timeout=300):
        """Obtiene posts populares con caché"""
        cache_key = f'popular_posts_{limit}'
        posts = cache.get(cache_key)
        
        if posts is None:
            posts = list(
                Post.objects.published()
                .with_stats()
                .order_by('-views_count', '-comment_count')[:limit]
            )
            cache.set(cache_key, posts, cache_timeout)
            logger.info(f'Popular posts cached: {len(posts)} posts')
        
        return posts
    
    @staticmethod
    def get_related_posts(post, limit=5):
        """Obtiene posts relacionados usando algoritmo de similitud"""
        cache_key = f'related_posts_{post.id}_{limit}'
        related_posts = cache.get(cache_key)
        
        if related_posts is None:
            # Algoritmo por tags compartidos
            tag_ids = list(post.tags.values_list('id', flat=True))
            
            if tag_ids:
                related_posts = list(
                    Post.objects.published()
                    .filter(tags__id__in=tag_ids)
                    .exclude(id=post.id)
                    .annotate(
                        shared_tags=Count('tags', filter=Q(tags__id__in=tag_ids))
                    )
                    .order_by('-shared_tags', '-published_date')
                    .distinct()[:limit]
                )
            else:
                # Fallback: posts de la misma categoría
                related_posts = list(
                    Post.objects.published()
                    .filter(category=post.category)
                    .exclude(id=post.id)
                    .order_by('-published_date')[:limit]
                )
            
            cache.set(cache_key, related_posts, 600)  # 10 minutos
            logger.info(f'Related posts cached for post {post.id}: {len(related_posts)} posts')
        
        return related_posts
    
    @staticmethod
    @transaction.atomic
    def publish_post(post, user):
        """Publica un post con validaciones"""
        if post.status != 'draft':
            raise ValueError("Only draft posts can be published")
        
        if not post.title or not post.content:
            raise ValueError("Title and content are required")
        
        post.status = 'published'
        post.published_date = timezone.now()
        post.save()
        
        # Invalidar cachés relacionados
        cache_keys = [
            'popular_posts_10',
            'recent_posts',
            f'category_posts_{post.category.slug}' if post.category else None,
        ]
        cache.delete_many([key for key in cache_keys if key])
        
        logger.info(f'Post published: {post.title} by {user.username}')
        return post
    
    @staticmethod
    def increment_post_views(post_id, user_ip=None):
        """Incrementa vistas de un post (con protección contra spam)"""
        cache_key = f'post_view_{post_id}_{user_ip}' if user_ip else f'post_view_{post_id}'
        
        # Protección: una vista por IP por hora
        if user_ip and cache.get(cache_key):
            return False
        
        # Incrementar contador
        Post.objects.filter(id=post_id).update(views_count=F('views_count') + 1)
        
        # Marcar IP como vista (1 hora)
        if user_ip:
            cache.set(cache_key, True, 3600)
        
        return True
    
    @staticmethod
    def get_blog_statistics():
        """Obtiene estadísticas generales del blog"""
        cache_key = 'blog_statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_posts': Post.objects.published().count(),
                'total_categories': Category.objects.filter(is_active=True).count(),
                'total_tags': Tag.objects.count(),
                'total_comments': Comment.objects.filter(is_approved=True).count(),
                'total_views': Post.objects.aggregate(
                    total=models.Sum('views_count')
                )['total'] or 0,
                'avg_reading_time': Post.objects.aggregate(
                    avg=models.Avg('reading_time')
                )['avg'] or 0,
            }
            cache.set(cache_key, stats, 1800)  # 30 minutos
        
        return stats

# blog/utils.py - Utilidades para el blog
import re
from django.utils.text import slugify
from django.utils.html import strip_tags

class BlogUtils:
    """Utilidades para el blog"""
    
    @staticmethod
    def generate_unique_slug(model_class, title, instance=None):
        """Genera un slug único para un modelo"""
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        
        while True:
            # Excluir la instancia actual si estamos editando
            queryset = model_class.objects.filter(slug=slug)
            if instance and instance.pk:
                queryset = queryset.exclude(pk=instance.pk)
            
            if not queryset.exists():
                break
            
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    @staticmethod
    def calculate_reading_time(content):
        """Calcula tiempo de lectura en minutos"""
        if not content:
            return 0
        
        # Remover HTML tags
        text = strip_tags(content)
        
        # Contar palabras
        words = len(re.findall(r'\b\w+\b', text))
        
        # Promedio de 200 palabras por minuto
        reading_time = max(1, round(words / 200))
        
        return reading_time
    
    @staticmethod
    def generate_excerpt(content, max_length=200):
        """Genera un excerpt del contenido"""
        if not content:
            return ""
        
        # Remover HTML tags
        text = strip_tags(content)
        
        # Truncar por palabras
        words = text.split()
        if len(words) <= max_length // 5:  # Aproximadamente 5 caracteres por palabra
            return text
        
        # Truncar y añadir "..."
        truncated = ' '.join(words[:max_length // 5])
        return f"{truncated}..."
    
    @staticmethod
    def extract_keywords(content, max_keywords=10):
        """Extrae palabras clave del contenido"""
        if not content:
            return []
        
        # Remover HTML y convertir a minúsculas
        text = strip_tags(content).lower()
        
        # Palabras comunes a filtrar (stop words básico)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
            'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'can', 'may', 'might', 'must'
        }
        
        # Extraer palabras
        words = re.findall(r'\b\w+\b', text)
        
        # Filtrar palabras cortas y stop words
        filtered_words = [
            word for word in words 
            if len(word) > 3 and word not in stop_words
        ]
        
        # Contar frecuencia
        from collections import Counter
        word_freq = Counter(filtered_words)
        
        # Retornar las más frecuentes
        return [word for word, count in word_freq.most_common(max_keywords)]

# Performance monitoring
class QueryCounter:
    """Utilidad para contar queries durante desarrollo"""
    
    def __init__(self):
        self.queries = 0
    
    def __enter__(self):
        from django.db import connection
        self.initial_queries = len(connection.queries)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        from django.db import connection
        self.queries = len(connection.queries) - self.initial_queries
        print(f"Executed {self.queries} database queries")

# Ejemplo de uso:
# with QueryCounter() as counter:
#     posts = list(Post.objects.published().with_full_relations()[:10])
# print(f"Posts loaded with {counter.queries} queries")