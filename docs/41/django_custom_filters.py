# blog/templatetags/__init__.py
# Archivo vacío para hacer que templatetags sea un paquete Python

# blog/templatetags/blog_extras.py
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from datetime import datetime, timedelta
import re

register = template.Library()

# FILTROS PERSONALIZADOS

@register.filter
def reading_time(content):
    """Calcula el tiempo estimado de lectura en minutos"""
    words = len(content.split())
    # Promedio de 200 palabras por minuto
    minutes = max(1, round(words / 200))
    return f"{minutes} min de lectura"

@register.filter
def highlight_search(text, search_term):
    """Resalta términos de búsqueda en el texto"""
    if not search_term:
        return text
    
    highlighted = re.sub(
        f'({re.escape(search_term)})', 
        r'<mark class="bg-warning">\1</mark>', 
        text, 
        flags=re.IGNORECASE
    )
    return mark_safe(highlighted)

@register.filter
def time_since_short(date):
    """Versión corta de tiempo transcurrido"""
    now = datetime.now()
    if date.tzinfo:
        from django.utils import timezone
        now = timezone.now()
    
    diff = now - date
    
    if diff.days > 7:
        return date.strftime("%d %b %Y")
    elif diff.days > 0:
        return f"hace {diff.days}d"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"hace {hours}h"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"hace {minutes}m"
    else:
        return "ahora"

@register.filter
def truncate_smart(text, length=100):
    """Trunca texto de forma inteligente, respetando palabras"""
    if len(text) <= length:
        return text
    
    truncated = text[:length]
    # Buscar el último espacio para no cortar palabras
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + '...'

@register.filter
def add_css_class(field, css_class):
    """Añade clases CSS a campos de formulario"""
    return field.as_widget(attrs={'class': css_class})

@register.filter
def to_json(value):
    """Convierte valor a JSON para usar en JavaScript"""
    import json
    return mark_safe(json.dumps(value))

# TEMPLATE TAGS PERSONALIZADOS

@register.simple_tag
def url_with_params(url_name, **kwargs):
    """Genera URL con parámetros GET"""
    from django.urls import reverse
    from django.http import QueryDict
    
    url = reverse(url_name)
    if kwargs:
        query_dict = QueryDict('', mutable=True)
        query_dict.update(kwargs)
        url += '?' + query_dict.urlencode()
    return url

@register.simple_tag(takes_context=True)
def active_nav(context, url_name):
    """Determina si un elemento de navegación está activo"""
    request = context['request']
    current_url = request.resolver_match.url_name
    return 'active' if current_url == url_name else ''

@register.inclusion_tag('blog/partials/post_card.html')
def render_post_card(post, show_actions=False):
    """Renderiza una tarjeta de post reutilizable"""
    return {
        'post': post,
        'show_actions': show_actions
    }

@register.inclusion_tag('blog/partials/pagination.html', takes_context=True)
def render_pagination(context, page_obj):
    """Renderiza paginación reutilizable"""
    request = context['request']
    return {
        'page_obj': page_obj,
        'request': request
    }

@register.simple_tag
def get_popular_posts(limit=5):
    """Obtiene posts populares basados en comentarios"""
    from blog.models import Post
    from django.db.models import Count
    
    return Post.objects.filter(status='published')\
        .annotate(comment_count=Count('comments'))\
        .order_by('-comment_count', '-created_at')[:limit]

@register.simple_tag
def get_recent_comments(limit=5):
    """Obtiene comentarios recientes"""
    from blog.models import Comment
    
    return Comment.objects.filter(active=True)\
        .select_related('post', 'author')\
        .order_by('-created_at')[:limit]

# TEMPLATE TAGS AVANZADOS

