# settings.py - Configuración para debugging y análisis de performance

DEBUG = True

# Debug Toolbar
INSTALLED_APPS = [
    # ... tus apps ...
    'debug_toolbar',
    'django_extensions',  # Para shell_plus --print-sql
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... otros middlewares ...
]

# Configuración Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 500,  # ms
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',  # ¡El más importante!
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# Logging para SQL queries
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'sql.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# urls.py - Incluir debug toolbar
from django.conf import settings
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    # ... tus URLs ...
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# ============================================================================
# management/commands/analyze_queries.py - Comando para análisis de performance
# ============================================================================

from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Analiza performance de queries comunes'
    
    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Mostrar SQL')
    
    def handle(self, *args, **options):
        # Asegurar que DEBUG esté activado
        settings.DEBUG = True
        
        self.stdout.write('Analizando queries de productos...\n')
        
        # Test 1: Lista de productos SIN optimización
        self.stdout.write('=== Test 1: Lista productos SIN optimización ===')
        reset_queries()
        start_time = time.time()
        
        from products.models import Product
        products = Product.objects.all()[:10]
        for product in products:
            _ = product.category.name  # Trigger N+1
            _ = product.brand.name if product.brand else "No brand"
        
        end_time = time.time()
        query_count = len(connection.queries)
        
        self.stdout.write(f'Tiempo: {end_time - start_time:.4f}s')
        self.stdout.write(f'Queries: {query_count}')
        if options['verbose']:
            for query in connection.queries[-5:]:  # Últimas 5 queries
                self.stdout.write(f"SQL: {query['sql'][:100]}...")
        self.stdout.write('')
        
        # Test 2: Lista de productos CON optimización
        self.stdout.write('=== Test 2: Lista productos CON optimización ===')
        reset_queries()
        start_time = time.time()
        
        products = Product.objects.select_related('category', 'brand')[:10]
        for product in products:
            _ = product.category.name  # Sin query adicional
            _ = product.brand.name if product.brand else "No brand"
        
        end_time = time.time()
        query_count = len(connection.queries)
        
        self.stdout.write(f'Tiempo: {end_time - start_time:.4f}s')
        self.stdout.write(f'Queries: {query_count}')
        self.stdout.write('')
        
        # Test 3: Query compleja con agregaciones
        self.stdout.write('=== Test 3: Estadísticas por categoría ===')
        reset_queries()
        start_time = time.time()
        
        from django.db.models import Count, Avg
        from products.models import Category
        
        stats = Category.objects.annotate(
            product_count=Count('products'),
            avg_price=Avg('products__price')
        ).filter(product_count__gt=0)
        
        for category in stats:
            self.stdout.write(
                f'{category.name}: {category.product_count} productos, '
                f'precio promedio: ${category.avg_price:.2f}'
            )
        
        end_time = time.time()
        query_count = len(connection.queries)
        
        self.stdout.write(f'\nTiempo: {end_time - start_time:.4f}s')
        self.stdout.write(f'Queries: {query_count}')
        
        if options['verbose']:
            self.stdout.write('\nSQL de la query compleja:')
            self.stdout.write(str(stats.query))

# ============================================================================
# utils/query_analyzer.py - Utilidades para análisis en vivo
# ============================================================================

from django.db import connection
from django.conf import settings
import time
import functools

def query_debugger(func):
    """
    Decorator para debuggear queries de una función
    Uso: @query_debugger encima de una vista o función
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.DEBUG:
            return func(*args, **kwargs)
        
        # Reset query log
        connection.queries_log.clear()
        start_time = time.time()
        
        # Ejecutar función
        result = func(*args, **kwargs)
        
        # Calcular métricas
        end_time = time.time()
        query_count = len(connection.queries)
        total_time = sum(float(q['time']) for q in connection.queries)
        
        print(f"\n{'='*50}")
        print(f"Function: {func.__name__}")
        print(f"Execution time: {end_time - start_time:.4f}s")
        print(f"Database queries: {query_count}")
        print(f"Database time: {total_time:.4f}s")
        
        # Mostrar queries lentas
        slow_queries = [q for q in connection.queries if float(q['time']) > 0.1]
        if slow_queries:
            print(f"Slow queries ({len(slow_queries)}):")
            for query in slow_queries:
                print(f"  {query['time']}s: {query['sql'][:100]}...")
        
        print('='*50)
        return result
    
    return wrapper

# Ejemplo de uso:
"""
from utils.query_analyzer import query_debugger

@query_debugger
def get_product_list(request):
    products = Product.objects.select_related('category', 'brand')
    return render(request, 'products/list.html', {'products': products})
"""

class QueryProfiler:
    """Context manager para profiling de queries"""
    
    def __init__(self, description="Query"):
        self.description = description
        self.start_time = None
        self.start_queries = None
    
    def __enter__(self):
        if settings.DEBUG:
            connection.queries_log.clear()
            self.start_queries = len(connection.queries)
            self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if settings.DEBUG:
            end_time = time.time()
            query_count = len(connection.queries) - self.start_queries
            execution_time = end_time - self.start_time
            
            print(f"\n[{self.description}]")
            print(f"Execution time: {execution_time:.4f}s")
            print(f"Queries executed: {query_count}")
            
            if query_count > 0:
                recent_queries = connection.queries[-query_count:]
                db_time = sum(float(q['time']) for q in recent_queries)
                print(f"Database time: {db_time:.4f}s")
                print(f"Python time: {execution_time - db_time:.4f}s")

# Uso del QueryProfiler:
"""
with QueryProfiler("Product search"):
    products = Product.objects.select_related('category').filter(name__icontains='phone')
    results = list(products)
"""