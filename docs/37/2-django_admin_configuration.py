# users/admin.py - Admin para usuarios
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    """Inline para perfil de usuario"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
    fieldsets = (
        ('Professional Information', {
            'fields': ('job_title', 'company', 'experience_years')
        }),
        ('Social Networks', {
            'fields': ('github_username', 'linkedin_url', 'twitter_username'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('profile_views', 'followers_count', 'following_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para usuarios"""
    inlines = [UserProfileInline]
    
    # Campos mostrados en la lista
    list_display = [
        'email', 'username', 'get_full_name', 'is_active', 
        'is_staff', 'date_joined', 'last_activity', 'avatar_preview'
    ]
    list_display_links = ['email', 'username']
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'date_joined',
        'email_notifications', 'is_profile_public'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    # Campos editables en línea
    list_editable = ['is_active']
    
    # Filtros por fecha
    date_hierarchy = 'date_joined'
    
    # Acciones personalizadas
    actions = ['activate_users', 'deactivate_users', 'send_welcome_email']
    
    # Configuración de fieldsets
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio', 'website', 'location', 'birth_date')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Privacy Settings', {
            'fields': ('is_profile_public', 'email_notifications'),
        }),
        ('Localization', {
            'fields': ('timezone', 'language'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'last_activity'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def get_full_name(self, obj):
        """Muestra nombre completo en el admin"""
        return obj.get_full_name() or '-'
    get_full_name.short_description = 'Full Name'
    
    def avatar_preview(self, obj):
        """Muestra preview del avatar"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; border-radius: 50%;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = 'Avatar'
    
    # Acciones personalizadas
    def activate_users(self, request, queryset):
        """Activa usuarios seleccionados"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} users activated successfully.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        """Desactiva usuarios seleccionados"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} users deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def send_welcome_email(self, request, queryset):
        """Envía email de bienvenida"""
        # Aquí implementarías el envío de emails
        count = queryset.count()
        self.message_user(request, f'Welcome email sent to {count} users.')
    send_welcome_email.short_description = 'Send welcome email'

# blog/admin.py - Admin para blog
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin para categorías"""
    list_display = ['name', 'slug', 'color_display', 'post_count', 'is_active', 'order']
    list_display_links = ['name']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'is_active', 'order')
        }),
        ('Appearance', {
            'fields': ('color', 'icon'),
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Override queryset para incluir conteo de posts"""
        queryset = super().get_queryset(request)
        return queryset.annotate(post_count=Count('posts'))
    
    def post_count(self, obj):
        """Muestra cantidad de posts en la categoría"""
        count = getattr(obj, 'post_count', 0)
        if count > 0:
            url = reverse('admin:blog_post_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    post_count.short_description = 'Posts'
    post_count.admin_order_field = 'post_count'
    
    def color_display(self, obj):
        """Muestra color como preview"""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin para tags"""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(post_count=Count('posts'))
    
    def post_count(self, obj):
        count = getattr(obj, 'post_count', 0)
        if count > 0:
            url = reverse('admin:blog_post_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    post_count.short_description = 'Posts'
    post_count.admin_order_field = 'post_count'

class CommentInline(admin.TabularInline):
    """Inline para comentarios"""
    model = Comment
    extra = 0
    fields = ['author', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin para posts de blog"""
    inlines = [CommentInline]
    
    list_display = [
        'title', 'author', 'category', 'status', 'is_featured',
        'published_date', 'views_count', 'comment_count', 'reading_time'
    ]
    list_display_links = ['title']
    list_filter = [
        'status', 'is_featured', 'category', 'tags', 'author',
        'created_at', 'published_date', 'allow_comments'
    ]
    list_editable = ['status', 'is_featured']
    search_fields = ['title', 'content', 'author__username', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_date'
    ordering = ['-created_at']
    
    # Acciones personalizadas
    actions = ['publish_posts', 'unpublish_posts', 'feature_posts', 'unfeature_posts']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image'),
        }),
        ('Publication', {
            'fields': ('status', 'published_date', 'is_featured', 'allow_comments'),
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'reading_time'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Override queryset para optimizar consultas"""
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category').annotate(
            comment_count=Count('comments', filter=models.Q(comments__is_approved=True))
        )
    
    def comment_count(self, obj):
        """Muestra cantidad de comentarios aprobados"""
        count = getattr(obj, 'comment_count', 0)
        if count > 0:
            url = reverse('admin:blog_comment_changelist') + f'?post__id__exact={obj.id}'
            return format_html('<a href="{}">{} comments</a>', url, count)
        return '0 comments'
    comment_count.short_description = 'Comments'
    comment_count.admin_order_field = 'comment_count'
    
    def save_model(self, request, obj, form, change):
        """Override save para establecer autor automáticamente"""
        if not change:  # Solo en creación
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    # Acciones personalizadas
    def publish_posts(self, request, queryset):
        """Publica posts seleccionados"""
        from django.utils import timezone
        count = queryset.filter(status='draft').update(
            status='published',
            published_date=timezone.now()
        )
        self.message_user(request, f'{count} posts published successfully.')
    publish_posts.short_description = 'Publish selected posts'
    
    def unpublish_posts(self, request, queryset):
        """Despublica posts seleccionados"""
        count = queryset.filter(status='published').update(status='draft')
        self.message_user(request, f'{count} posts unpublished successfully.')
    unpublish_posts.short_description = 'Unpublish selected posts'
    
    def feature_posts(self, request, queryset):
        """Marca posts como destacados"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} posts marked as featured.')
    feature_posts.short_description = 'Mark as featured'
    
    def unfeature_posts(self, request, queryset):
        """Desmarca posts como destacados"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} posts unmarked as featured.')
    unfeature_posts.short_description = 'Unmark as featured'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin para comentarios"""
    list_display = [
        'post', 'author', 'content_preview', 'is_approved', 
        'is_reply', 'created_at'
    ]
    list_display_links = ['content_preview']
    list_filter = [
        'is_approved', 'created_at', 'post__category',
        'post__author', 'parent__isnull'
    ]
    list_editable = ['is_approved']
    search_fields = [
        'content', 'author__username', 'author__email', 'post__title'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # Acciones personalizadas
    actions = ['approve_comments', 'disapprove_comments']
    
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'parent', 'content', 'is_approved')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimiza consultas"""
        queryset = super().get_queryset(request)
        return queryset.select_related('post', 'author', 'parent')
    
    def content_preview(self, obj):
        """Muestra preview del contenido"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def is_reply(self, obj):
        """Indica si es una respuesta"""
        return obj.parent is not None
    is_reply.short_description = 'Reply'
    is_reply.boolean = True
    
    # Acciones personalizadas
    def approve_comments(self, request, queryset):
        """Aprueba comentarios seleccionados"""
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        """Desaprueba comentarios seleccionados"""
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} comments disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'

# Personalización del admin site
from django.contrib import admin

admin.site.site_header = "Interview Project Administration"
admin.site.site_title = "Interview Project Admin"
admin.site.index_title = "Welcome to Interview Project Administration"

# Personalización de templates del admin (opcional)
# admin/base_site.html
admin.site.enable_nav_sidebar = True