@register.assignment_tag
def get_category_stats():
    """Obtiene estadísticas de categorías"""
    from blog.models import Category, Post
    from django.db.models import Count
    
    return Category.objects.annotate(
        post_count=Count('posts', filter=models.Q(posts__status='published')),
        recent_posts=Count('posts', filter=models.Q(
            posts__status='published',
            posts__created_at__gte=datetime.now() - timedelta(days=7)
        ))
    ).filter(post_count__gt=0).order_by('-post_count')

@register.simple_tag(takes_context=True)
def breadcrumb(context, title=None):
    """Genera breadcrumbs automáticamente"""
    request = context['request']
    url_name = request.resolver_match.url_name
    
    breadcrumbs = [
        {'title': 'Inicio', 'url': reverse('post_list')}
    ]
    
    if url_name == 'post_detail':
        breadcrumbs.append({
            'title': title or 'Post',
            'url': None  # Actual page
        })
    elif url_name == 'post_create':
        breadcrumbs.append({
            'title': 'Crear Post',
            'url': None
        })
    elif url_name == 'post_edit':
        breadcrumbs.extend([
            {'title': title or 'Post', 'url': '#'},
            {'title': 'Editar', 'url': None}
        ])
    
    return breadcrumbs

# FILTROS DE SEGURIDAD Y VALIDACIÓN

@register.filter
def safe_markdown(text):
    """Renderiza markdown de forma segura (requiere markdown library)"""
    try:
        import markdown
        from django.utils.safestring import mark_safe
        
        md = markdown.Markdown(extensions=['extra', 'codehilite'])
        return mark_safe(md.convert(text))
    except ImportError:
        # Fallback si no está instalado markdown
        return text.replace('\n', '<br>')

@register.filter
def extract_first_image(content):
    """Extrae la primera imagen del contenido HTML"""
    import re
    
    img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    match = re.search(img_pattern, content)
    return match.group(1) if match else None

# CONTEXTO PROCESSORS PERSONALIZADOS (context_processors.py)

def blog_context(request):
    """Context processor para datos globales del blog"""
    from blog.models import Category, Post
    from django.db.models import Count
    
    return {
        'categories': Category.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        ).filter(post_count__gt=0),
        'recent_posts': Post.objects.filter(status='published')[:5],
        'total_posts': Post.objects.filter(status='published').count(),
    }

# MIDDLEWARE PERSONALIZADO (middleware.py)

class BlogMiddleware:
    """Middleware para funcionalidades del blog"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Código antes de la vista
        response = self.get_response(request)
        
        # Código después de la vista
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Registrar última actividad del usuario
            from django.utils import timezone
            request.user.last_login = timezone.now()
            request.user.save(update_fields=['last_login'])
        
        return response

# MANAGEMENT COMMANDS (management/commands/generate_test_data.py)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Genera datos de prueba para el blog'
    
    def add_arguments(self, parser):
        parser.add_argument('--posts', type=int, default=20, help='Número de posts a crear')
        parser.add_argument('--comments', type=int, default=50, help='Número de comentarios a crear')
    
    def handle(self, *args, **options):
        fake = Faker(['es_ES'])
        
        # Crear usuario de prueba si no existe
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Usuario creado: {user.username}')
        
        # Crear categorías si no existen
        categories = ['Tecnología', 'Programación', 'Django', 'Python', 'Web Development']
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Categoría creada: {category.name}')
        
        # Crear posts
        categories = Category.objects.all()
        for _ in range(options['posts']):
            post = Post.objects.create(
                title=fake.sentence(nb_words=6)[:-1],
                slug=fake.slug(),
                author=user,
                content=fake.text(max_nb_chars=2000),
                category=random.choice(categories),
                status='published',
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
        
        self.stdout.write(f'Creados {options["posts"]} posts')
        
        # Crear comentarios
        posts = Post.objects.all()
        for _ in range(options['comments']):
            comment = Comment.objects.create(
                post=random.choice(posts),
                author=user,
                content=fake.text(max_nb_chars=500),
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
        
        self.stdout.write(f'Creados {options["comments"]} comentarios')
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados exitosamente!'))