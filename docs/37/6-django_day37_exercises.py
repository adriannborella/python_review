# EJERCICIOS PRÁCTICOS - DÍA 37
# Completar estos ejercicios para consolidar el conocimiento

# EJERCICIO 1: Implementar un sistema de rating para posts
# Crear modelo Rating y agregarlo al sistema existente

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Rating(models.Model):
    """Sistema de calificaciones para posts"""
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['post', 'user']  # Un usuario solo puede calificar una vez
        indexes = [
            models.Index(fields=['post', 'score']),
        ]
    
    def __str__(self):
        return f'{self.user.username} rated {self.post.title}: {self.score}/5'

# Agregar al modelo Post:
    # average_rating = models.FloatField(default=0.0)
    # ratings_count = models.PositiveIntegerField(default=0)

# EJERCICIO 2: Implementar queries de optimización avanzada
class AdvancedBlogQueries:
    """Clase con queries optimizados para entrevistas"""
    
    @staticmethod
    def get_top_authors_by_posts(limit=10):
        """Obtiene autores con más posts publicados"""
        return User.objects.annotate(
            published_posts_count=Count(
                'posts', 
                filter=Q(posts__status='published')
            )
        ).filter(
            published_posts_count__gt=0
        ).order_by('-published_posts_count')[:limit]
    
    @staticmethod
    def get_posts_with_engagement_metrics():
        """Posts con métricas de engagement calculadas"""
        return Post.objects.published().annotate(
            total_comments=Count('comments', filter=Q(comments__is_approved=True)),
            total_ratings=Count('ratings'),
            avg_rating=Avg('ratings__score'),
            engagement_score=F('views_count') + F('total_comments') * 2 + F('total_ratings') * 3
        ).order_by('-engagement_score')
    
    @staticmethod
    def get_trending_tags(days=30):
        """Tags trending en los últimos N días"""
        date_threshold = timezone.now() - timezone.timedelta(days=days)
        
        return Tag.objects.annotate(
            recent_posts_count=Count(
                'posts',
                filter=Q(
                    posts__status='published',
                    posts__published_date__gte=date_threshold
                )
            )
        ).filter(
            recent_posts_count__gt=0
        ).order_by('-recent_posts_count')
    
    @staticmethod
    def get_user_reading_stats(user):
        """Estadísticas de lectura de un usuario"""
        from django.db.models import Sum
        
        return {
            'posts_read': user.post_views.count(),
            'total_reading_time': user.post_views.aggregate(
                total=Sum('post__reading_time')
            )['total'] or 0,
            'favorite_categories': user.post_views.values(
                'post__category__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:5],
            'comments_posted': user.comments.filter(is_approved=True).count(),
            'avg_rating_given': user.ratings.aggregate(
                avg=Avg('score')
            )['avg'] or 0,
        }

# EJERCICIO 3: Implementar sistema de follow/unfollow entre usuarios
class UserFollow(models.Model):
    """Sistema de seguimiento entre usuarios"""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower', 'created_at']),
            models.Index(fields=['following', 'created_at']),
        ]
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

# Agregar métodos al modelo User:
def get_followers_count(self):
    """Cuenta de seguidores"""
    return self.followers.count()

def get_following_count(self):
    """Cuenta de usuarios seguidos"""
    return self.following.count()

def is_following(self, user):
    """Verifica si sigue a un usuario"""
    return self.following.filter(following=user).exists()

def follow(self, user):
    """Seguir a un usuario"""
    if user != self and not self.is_following(user):
        UserFollow.objects.create(follower=self, following=user)
        return True
    return False

def unfollow(self, user):
    """Dejar de seguir a un usuario"""
    return self.following.filter(following=user).delete()[0] > 0

