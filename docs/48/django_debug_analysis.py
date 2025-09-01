# settings.py - Configuración para debugging y profiling

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Debug y Development settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database con configuración para debugging
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        # ✅ Configuración para logging de queries
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# ✅ Django Debug Toolbar Configuration
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Debug tools
    'debug_toolbar',
    'django_extensions',  # Para shell_plus y otros comandos útiles
    
    # Apps
    'products',
    'orders',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # ✅ Debe estar al principio
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Debug Toolbar Settings
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'HIDE_DJANGO_SQL': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
}

# ✅ Logging configuration para análisis de queries
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'sql': {
            'format': '[{duration:.3f}] {sql}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sql_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['sql_console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# urls.py - URLs con debug toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
]

# ✅ Debug toolbar URLs
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# management/commands/profile_queries.py - Comando personalizado para profiling
from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.test.utils import override_settings
import time

class Command(BaseCommand):
    help = 'Profile database queries for performance testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--view-name',
            type=str,
            help='Name of the view to profile'
        )
        parser.add_argument(
            '--iterations',
            type=int,
            default=10,
            help='Number of iterations to run'
        )
    
    @override_settings(DEBUG=True)
    def handle(self, *args, **options):
        view_name = options['view_name']
        iterations = options['iterations']
        
        if view_name == 'product_list_slow':
            self.profile_product_list_slow(iterations)
        elif view_name == 'product_list_optimized':
            self.profile_product_list_optimized(iterations)
        else:
            self.stdout.write(
                self.style.ERROR(f'Unknown view: {view_name}')
            )
    
    def profile_product_list_slow(self, iterations):
        """Profile the slow product list view"""
        from products.views import product_list_slow
        from django.test import RequestFactory
        
        factory = RequestFactory()
        total_time = 0
        total_queries = 0
        
        self.stdout.write(f'Profiling product_list_slow - {iterations} iterations')
        
        for i in range(iterations):
            reset_queries()
            start_time = time.time()
            
            request = factory.get('/api/products/')
            response = product_list_slow(request)
            
            end_time = time.time()
            execution_time = end_time - start_time
            query_count = len(connection.queries)
            
            total_time += execution_time
            total_queries += query_count
            
            self.stdout.write(f'Iteration {i+1}: {execution_time:.4f}s, {query_count} queries')
        
        avg_time = total_time / iterations
        avg_queries = total_queries / iterations
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nAverage: {avg_time:.4f}s, {avg_queries:.1f} queries'
            )
        )
    
    def profile_product_list_optimized(self, iterations):
        """Profile the optimized product list view"""
        from products.views import product_list_optimized
        from django.test import RequestFactory
        
        factory = RequestFactory()
        total_time = 0
        total_queries = 0
        
        self.stdout.write(f'Profiling product_list_optimized - {iterations} iterations')
        
        for i in range(iterations):
            reset_queries()
            start_time = time.time()
            
            request = factory.get('/api/products/')
            response = product_list_optimized(request)
            
            end_time = time.time()
            execution_time = end_time - start_time
            query_count = len(connection.queries)
            
            total_time += execution_time
            total_queries += query_count
            
            self.stdout.write(f'Iteration {i+1}: {execution_time:.4f}s, {query_count} queries')
        
        avg_time = total_time / iterations
        avg_queries = total_queries / iterations
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nAverage: {avg_time:.4f}s, {avg_queries:.1f} queries'
            )
        )

# utils/performance.py - Utilidades para análisis de performance
from django.db import connection
from django.conf import settings
import time
import functools
import logging

logger = logging.getLogger(__name__)

class QueryCountDebugger:
    """Context manager para contar queries en un bloque de código"""
    
    def __init__(self, description=""):
        self.description = description
        
    def __enter__(self):
        self.queries_before = len(connection.queries)
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.queries_after = len(connection.queries)
        self.end_time = time.time()
        
        query_count = self.queries_after - self.queries_before
        execution_time = self.end_time - self.start_time
        
        print(f"\n{'='*50}")
        if self.description:
            print(f"Debug: {self.description}")
        print(f"Queries executed: {query_count}")
        print(f"Execution time: {execution_time:.4f}s")
        print(f"{'='*50}")
        
        if settings.DEBUG and query_count > 0:
            print("Executed queries:")
            recent_queries = connection.queries[-query_count:]
            for i, query in enumerate(recent_queries, 1):
                print(f"{i}. [{query['time']}s] {query['sql'][:100]}...")

