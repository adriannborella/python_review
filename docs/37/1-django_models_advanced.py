# core/models.py - Modelos base y abstracts
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import uuid

class TimeStampedModel(models.Model):
    """Modelo abstracto para timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDModel(models.Model):
    """Modelo abstracto con UUID como primary key"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    class Meta:
        abstract = True

class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet personalizado para soft delete"""
    
    def active(self):
        """Retorna solo registros activos (no eliminados)"""
        return self.filter(deleted_at__isnull=True)
    
    def deleted(self):
        """Retorna solo registros eliminados"""
        return self.filter(deleted_at__isnull=False)
    
    def delete(self):
        """Soft delete para querysets"""
        return self.update(deleted_at=timezone.now())

class SoftDeleteManager(models.Manager):
    """Manager personalizado para soft delete"""
    
    def get_queryset(self):
        """Retorna queryset con solo registros activos por defecto"""
        return SoftDeleteQuerySet(self.model, using=self._db).active()
    
    def all_with_deleted(self):
        """Retorna todos los registros incluyendo eliminados"""
        return SoftDeleteQuerySet(self.model, using=self._db)
    
    def deleted_only(self):
        """Retorna solo registros eliminados"""
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()

class SoftDeleteModel(models.Model):
    """Modelo abstracto con soft delete"""
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Manager para acceso a todos los registros
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete para instancias individuales"""
        self.deleted_at = timezone.now()
        self.save(using=using)
    
    def hard_delete(self, using=None, keep_parents=False):
        """Hard delete real"""
        super().delete(using=using, keep_parents=keep_parents)
    
    def restore(self):
        """Restaurar registro eliminado"""
        self.deleted_at = None
        self.save()
    
    @property
    def is_deleted(self):
        """Verifica si el registro está eliminado"""
        return self.deleted_at is not None

# users/models.py - Sistema de usuarios extendido
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
import os

def user_avatar_path(instance, filename):
    """Genera path para avatar de usuario"""
    ext = filename.split('.')[-1]
    filename = f"{instance.username}_avatar.{ext}"
    return os.path.join('avatars', str(instance.id), filename)

class User(AbstractUser):
    """Modelo de usuario personalizado"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Configuración de privacidad
    is_profile_public = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    
    # Campos adicionales
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Retorna nombre completo"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
    
    @property
    def display_name(self):
        """Nombre para mostrar públicamente"""
        return self.get_full_name() or self.username

class UserProfile(TimeStampedModel):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Información profesional
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    
    # Redes sociales
    github_username = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=50, blank=True)
    
    # Estadísticas
    profile_views = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"

# blog/models.py - Sistema de blog complejo
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinLengthValidator
from core.models import TimeStampedModel, SoftDeleteModel
import re

User = get_user_model()

class CategoryQuerySet(models.QuerySet):
    """QuerySet personalizado para categorías"""
    
    def active(self):
        return self.filter(is_active=True)
    
    def with_post_count(self):
        return self.annotate(post_count=models.Count('posts'))

class CategoryManager(models.Manager):
    """Manager personalizado para categorías"""
    
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def with_post_count(self):
        return self.get_queryset().with_post_count()

class Category(TimeStampedModel):
    """Categoría de blog posts"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#007bff")  # Hex color
    icon = models.CharField(max_length=50, blank=True)  # CSS class para icono
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    objects = CategoryManager()
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

class Tag(TimeStampedModel):
    """Tag para blog posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})

class PostQuerySet(models.QuerySet):
    """QuerySet personalizado para posts"""
    
    def published(self):
        return self.filter(status='published', published_date__lte=timezone.now())
    
    def draft(self):
        return self.filter(status='draft')
    
    def by_author(self, author):
        return self.filter(author=author)
    
    def by_category(self, category):
        return self.filter(category=category)
    
    def featured(self):
        return self.filter(is_featured=True)
    
    def with_related(self):
        return self.select_related('author', 'category').prefetch_related('tags')

class PostManager(models.Manager):
    """Manager personalizado para posts"""
    
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def with_related(self):
        return self.get_queryset().with_related()

class Post(TimeStampedModel, SoftDeleteModel):
    """Blog post con funcionalidades avanzadas"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]
    )
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Contenido
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/',
        blank=True,
        null=True
    )
    
    # Estado y fechas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Configuración
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Estadísticas
    views_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=0, help_text="Reading time in minutes")
    
    objects = PostManager()
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_date']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['category', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generar excerpt si está vacío
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + "..."
        
        # Calcular tiempo de lectura
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, word_count // 200)  # ~200 words per minute
        
        # Auto-publish si cambia a published
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return (
            self.status == 'published' and 
            self.published_date and 
            self.published_date <= timezone.now()
        )
    
    def get_next_post(self):
        """Obtiene el siguiente post publicado"""
        return Post.objects.published().filter(
            published_date__gt=self.published_date
        ).first()
    
    def get_previous_post(self):
        """Obtiene el post anterior publicado"""
        return Post.objects.published().filter(
            published_date__lt=self.published_date
        ).last()
    
    def get_related_posts(self, limit=5):
        """Obtiene posts relacionados por tags"""
        if not self.pk:
            return Post.objects.none()
        
        return Post.objects.published().filter(
            tags__in=self.tags.all()
        ).exclude(pk=self.pk).distinct()[:limit]

class Comment(TimeStampedModel, SoftDeleteModel):
    """Sistema de comentarios"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    content = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'is_approved', 'created_at']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    def get_replies(self):
        """Obtiene respuestas a este comentario"""
        return self.replies.filter(is_approved=True)

# Signals para mantener consistencia
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea perfil automáticamente al crear usuario"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda perfil cuando se guarda usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Comment)
def update_comment_count(sender, instance, created, **kwargs):
    """Actualiza contador de comentarios del post"""
    if created and instance.is_approved:
        # Aquí podrías actualizar un campo comments_count en Post si lo tuvieras
        pass

@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    """Disminuye contador de comentarios al eliminar"""
    pass