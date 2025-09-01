# blog/models.py - Modelos extendidos
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class UserProfile(models.Model):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    github = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Color hex
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """Sistema de etiquetas para posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='created_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.URLField(blank=True)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...' if len(self.content) > 300 else self.content
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'slug': self.slug})
    
    def increment_views(self):
        """Incrementa el contador de vistas"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

class PostLike(models.Model):
    """Sistema de likes para posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
    @property
    def is_reply(self):
        return self.parent is not None

# accounts/forms.py - Formularios de autenticación
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Crear perfil automáticamente
            UserProfile.objects.create(user=user)
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileExtendedForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'website', 'twitter', 'github']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'github': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario'}),
        }

# blog/forms.py - Formularios extendidos
from django import forms
from .models import Post, Comment, Tag

class AdvancedSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en título y contenido...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    author = forms.ModelChoiceField(
        queryset=User.objects.filter(posts__isnull=False).distinct(),
        required=False,
        empty_label="Todos los autores",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('created_at', 'Más recientes'),
            ('-created_at', 'Más antiguos'),
            ('-views_count', 'Más vistos'),
            ('-likes_count', 'Más gustados'),
            ('title', 'Alfabético'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PostFormExtended(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        required=False,
        help_text="Separar tags con comas (ej: python, django, web)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, web development'
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'status', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')
        if tags_string:
            tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
            if len(tag_names) > 10:
                raise forms.ValidationError("Máximo 10 tags permitidos")
            return tag_names
        return []
    
    def save(self, commit=True):
        instance = super().save(commit)
        
        if commit:
            # Procesar tags
            tag_names = self.cleaned_data.get('tags', [])
            if tag_names:
                tags = []
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=name.lower(),
                        defaults={'slug': slugify(name)}
                    )
                    tags.append(tag)
                instance.tags.set(tags)
        
        return instance

# blog/views.py - Views completas con todas las funcionalidades
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category, Comment, PostLike, Tag
from .forms import PostFormExtended, CommentForm, AdvancedSearchForm
from .search import PostSearchEngine

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published')\
            .select_related('author', 'category')\
            .prefetch_related('tags', 'likes')\
            .annotate(
                comment_count=Count('comments', filter=Q(comments__active=True)),
                like_count=Count('likes')
            ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_object(self):
        obj = get_object_or_404(
            Post.objects.select_related('author', 'category')
                       .prefetch_related('tags', 'comments__author'),
            pk=self.kwargs['pk'],
            status='published'
        )
        # Incrementar vistas solo si no es el autor
        if self.request.user != obj.author:
            obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Comentarios con replies anidados
        comments = self.object.comments.filter(active=True, parent=None)\
                              .select_related('author')\
                              .prefetch_related('replies__author')
        context['comments'] = comments
        
        # Formulario de comentarios
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        
        # Post relacionados
        related_posts = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(pk=self.object.pk)[:3]
        context['related_posts'] = related_posts
        
        # Verificar si el usuario le dio like
        if self.request.user.is_authenticated:
            context['user_liked'] = PostLike.objects.filter(
                user=self.request.user,
                post=self.object
            ).exists()
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostFormExtended
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '¡Post creado exitosamente!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PostPermissionMixin, UpdateView):
    model = Post
    form_class = PostFormExtended
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, '¡Post actualizado exitosamente!')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, PostPermissionMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '¡Post eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)

# VIEWS AJAX
@login_required
@require_POST
def ajax_add_comment(request, post_id):
    """Agregar comentario vía AJAX"""
    post = get_object_or_404(Post, pk=post_id, status='published')
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Manejar respuestas a comentarios
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id
            
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.get_full_name() or comment.author.username,
                    'created_at': comment.created_at.strftime('%d %b %Y, %H:%M'),
                    'is_reply': comment.is_reply
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
@require_POST
def ajax_toggle_like(request, post_id):
    """Toggle like de un post vía AJAX"""
    post = get_object_or_404(Post, pk=post_id)
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        like, created = PostLike.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        # Actualizar contador en el post
        post.likes_count = post.likes.count()
        post.save(update_fields=['likes_count'])
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def advanced_search_view(request):
    """Vista de búsqueda avanzada"""
    form = AdvancedSearchForm(request.GET or None)
    posts = Post.objects.none()
    search_performed = False
    
    if form.is_valid() and any(form.cleaned_data.values()):
        search_engine = PostSearchEngine()
        posts = search_engine.search(
            query=form.cleaned_data.get('query'),
            category=form.cleaned_data.get('category'),
            author=form.cleaned_data.get('author'),
            date_from=form.cleaned_data.get('date_from'),
            date_to=form.cleaned_data.get('date_to')
        )
        
        # Aplicar ordenamiento
        sort_by = form.cleaned_data.get('sort_by', '-created_at')
        posts = posts.order_by(sort_by)
        search_performed = True
    
    # Paginación
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'posts': posts,
        'search_performed': search_performed,
        'total_results': posts.paginator.count if search_performed else 0
    }
    return render(request, 'blog/advanced_search.html', context)

# blog/admin.py - Configuración del Admin
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Post, Category, Comment, Tag, PostLike, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'has_bio', 'has_social_links')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at',)
    
    def has_bio(self, obj):
        return bool(obj.bio)
    has_bio.boolean = True
    has_bio.short_description = 'Tiene bio'
    
    def has_social_links(self, obj):
        return bool(obj.twitter or obj.github or obj.website)
    has_social_links.boolean = True
    has_social_links.short_description = 'Enlaces sociales'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'color_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            post_count=Count('posts')
        )
    
    def post_count(self, obj):
        return obj.post_count
    post_count.admin_order_field = 'post_count'
    post_count.short_description = 'Posts'
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            post_count=Count('posts')
        )
    
    def post_count(self, obj):
        return obj.post_count
    post_count.admin_order_field = 'post_count'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at')
    fields = ('author', 'content', 'active', 'created_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'views_count', 'comment_count', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    inlines = [CommentInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Contenido', {
            'fields': ('content', 'excerpt', 'featured_image'),
            'classes': ('wide',)
        }),
        ('Clasificación', {
            'fields': ('tags', 'status'),
        }),
        ('Estadísticas', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')\
                                           .prefetch_related('tags')\
                                           .annotate(comment_count=Count('comments'))
    
    def comment_count(self, obj):
        return obj.comment_count
    comment_count.admin_order_field = 'comment_count'
    comment_count.short_description = 'Comentarios'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo post
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'author', 'post', 'active', 'created_at', 'is_reply')
    list_filter = ('active', 'created_at', 'post__category')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('post', 'parent')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Contenido'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Es respuesta'
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} comentarios marcados como activos.')
    mark_as_active.short_description = 'Marcar como activos'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} comentarios marcados como inactivos.')
    mark_as_inactive.short_description = 'Marcar como inactivos'

# Custom Admin Site
class BlogAdminSite(admin.AdminSite):
    site_header = 'Administración del Blog'
    site_title = 'Blog Admin'
    index_title = 'Panel de Control'
    
    def index(self, request, extra_context=None):
        """Dashboard personalizado"""
        extra_context = extra_context or {}
        
        # Estadísticas para el dashboard
        from datetime import timedelta
        from django.utils import timezone
        
        last_week = timezone.now() - timedelta(days=7)
        
        extra_context.update({
            'total_posts': Post.objects.filter(status='published').count(),
            'draft_posts': Post.objects.filter(status='draft').count(),
            'total_comments': Comment.objects.filter(active=True).count(),
            'pending_comments': Comment.objects.filter(active=False).count(),
            'posts_this_week': Post.objects.filter(created_at__gte=last_week).count(),
            'popular_posts': Post.objects.annotate(
                comment_count=Count('comments')
            ).order_by('-comment_count')[:5]
        })
        
        return super().index(request, extra_context)

# blog/signals.py - Señales para automatización
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import UserProfile, Post, Comment

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear perfil automáticamente cuando se crea un usuario"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar perfil cuando se actualiza el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver([post_save, post_delete], sender=Post)
def invalidate_blog_cache(sender, **kwargs):
    """Invalidar caché cuando se modifica un post"""
    cache_keys = [
        'popular_posts_5',
        'blog_stats',
        'recent_posts',
    ]
    cache.delete_many(cache_keys)

@receiver([post_save, post_delete], sender=Comment)
def update_comment_counts(sender, instance, **kwargs):
    """Actualizar contadores cuando se modifica un comentario"""
    if hasattr(instance, 'post'):
        post = instance.post
        # Actualizar contador de comentarios
        active_comments = post.comments.filter(active=True).count()
        # Aquí podrías actualizar un campo de contador si lo tienes
        
        # Invalidar caché relacionado
        cache.delete('blog_stats')

# blog/urls.py - URLs completas
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Posts principales
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_short'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Búsqueda
    path('search/', views.advanced_search_view, name='advanced_search'),
    
    # Filtros
    path('category/<int:category_id>/', views.PostListView.as_view(), name='posts_by_category'),
    path('author/<int:author_id>/', views.PostListView.as_view(), name='posts_by_author'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='posts_by_tag'),
    
    # AJAX endpoints
    path('ajax/comment/add/<int:post_id>/', views.ajax_add_comment, name='ajax_add_comment'),
    path('ajax/post/like/<int:post_id>/', views.ajax_toggle_like, name='ajax_toggle_like'),
]

# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]

# myproject/settings.py - Configuración completa
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'tu-secret-key-super-segura'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Para filtros humanizados
    
    # Apps locales
    'blog',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.BlogMiddleware',  # Nuestro middleware personalizado
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.blog_context',  # Context processor personalizado
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Caché configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutos por defecto
    }
}

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'blog:post_list'
LOGOUT_REDIRECT_URL = 'blog:post_list'

# Messages framework
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Email settings (para password reset)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Para desarrollo
# En producción:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'tu_password'

# Pagination
PAGINATE_BY = 6

# Security settings para producción
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True