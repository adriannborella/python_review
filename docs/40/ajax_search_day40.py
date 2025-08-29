# ================================
# AJAX SEARCH - EJERCICIO DÍA 40
# ================================

# ===== VIEWS PARA AJAX (articles/ajax_views.py) =====
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Article
import json

def ajax_search_articles(request):
    """Vista AJAX para búsqueda de artículos"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    status = request.GET.get('status', '')
    page = request.GET.get('page', 1)
    
    # Base queryset
    articles = Article.objects.select_related('author', 'category')
    
    # Apply filters
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    if status:
        articles = articles.filter(status=status)
    else:
        articles = articles.filter(status='published')  # Default to published
    
    # Pagination
    paginator = Paginator(articles, 6)
    page_obj = paginator.get_page(page)
    
    # Render articles HTML
    articles_html = render_to_string(
        'articles/ajax/article_cards.html',
        {'page_obj': page_obj, 'query': query}
    )
    
    # Render pagination HTML
    pagination_html = render_to_string(
        'articles/ajax/pagination.html',
        {'page_obj': page_obj}
    )
    
    return JsonResponse({
        'success': True,
        'articles_html': articles_html,
        'pagination_html': pagination_html,
        'total_results': paginator.count,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_results': paginator.count > 0
    })

def ajax_article_suggestions(request):
    """Vista AJAX para sugerencias de búsqueda (autocomplete)"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get title suggestions
    title_suggestions = Article.objects.filter(
        title__icontains=query,
        status='published'
    ).values_list('title', flat=True)[:5]
    
    # Get tag suggestions
    tag_suggestions = []
    articles_with_tags = Article.objects.filter(
        tags__icontains=query,
        status='published'
    ).values_list('tags', flat=True)
    
    for tags_string in articles_with_tags:
        tags = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        tag_suggestions.extend([
            tag for tag in tags 
            if query.lower() in tag.lower() and tag not in tag_suggestions
        ])
    
    # Combine and limit suggestions
    all_suggestions = list(title_suggestions) + tag_suggestions[:3]
    
    return JsonResponse({
        'suggestions': all_suggestions[:8]
    })

def ajax_toggle_article_status(request, slug):
    """Vista AJAX para cambiar status de artículo"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        article = Article.objects.get(slug=slug, author=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in ['draft', 'published', 'archived']:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        old_status = article.status
        article.status = new_status
        article.save()
        
        return JsonResponse({
            'success': True,
            'old_status': old_status,
            'new_status': new_status,
            'message': f'Article status changed from {old_status} to {new_status}'
        })
        
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

# ===== URL PATTERNS PARA AJAX (articles/ajax_urls.py) =====
from django.urls import path
from . import ajax_views

app_name = 'ajax'

urlpatterns = [
    path('search/', ajax_views.ajax_search_articles, name='search_articles'),
    path('suggestions/', ajax_views.ajax_article_suggestions, name='article_suggestions'),
    path('toggle-status/<slug:slug>/', ajax_views.ajax_toggle_article_status, name='toggle_status'),
]

# ===== MIDDLEWARE PERSONALIZADO (articles/middleware.py) =====
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AjaxExceptionMiddleware:
    """Middleware para manejar excepciones en requests AJAX"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.error(f"AJAX Exception: {exception}", exc_info=True)
            
            if settings.DEBUG:
                return JsonResponse({
                    'error': str(exception),
                    'type': exception.__class__.__name__
                }, status=500)
            else:
                return JsonResponse({
                    'error': 'An internal error occurred'
                }, status=500)
        
        return None