def debug_queries(func):
    """Decorator para debuggear queries de una función"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with QueryCountDebugger(f"Function: {func.__name__}"):
            return func(*args, **kwargs)
    return wrapper

def analyze_query_patterns():
    """Analiza patrones comunes en queries ejecutadas"""
    if not settings.DEBUG:
        return "Query analysis only available in DEBUG mode"
    
    queries = connection.queries
    if not queries:
        return "No queries executed yet"
    
    analysis = {
        'total_queries': len(queries),
        'total_time': sum(float(q['time']) for q in queries),
        'slow_queries': [],
        'repeated_queries': {},
    }
    
    # Encontrar queries lentas (>0.1s)
    for query in queries:
        if float(query['time']) > 0.1:
            analysis['slow_queries'].append({
                'time': query['time'],
                'sql': query['sql'][:200] + '...'
            })
    
    # Encontrar queries repetidas
    for query in queries:
        sql = query['sql'][:100]  # Primeros 100 chars para identificar
        if sql in analysis['repeated_queries']:
            analysis['repeated_queries'][sql] += 1
        else:
            analysis['repeated_queries'][sql] = 1
    
    # Solo mantener las que se repiten
    analysis['repeated_queries'] = {
        k: v for k, v in analysis['repeated_queries'].items() if v > 1
    }
    
    return analysis

# tests/test_performance.py - Tests de performance
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.db import connection, reset_queries
import time

class PerformanceTestCase(TransactionTestCase):
    """Base class para tests de performance"""
    
    def setUp(self):
        reset_queries()
    
    def assertQueryCountLessThan(self, max_queries):
        """Assert que el número de queries sea menor que el máximo"""
        query_count = len(connection.queries)
        self.assertLess(
            query_count, 
            max_queries,
            f"Expected less than {max_queries} queries, got {query_count}"
        )
    
    def assertExecutionTimeLessThan(self, max_time):
        """Assert que el tiempo de ejecución sea menor que el máximo"""
        # Implementar medición de tiempo en el test específico
        pass

class ProductListPerformanceTest(PerformanceTestCase):
    
    def setUp(self):
        super().setUp()
        # Setup test data
        from products.models import Category, Brand, Product
        
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="TechBrand")
        
        # Crear productos de prueba
        for i in range(50):
            Product.objects.create(
                name=f"Product {i}",
                price=10.00 + i,
                category=self.category,
                brand=self.brand
            )
    
    @override_settings(DEBUG=True)
    def test_optimized_product_list_performance(self):
        """Test que la vista optimizada use pocas queries"""
        from products.views import product_list_optimized
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/api/products/')
        
        reset_queries()
        start_time = time.time()
        
        response = product_list_optimized(request)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions de performance
        self.assertQueryCountLessThan(5)  # Máximo 5 queries
        self.assertLess(execution_time, 0.1)  # Menos de 100ms
        self.assertEqual(response.status_code, 200)
        
    @override_settings(DEBUG=True)
    def test_slow_vs_optimized_comparison(self):
        """Compara performance entre vista lenta y optimizada"""
        from products.views import product_list_slow, product_list_optimized
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/api/products/')
        
        # Test vista lenta
        reset_queries()
        start_time = time.time()
        product_list_slow(request)
        slow_time = time.time() - start_time
        slow_queries = len(connection.queries)
        
        # Test vista optimizada
        reset_queries()
        start_time = time.time()
        product_list_optimized(request)
        fast_time = time.time() - start_time
        fast_queries = len(connection.queries)
        
        # La vista optimizada debe ser mejor
        self.assertLess(fast_queries, slow_queries)
        self.assertLess(fast_time, slow_time)
        
        print(f"\nPerformance Comparison:")
        print(f"Slow view: {slow_