# EJERCICIO 4: Implementar sistema de bookmarks/favoritos
class Bookmark(models.Model):
    """Sistema de bookmarks para posts"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this bookmark")
    
    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} bookmarked {self.post.title}'

# EJERCICIO 5: Query para dashboard analytics
class DashboardAnalytics:
    """Queries para dashboard de analytics"""
    
    @staticmethod
    def get_blog_overview():
        """Overview general del blog"""
    @staticmethod
    def get_blog_overview():
        """Overview general del blog"""
        today = timezone.now().date()
        last_month = today - timezone.timedelta(days=30)
        
        return {
            'total_posts': Post.objects.published().count(),
            'total_users': User.objects.filter(is_active=True).count(),
            'total_comments': Comment.objects.filter(is_approved=True).count(),
            'total_categories': Category.objects.filter(is_active=True).count(),
            'posts_this_month': Post.objects.filter(
                status='published',
                published_date__date__gte=last_month
            ).count(),
            'new_users_this_month': User.objects.filter(
                date_joined__date__gte=last_month
            ).count(),
            'total_views': Post.objects.aggregate(
                total=models.Sum('views_count')
            )['total'] or 0,
        }
    
    @staticmethod
    def get_popular_posts_this_month(limit=10):
        """Posts más populares del mes"""
        last_month = timezone.now().date() - timezone.timedelta(days=30)
        
        return Post.objects.filter(
            status='published',
            published_date__date__gte=last_month
        ).annotate(
            engagement=F('views_count') + Count('comments') * 2
        ).order_by('-engagement')[:limit]
    
    @staticmethod
    def get_category_distribution():
        """Distribución de posts por categoría"""
        return Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(posts_count__gt=0).values('name', 'posts_count')
    
    @staticmethod
    def get_engagement_trends(days=30):
        """Tendencias de engagement"""
        from django.db.models.functions import TruncDate
        
        date_threshold = timezone.now() - timezone.timedelta(days=days)
        
        return Comment.objects.filter(
            created_at__gte=date_threshold,
            is_approved=True
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            comments_count=Count('id')
        ).order_by('date')

# EJERCICIO 6: Implementar cache invalidation
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class CacheManager:
    """Manager para invalidación de cache"""
    
    CACHE_KEYS = {
        'popular_posts': 'popular_posts_{limit}',
        'recent_posts': 'recent_posts_{limit}',
        'category_posts': 'category_posts_{slug}_{limit}',
        'blog_stats': 'blog_statistics',
        'trending_tags': 'trending_tags_{days}',
    }
    
    @classmethod
    def invalidate_post_caches(cls, post=None):
        """Invalida caches relacionados con posts"""
        keys_to_delete = [
            'popular_posts_*',
            'recent_posts_*',
            'blog_statistics',
            'trending_tags_*',
        ]
        
        if post and post.category:
            keys_to_delete.append(f'category_posts_{post.category.slug}_*')
        
        # En producción usarías cache.delete_pattern() con Redis
        # Aquí simulamos eliminando claves conocidas
        for pattern in keys_to_delete:
            for limit in [5, 10, 15, 20]:
                if '*' in pattern:
                    key = pattern.replace('*', str(limit))
                else:
                    key = pattern
                cache.delete(key)

# Signals para invalidar cache automáticamente
@receiver(post_save, sender=Post)
def invalidate_cache_on_post_save(sender, instance, **kwargs):
    """Invalida cache cuando se guarda un post"""
    CacheManager.invalidate_post_caches(instance)

@receiver(post_delete, sender=Post)
def invalidate_cache_on_post_delete(sender, instance, **kwargs):
    """Invalida cache cuando se elimina un post"""
    CacheManager.invalidate_post_caches(instance)

# EJERCICIO 7: Custom field para SEO
class SEOField(models.TextField):
    """Campo personalizado para contenido SEO"""
    
    def __init__(self, max_length=160, *args, **kwargs):
        self.max_length = max_length
        super().__init__(*args, **kwargs)
    
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        
        if value and len(value) > self.max_length:
            raise ValidationError(
                f'SEO content cannot exceed {self.max_length} characters. '
                f'Current length: {len(value)}'
            )

class SEOMixin(models.Model):
    """Mixin para campos SEO comunes"""
    meta_title = SEOField(max_length=60, blank=True, help_text="60 characters max")
    meta_description = SEOField(max_length=160, blank=True, help_text="160 characters max")
    meta_keywords = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(blank=True)
    robots_meta = models.CharField(
        max_length=50,
        choices=[
            ('index,follow', 'Index, Follow'),
            ('noindex,follow', 'No Index, Follow'),
            ('index,nofollow', 'Index, No Follow'),
            ('noindex,nofollow', 'No Index, No Follow'),
        ],
        default='index,follow'
    )
    
    class Meta:
        abstract = True
    
    def get_meta_title(self):
        """Retorna meta title o title por defecto"""
        return self.meta_title or getattr(self, 'title', '')
    
    def get_meta_description(self):
        """Retorna meta description o excerpt por defecto"""
        return self.meta_description or getattr(self, 'excerpt', '')[:160]

# EJERCICIO 8: Modelo para Analytics y Tracking
class PostView(models.Model):
    """Tracking de vistas de posts"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_views'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='post_views'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Campos calculados para analytics
    country = models.CharField(max_length=2, blank=True)  # ISO country code
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
        ],
        blank=True
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
    
    def __str__(self):
        user_info = self.user.username if self.user else self.ip_address
        return f'{user_info} viewed {self.post.title}'

