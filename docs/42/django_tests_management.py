class PostViewTest(TestCase):
    """Tests para las views de Post"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_post_list_view(self):
        """Test vista de lista de posts"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.user.username)
    
    def test_post_detail_view(self):
        """Test vista detalle de post"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
    
    def test_post_detail_increments_views(self):
        """Test que la vista detalle incrementa las vistas"""
        initial_views = self.post.views_count
        
        # Visita como usuario diferente (no el autor)
        other_user = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)
    
    def test_post_create_requires_login(self):
        """Test que crear post requiere autenticación"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
    
    def test_post_create_authenticated(self):
        """Test crear post autenticado"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'content': 'New content',
            'category': self.category.pk,
            'status': 'published'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect después de crear
        self.assertTrue(Post.objects.filter(title='New Post').exists())
    
    def test_post_edit_authorization(self):
        """Test que solo el autor puede editar"""
        other_user = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        
        response = self.client.get(reverse('blog:post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect por falta de permisos

class CommentTest(TestCase):
    """Tests para comentarios"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_comment_creation(self):
        """Test creación de comentario"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertTrue(comment.active)
    
    def test_nested_comments(self):
        """Test comentarios anidados (replies)"""
        parent_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Parent comment'
        )
        
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Reply comment',
            parent=parent_comment
        )
        
        self.assertEqual(reply.parent, parent_comment)
        self.assertTrue(reply.is_reply)
        self.assertFalse(parent_comment.is_reply)

class FormTest(TestCase):
    """Tests para formularios"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Test', slug='test')
    
    def test_post_form_valid(self):
        """Test formulario de post válido"""
        form_data = {
            'title': 'Test Post Title',
            'content': 'A' * 150,  # Contenido suficiente para publicación
            'category': self.category.pk,
            'status': 'published',
            'tags': 'python, django, web'
        }
        
        form = PostFormExtended(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_post_form_invalid_short_content(self):
        """Test formulario inválido por contenido corto"""
        form_data = {
            'title': 'Test Post',
            'content': 'Short content',  # Muy corto para publicación
            'category': self.category.pk,
            'status': 'published'
        }
        
        form = PostFormExtended(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_comment_form_validation(self):
        """Test validación de formulario de comentario"""
        # Comentario muy corto
        form = CommentForm(data={'content': 'Corto'})
        self.assertFalse(form.is_valid())
        
        # Comentario válido
        form = CommentForm(data={'content': 'Este es un comentario válido con suficiente contenido'})
        self.assertTrue(form.is_valid())

class AjaxViewTest(TestCase):
    """Tests para views AJAX"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.client.login(username='testuser', password='pass')
    
    def test_ajax_add_comment(self):
        """Test agregar comentario vía AJAX"""
        response = self.client.post(
            reverse('blog:ajax_add_comment', kwargs={'post_id': self.post.pk}),
            {'content': 'Test comment via AJAX'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(Comment.objects.filter(content='Test comment via AJAX').exists())
    
    def test_ajax_toggle_like(self):
        """Test toggle like vía AJAX"""
        response = self.client.post(
            reverse('blog:ajax_toggle_like', kwargs={'post_id': self.post.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)

# blog/management/commands/cleanup_blog.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from blog.models import Post, Comment

class Command(BaseCommand):
    help = 'Limpia datos antiguos y optimiza la base de datos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Días para considerar contenido como antiguo'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar sin hacer cambios reales'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Encontrar posts antiguos en borrador
        old_drafts = Post.objects.filter(
            status='draft',
            created_at__lt=cutoff_date
        )
        
        # Encontrar comentarios inactivos antiguos
        old_inactive_comments = Comment.objects.filter(
            active=False,
            created_at__lt=cutoff_date
        )
        
        if dry_run:
            self.stdout.write(f'DRY RUN - Se eliminarían:')
            self.stdout.write(f'- {old_drafts.count()} borradores antiguos')
            self.stdout.write(f'- {old_inactive_comments.count()} comentarios inactivos')
        else:
            # Ejecutar limpieza
            drafts_deleted = old_drafts.count()
            old_drafts.delete()
            
            comments_deleted = old_inactive_comments.count()
            old_inactive_comments.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Limpieza completada:\n'
                    f'- {drafts_deleted} borradores eliminados\n'
                    f'- {comments_deleted} comentarios inactivos eliminados'
                )
            )

# blog/management/commands/import_posts.py
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Post, Category

class Command(BaseCommand):
    help = 'Importa posts desde un archivo CSV'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV')
        parser.add_argument('--author', type=str, help='Username del autor por defecto')
        parser.add_argument('--status', type=str, default='draft', help='Estado por defecto')
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        author_username = options['author']
        default_status = options['status']
        
        # Obtener autor por defecto
        if author_username:
            try:
                default_author = User.objects.get(username=author_username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuario {author_username} no encontrado'))
                return
        else:
            default_author = User.objects.first()
            if not default_author:
                self.stdout.write(self.style.ERROR('No hay usuarios en el sistema'))
                return
        
        imported_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        title = row.get('title', '').strip()
                        content = row.get('content', '').strip()
                        category_name = row.get('category', 'General').strip()
                        
                        if not title or not content:
                            self.stdout.write(f'Saltando fila sin título o contenido')
                            skipped_count += 1
                            continue
                        
                        # Obtener o crear categoría
                        category, created = Category.objects.get_or_create(
                            name=category_name,
                            defaults={'slug': slugify(category_name)}
                        )
                        
                        # Crear post si no existe
                        post, created = Post.objects.get_or_create(
                            title=title,
                            defaults={
                                'content': content,
                                'author': default_author,
                                'category': category,
                                'status': default_status,
                                'slug': slugify(title)
                            }
                        )
                        
                        if created:
                            imported_count += 1
                            self.stdout.write(f'Importado: {title}')
                        else:
                            skipped_count += 1
                            self.stdout.write(f'Ya existe: {title}')
                    
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error procesando fila: {e}'))
                        skipped_count += 1
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Archivo {csv_file} no encontrado'))
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Importación completada:\n'
                f'- {imported_count} posts importados\n'
                f'- {skipped_count} posts saltados'
            )
        )

# blog/management/commands/generate_sitemap.py
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings
from blog.models import Post
import os

class Command(BaseCommand):
    help = 'Genera un sitemap XML para SEO'
    
    def handle(self, *args, **options):
        posts = Post.objects.filter(status='published').order_by('-updated_at')
        
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://myblog.com/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
'''
        
        for post in posts:
            sitemap_content += f'''    <url>
        <loc>https://myblog.com{post.get_absolute_url()}</loc>
        <lastmod>{post.updated_at.strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
        
        sitemap_content += '</urlset>'
        
        # Guardar sitemap
        sitemap_path = os.path.join(settings.BASE_DIR, 'static', 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        self.stdout.write(
            self.style.SUCCESS(f'Sitemap generado con {posts.count()} posts')
        )

# blog/management/commands/blog_stats.py
from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from blog.models import Post, Comment, Category

class Command(BaseCommand):
    help = 'Muestra estadísticas del blog'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--period',
            type=str,
            default='month',
            choices=['week', 'month', 'year'],
            help='Período para las estadísticas'
        )
    
    def handle(self, *args, **options):
        period = options['period']
        
        # Calcular fechas
        now = datetime.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
            period_name = 'última semana'
        elif period == 'month':
            start_date = now - timedelta(days=30)
            period_name = 'último mes'
        else:  # year
            start_date = now - timedelta(days=365)
            period_name = 'último año'
        
        # Estadísticas generales
        total_posts = Post.objects.filter(status='published').count()
        total_users = User.objects.count()
        total_comments = Comment.objects.filter(active=True).count()
        total_categories = Category.objects.count()
        
        # Estadísticas del período
        period_posts = Post.objects.filter(
            status='published',
            created_at__gte=start_date
        ).count()
        
        period_comments = Comment.objects.filter(
            created_at__gte=start_date
        ).count()
        
        # Top autores
        top_authors = User.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        ).filter(post_count__gt=0).order_by('-post_count')[:5]
        
        # Top categorías
        top_categories = Category.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        ).order_by('-post_count')[:5]
        
        # Posts más populares
        popular_posts = Post.objects.filter(status='published').annotate(
            popularity=Count('comments') + Count('likes')
        ).order_by('-popularity')[:5]
        
        # Mostrar estadísticas
        self.stdout.write(self.style.SUCCESS('=== ESTADÍSTICAS DEL BLOG ===\n'))
        
        self.stdout.write(f'📊 GENERALES:')
        self.stdout.write(f'   Posts publicados: {total_posts}')
        self.stdout.write(f'   Usuarios registrados: {total_users}')
        self.stdout.write(f'   Comentarios activos: {total_comments}')
        self.stdout.write(f'   Categorías: {total_categories}\n')
        
        self.stdout.write(f'📈 {period_name.upper()}:')
        self.stdout.write(f'   Posts nuevos: {period_posts}')
        self.stdout.write(f'   Comentarios nuevos: {period_comments}\n')
        
        self.stdout.write(f'👑 TOP AUTORES:')
        for i, author in enumerate(top_authors, 1):
            self.stdout.write(f'   {i}. {author.username}: {author.post_count} posts')
        
        self.stdout.write(f'\n📁 TOP CATEGORÍAS:')
        for i, category in enumerate(top_categories, 1):
            self.stdout.write(f'   {i}. {category.name}: {category.post_count} posts')
        
        self.stdout.write(f'\n🔥 POSTS MÁS POPULARES:')
        for i, post in enumerate(popular_posts, 1):
            self.stdout.write(f'   {i}. {post.title}: {post.popularity} interacciones')

# blog/utils.py - Utilidades del blog
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post

def send_new_post_notification(post):
    """Envía notificación de nuevo post a suscriptores"""
    if post.status == 'published':
        # En un escenario real, tendrías un modelo de Subscriber
        # subscribers = Subscriber.objects.filter(active=True)
        
        # Por ahora, notificar a todos los usuarios
        recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
        
        subject = f'Nuevo post: {post.title}'
        html_message = render_to_string('blog/emails/new_post_notification.html', {
            'post': post,
            'site_url': 'https://myblog.com'
        })
        
        try:
            send_mail(
                subject=subject,
                message='',  # Versión texto plano vacía
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False
            )
            return True
        except Exception as e:
            print(f'Error enviando notificación: {e}')
            return False

def calculate_read_time(content):
    """Calcula tiempo de lectura estimado"""
    words = len(content.split())
    # Promedio de 200 palabras por minuto
    minutes = max(1, round(words / 200))
    return minutes

def generate_post_excerpt(content, max_length=300):
    """Genera excerpt inteligente para posts"""
    if len(content) <= max_length:
        return content
    
    # Buscar el último punto antes del límite
    truncated = content[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.7:  # Si está en el último 30%
        return content[:last_period + 1]
    else:
        # Buscar el último espacio para no cortar palabras
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + '...'

class BlogAnalytics:
    """Clase para análisis del blog"""
    
    @staticmethod
    def get_engagement_metrics():
        """Obtiene métricas de engagement"""
        from django.db.models import Avg, Count
        
        metrics = Post.objects.filter(status='published').aggregate(
            avg_views=Avg('views_count'),
            avg_likes=Avg('likes_count'),
            avg_comments=Avg('comments__id'),
            total_posts=Count('id')
        )
        
        return {
            'average_views_per_post': round(metrics['avg_views'] or 0, 2),
            'average_likes_per_post': round(metrics['avg_likes'] or 0, 2),
            'average_comments_per_post': round(metrics['avg_comments'] or 0, 2),
            'total_published_posts': metrics['total_posts']
        }
    
    @staticmethod
    def get_content_performance():
        """Analiza rendimiento del contenido"""
        # Posts con mejor engagement
        top_posts = Post.objects.filter(status='published').annotate(
            engagement_score=(
                Count('comments') * 3 +  # Comentarios valen más
                Count('likes') * 2 +     # Likes valen medio
                models.F('views_count')   # Vistas valen menos
            )
        ).order_by('-engagement_score')[:10]
        
        return {
            'top_performing_posts': [
                {
                    'title': post.title,
                    'engagement_score': post.engagement_score,
                    'views': post.views_count,
                    'likes': post.likes_count,
                    'comments': post.comments.count()
                }
                for post in top_posts
            ]
        }

# blog/context_processors.py - Context processors
def blog_context(request):
    """Context processor para datos globales del blog"""
    from django.db.models import Count
    from django.core.cache import cache
    
    # Intentar obtener del caché
    context = cache.get('blog_global_context')
    
    if context is None:
        from .models import Category, Post
        
        context = {
            'sidebar_categories': Category.objects.annotate(
                post_count=Count('posts', filter=models.Q(posts__status='published'))
            ).filter(post_count__gt=0).order_by('-post_count')[:10],
            
            'sidebar_recent_posts': Post.objects.filter(status='published')
                                               .select_related('author')[:5],
            
            'total_published_posts': Post.objects.filter(status='published').count(),
        }
        
        # Cachear por 15 minutos
        cache.set('blog_global_context', context, 900)
    
    return context

# blog/middleware.py - Middleware personalizado
import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class BlogStatsMiddleware(MiddlewareMixin):
    """Middleware para recopilar estadísticas del blog"""
    
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        # Calcular tiempo de respuesta
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f'{duration:.2f}s'
        
        # Incrementar contador de páginas vistas
        if request.path.startswith('/post/'):
            cache_key = f'page_views_{request.path}'
            current_views = cache.get(cache_key, 0)
            cache.set(cache_key, current_views + 1, 86400)  # 24 horas
        
        return response

class SecurityMiddleware(MiddlewareMixin):
    """Middleware de seguridad para el blog"""
    
    def process_response(self, request, response):
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

# blog/apps.py - Configuración de la app
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Blog'
    
    def ready(self):
        # Importar señales
        import blog.signals

# blog/admin.py - Admin personalizado avanzado
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Post, Category, Comment, Tag, PostLike, UserProfile
import csv

class ExportCsvMixin:
    """Mixin para exportar datos a CSV"""
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    
    export_as_csv.short_description = "Exportar seleccionados a CSV"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title', 'author', 'category', 'status', 'views_count', 'comment_count', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at', 'comment_count_display')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    actions = ['mark_as_published', 'mark_as_draft', 'export_as_csv']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Contenido', {
            'fields': ('content', 'excerpt', 'featured_image'),
            'classes': ('wide',)
        }),
        ('Clasificación', {
            'fields': ('tags',),
        }),
        ('Estadísticas', {
            'fields': ('views_count', 'likes_count', 'comment_count_display'),
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
    
    def comment_count_display(self, obj):
        count = obj.comments.filter(active=True).count()
        return format_html(
            '<strong>{}</strong> activos, <span style="color: #999;">{}</span> inactivos',
            count,
            obj.comments.filter(active=False).count()
        )
    comment_count_display.short_description = 'Comentarios detalle'
    
    def mark_as_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts marcados como publicados.')
    mark_as_published.short_description = 'Marcar como publicados'
    
    def mark_as_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts marcados como borradores.')
    mark_as_draft.short_description = 'Marcar como borradores'

# Personalización del Admin Site
class BlogAdminSite(admin.AdminSite):
    site_header = 'Administración del Blog'
    site_title = 'Blog Admin'
    index_title = 'Panel de Control del Blog'
    
    def index(self, request, extra_context=None):
        """Dashboard personalizado con métricas"""
        extra_context = extra_context or {}
        
        from django.utils import timezone
        last_week = timezone.now() - timedelta(days=7)
        last_month = timezone.now() - timedelta(days=30)
        
        # Métricas principales
        stats = {
            'total_posts': Post.objects.filter(status='published').count(),
            'draft_posts': Post.objects.filter(status='draft').count(),
            'total_comments': Comment.objects.filter(active=True).count(),
            'pending_comments': Comment.objects.filter(active=False).count(),
            'total_users': User.objects.count(),
            'posts_this_week': Post.objects.filter(created_at__gte=last_week).count(),
            'posts_this_month': Post.objects.filter(created_at__gte=last_month).count(),
        }
        
        # Posts más populares
        popular_posts = Post.objects.filter(status='published').annotate(
            engagement=Count('comments') + Count('likes')
        ).order_by('-engagement')[:5]
        
        # Categorías más activas
        active_categories = Category.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        ).order_by('-post_count')[:5]
        
        # Comentarios recientes que necesitan moderación
        pending_comments = Comment.objects.filter(active=False).order_by('-created_at')[:5]
        
        extra_context.update({
            'stats': stats,
            'popular_posts': popular_posts,
            'active_categories': active_categories,
            'pending_comments': pending_comments,
        })
        
        return super().index(request, extra_context)

# Crear instancia personalizada del admin
admin_site = BlogAdminSite(name='blog_admin')

# Registrar modelos en el admin personalizado
admin_site.register(Post, PostAdmin)
admin_site.register(Category)
admin_site.register(Comment)
admin_site.register(Tag)
admin_site.register(User)

# blog/templatetags/admin_extras.py - Tags para el admin
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def admin_metric_card(title, value, icon, color='primary'):
    """Genera tarjeta de métrica para el dashboard"""
    return format_html(
        '''
        <div class="col-md-3">
            <div class="card border-{color} mb-3">
                <div class="card-body text-center">
                    <i class="fas fa-{icon} fa-2x text-{color} mb-2"></i>
                    <h3 class="text-{color}">{value}</h3>
                    <p class="card-text">{title}</p>
                </div>
            </div>
        </div>
        ''',
        color=color,
        icon=icon,
        value=value,
        title=title
    )

# blog/signals.py - Señales completas
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, Post, Comment
from .utils import send_new_post_notification

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Crear o actualizar perfil de usuario"""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

@receiver(post_save, sender=Post)
def post_saved_handler(sender, instance, created, **kwargs):
    """Manejar acciones cuando se guarda un post"""
    # Invalidar caché
    cache_keys = [
        'blog_global_context',
        'popular_posts_5',
        'recent_posts',
        f'post_detail_{instance.pk}',
    ]
    cache.delete_many(cache_keys)
    
    # Si es un nuevo post publicado, enviar notificaciones
    if created and instance.status == 'published':
        # Enviar notificación asíncrona (en un proyecto real usarías Celery)
        try:
            send_new_post_notification(instance)
        except Exception as e:
            print(f'Error enviando notificación: {e}')

@receiver(post_save, sender=Comment)
def comment_saved_handler(sender, instance, created, **kwargs):
    """Manejar acciones cuando se guarda un comentario"""
    if created:
        # Invalidar caché relacionado
        cache.delete('blog_global_context')
        cache.delete(f'post_detail_{instance.post.pk}')
        
        # Notificar al autor del post (si no es él mismo quien comenta)
        if instance.author != instance.post.author:
            try:
                send_mail(
                    subject=f'Nuevo comentario en "{instance.post.title}"',
                    message=f'{instance.author.username} comentó: {instance.content[:100]}...',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.post.author.email],
                    fail_silently=True
                )
            except:
                pass  # Fallar silenciosamente si hay problemas con email

@receiver(pre_save, sender=Post)
def post_pre_save_handler(sender, instance, **kwargs):
    """Acciones antes de guardar un post"""
    # Auto-generar excerpt si no existe
    if not instance.excerpt and instance.content:
        from .utils import generate_post_excerpt
        instance.excerpt = generate_post_excerpt(instance.content)

# requirements.txt - Dependencias del proyecto
"""
Django==4.2.7
Pillow==10.0.1
python-decouple==3.8
django-extensions==3.2.3
faker==19.12.0
django-debug-toolbar==4.2.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
django-taggit==4.0.0
django-cors-headers==4.3.1
redis==5.0.1
celery==5.3.4
django-storages==1.14.2
boto3==1.34.0
gunicorn==21.2.0
psycopg2-binary==2.9.8
whitenoise==6.6.0
django-environ==0.11.2
"""

# docker-compose.yml - Para desarrollo con Docker
"""
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: blog_db
      POSTGRES_USER: blog_user
      POSTGRES_PASSWORD: blog_pass
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://blog_user:blog_pass@db:5432/blog_db
      - REDIS_URL=redis://redis:6379/1

  celery:
    build: .
    command: celery -A myproject worker -l info
    volumes:
      - .:/code
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://blog_user:blog_pass@db:5432/blog_db
      - REDIS_URL=redis://redis:6379/1

volumes:
  postgres_data:
"""

# Dockerfile
"""
FROM python:3.11

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
"""

# myproject/settings/production.py - Settings de producción
"""
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/blog.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'blog': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Celery
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')

# Sentry (monitoreo de errores)
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )
"""

# deploy.sh - Script de deployment
"""
#!/bin/bash

# Script de deployment para producción

set -e

echo "🚀 Iniciando deployment..."

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

# Recopilar archivos estáticos
echo "📂 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar tests
echo "🧪 Ejecutando tests..."
python manage.py test

# Generar sitemap
echo "🗺️ Generando sitemap..."
python manage.py generate_sitemap

# Limpiar datos antiguos
echo "🧹 Limpiando datos antiguos..."
python manage.py cleanup_blog --days=90

# Restart services
echo "🔄 Reiniciando servicios..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart celery

echo "✅ Deployment completado!"
"""

# fabfile.py - Para deployment con Fabric
"""
from fabric import task
import os

@task
def deploy(ctx):
    \"\"\"Deploy completo a producción\"\"\"
    with ctx.cd('/var/www/blog'):
        # Git pull
        ctx.run('git pull origin main')
        
        # Activar virtual env e instalar deps
        ctx.run('source venv/bin/activate && pip install -r requirements.txt')
        
        # Migraciones
        ctx.run('source venv/bin/activate && python manage.py migrate')
        
        # Collect static
        ctx.run('source venv/bin/activate && python manage.py collectstatic --noinput')
        
        # Tests
        ctx.run('source venv/bin/activate && python manage.py test')
        
        # Restart services
        ctx.run('sudo systemctl restart gunicorn')
        ctx.run('sudo systemctl restart nginx')
        
    print("✅ Deployment completado!")

@task
def backup_db(ctx):
    \"\"\"Backup de base de datos\"\"\"
    timestamp = ctx.run('date +%Y%m%d_%H%M%S', hide=True).stdout.strip()
    ctx.run(f'pg_dump blog_db > backup_{timestamp}.sql')
    print(f"✅ Backup creado: backup_{timestamp}.sql")
"""
            'posts# blog/tests.py - Tests comprehensivos
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Post, Category, Comment, Tag, UserProfile
from .forms import PostFormExtended, CommentForm

class PostModelTest(TestCase):
    """Tests para el modelo Post"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Tecnología',
            slug='tecnologia'
        )
    
    def test_post_creation(self):
        """Test creación básica de post"""
        post = Post.objects.create(
            title='Test Post',
            content='Contenido de prueba',
            author=self.user,
            category=self.category,
            status='published'
        )
        
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(str(post), 'Test Post')
    
    def test_post_auto_slug_generation(self):
        """Test generación automática de slug"""
        post = Post.objects.create(
            title='Mi Post con Espacios y Acentos ñ',
            content='Contenido',
            author=self.user,
            category=self.category
        )
        self.assertEqual(post.slug, 'mi-post-con-espacios-y-acentos-n')
    
    def test_post_excerpt_auto_generation(self):
        """Test generación automática de excerpt"""
        long_content = 'A' * 400  # Contenido largo
        post = Post.objects.create(
            title='Test Post',
            content=long_content,
            author=self.user,
            category=self.category
        )
        
        self.assertEqual(len(post.excerpt), 300)  # 297 + '...'
        self.assertTrue(post.excerpt.endswith('...'))
    
    def test_increment_views(self):
        """Test incremento de vistas"""
        post = Post.objects.create(
            title='Test Post',
            content='Contenido',
            author=self.user,
            category=self.category
        )
        
        initial_views = post.views_count
        post.increment_views()
        post.refresh_from_db()
        
        self.assertEqual(post.views_count, initial_views + 1)

class PostViewTest(TestCase):
    """Tests para las views de Post"""