# ===== MANAGEMENT COMMAND (management/commands/generate_test_data.py) =====
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Article, Category
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate test data for AJAX demonstrations'
    
    def add_arguments(self, parser):
        parser.add_argument('--articles', type=int, default=50, help='Number of articles')
        parser.add_argument('--categories', type=int, default=8, help='Number of categories')
        parser.add_argument('--users', type=int, default=5, help='Number of users')
    
    def handle(self, *args, **options):
        fake = Faker()
        
        # Create users
        users = []
        for i in range(options['users']):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                users.append(user)
        
        # Create categories
        categories = []
        category_names = [
            'Technology', 'Science', 'Health', 'Travel', 'Food',
            'Sports', 'Music', 'Art', 'Business', 'Education'
        ]
        
        for name in category_names[:options['categories']]:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': fake.text(max_nb_chars=200)}
            )
            categories.append(category)
        
        # Create articles
        tech_words = ['AI', 'Machine Learning', 'Python', 'Django', 'JavaScript', 'React']
        science_words = ['Research', 'Discovery', 'Innovation', 'Study', 'Analysis']
        common_tags = ['tutorial', 'guide', 'tips', 'howto', 'review', 'news', 'update']
        
        for i in range(options['articles']):
            # Generate realistic titles
            if random.choice([True, False]):
                title_words = random.choice([tech_words, science_words])
                title = f"How to Master {random.choice(title_words)}: {fake.sentence(nb_words=4)}"
            else:
                title = fake.sentence(nb_words=random.randint(4, 8)).rstrip('.')
            
            # Generate tags
            selected_tags = random.sample(common_tags, random.randint(2, 5))
            if random.choice([True, False]):
                selected_tags.append(fake.word())
            
            article = Article.objects.create(
                title=title,
                slug=fake.unique.slug(),
                author=random.choice(users),
                category=random.choice(categories),
                content=fake.text(max_nb_chars=random.randint(500, 2000)),
                status=random.choices(
                    ['published', 'draft', 'archived'],
                    weights=[0.7, 0.2, 0.1]
                )[0],
                tags=', '.join(selected_tags)
            )
            
            if i % 10 == 0:
                self.stdout.write(f'Created {i+1} articles...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {options["articles"]} articles, '
                f'{len(categories)} categories, and {len(users)} users!'
            )
        )

# ===== CUSTOM DECORATORS (articles/decorators.py) =====
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def ajax_required(view_func):
    """Decorator que requiere que el request sea AJAX"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'AJAX request required'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper

def ajax_login_required(view_func):
    """Decorator combinado para login + AJAX"""
    @wraps(view_func)
    @ajax_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def json_response(view_func):
    """Decorator que convierte excepciones en JSON responses"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    return wrapper

# ===== UTILS PARA AJAX (articles/ajax_utils.py) =====
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json

class AjaxResponseMixin:
    """Mixin para views que manejan AJAX"""
    
    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.is_ajax = True
        else:
            self.is_ajax = False
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        if self.is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'Operation completed successfully'
            })
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.is_ajax:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

def serialize_articles(articles, fields=None):
    """Serializa artículos para respuestas AJAX"""
    if fields is None:
        fields = ['id', 'title', 'slug', 'status', 'created_at']
    
    data = []
    for article in articles:
        item = {}
        for field in fields:
            if hasattr(article, field):
                value = getattr(article, field)
                if hasattr(value, 'isoformat'):  # datetime objects
                    value = value.isoformat()
                elif hasattr(value, 'url'):  # file fields
                    value = value.url
                item[field] = value
        
        # Add related data
        item['author'] = article.author.username
        item['category'] = article.category.name if article.category else None
        item['tags'] = article.get_tags_list()
        
        data.append(item)
    
    return data

# ===== CONTEXT PROCESSOR PARA AJAX (articles/context_processors.py) =====
from django.conf import settings

def ajax_context(request):
    """Context processor que agrega variables útiles para AJAX"""
    return {
        'AJAX_TIMEOUT': getattr(settings, 'AJAX_TIMEOUT', 10000),  # 10 seconds
        'CSRF_COOKIE_NAME': settings.CSRF_COOKIE_NAME,
        'is_ajax': request.headers.get('X-Requested-With') == 'XMLHttpRequest',
    }

# ===== TESTS PARA AJAX (articles/tests/test_ajax_views.py) =====
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from articles.models import Article, Category
import json

class AjaxViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            author=self.user,
            category=self.category,
            content='Test content',
            status='published',
            tags='test, ajax'
        )
    
    def test_ajax_search_articles(self):
        """Test AJAX search functionality"""
        response = self.client.get(
            reverse('ajax:search_articles'),
            {'q': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_results'], 0)
        self.assertIn('articles_html', data)
    
    def test_ajax_article_suggestions(self):
        """Test AJAX autocomplete suggestions"""
        response = self.client.get(
            reverse('ajax:article_suggestions'),
            {'q': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('suggestions', data)
        self.assertGreater(len(data['suggestions']), 0)
    
    def test_ajax_toggle_status_authenticated(self):
        """Test status toggle with authentication"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('ajax:toggle_status', args=[self.article.slug]),
            json.dumps({'status': 'draft'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_status'], 'draft')
        
        # Verify in database
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, 'draft')
    
    def test_ajax_toggle_status_unauthenticated(self):
        """Test status toggle without authentication"""
        response = self.client.post(
            reverse('ajax:toggle_status', args=[self.article.slug]),
            json.dumps({'status': 'draft'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_non_ajax_request_rejection(self):
        """Test that non-AJAX requests are rejected"""
        response = self.client.get(
            reverse('ajax:search_articles'),
            {'q': 'test'}
        )
        
        self.assertEqual(response.status_code, 400)