# EJERCICIO 9: Implementar audit trail
class AuditLog(models.Model):
    """Log de auditoría para cambios en modelos"""
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    action = models.CharField(
        max_length=20,
        choices=[
            ('CREATE', 'Create'),
            ('UPDATE', 'Update'),
            ('DELETE', 'Delete'),
        ]
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Campos de cambio
    field_name = models.CharField(max_length=100, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    
    # Metadatos
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]

# EJERCICIO 10: Queries para reportes avanzados
class BlogReports:
    """Queries para reportes avanzados"""
    
    @staticmethod
    def get_author_performance_report():
        """Reporte de performance por autor"""
        return User.objects.annotate(
            total_posts=Count('posts'),
            published_posts=Count('posts', filter=Q(posts__status='published')),
            total_views=Sum('posts__views_count'),
            total_comments=Count('posts__comments', filter=Q(posts__comments__is_approved=True)),
            avg_reading_time=Avg('posts__reading_time'),
            last_post_date=Max('posts__published_date')
        ).filter(
            total_posts__gt=0
        ).order_by('-published_posts')
    
    @staticmethod
    def get_content_performance_by_month():
        """Performance del contenido por mes"""
        from django.db.models.functions import TruncMonth
        
        return Post.objects.filter(
            status='published'
        ).annotate(
            month=TruncMonth('published_date')
        ).values('month').annotate(
            posts_count=Count('id'),
            total_views=Sum('views_count'),
            total_comments=Count('comments', filter=Q(comments__is_approved=True)),
            avg_reading_time=Avg('reading_time')
        ).order_by('month')
    
    @staticmethod
    def get_engagement_by_category():
        """Análisis de engagement por categoría"""
        return Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published')),
            total_views=Sum('posts__views_count'),
            total_comments=Count('posts__comments', filter=Q(posts__comments__is_approved=True)),
            avg_engagement=Avg(
                F('posts__views_count') + Count('posts__comments') * 2
            )
        ).filter(posts_count__gt=0).order_by('-avg_engagement')
    
    @staticmethod
    def get_user_engagement_segmentation():
        """Segmentación de usuarios por engagement"""
        return User.objects.annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True)),
            bookmarks_count=Count('bookmarks'),
            posts_read=Count('post_views'),
            engagement_score=(
                F('comments_count') * 3 +
                F('bookmarks_count') * 2 +
                F('posts_read')
            )
        ).filter(engagement_score__gt=0).order_by('-engagement_score')

# COMANDOS PARA EJECUTAR LOS EJERCICIOS

"""
1. Crear las migrations:
python manage.py makemigrations

2. Aplicar migrations:
python manage.py migrate

3. Poblar con datos de prueba:
python manage.py shell
>>> from blog.models import *
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> # Crear datos de prueba usando los factories

4. Probar queries de optimización:
>>> from blog.exercises import AdvancedBlogQueries
>>> AdvancedBlogQueries.get_top_authors_by_posts()

5. Ejecutar tests:
python manage.py test blog.tests.test_models

6. Verificar performance:
>>> from django.db import connection
>>> connection.queries  # Ver queries ejecutadas
"""