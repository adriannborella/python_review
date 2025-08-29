# EJERCICIO 1: Crear un sistema de configuración personalizado
# core/config.py
from django.conf import settings
from typing import Dict, Any
import os

class AppConfig:
    """Configuración centralizada de la aplicación"""
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde múltiples fuentes"""
        config = {}
        
        # Configuración por defecto
        config.update({
            'APP_NAME': 'Interview Project',
            'VERSION': '1.0.0',
            'MAINTENANCE_MODE': False,
            'MAX_UPLOAD_SIZE': 5 * 1024 * 1024,  # 5MB
            'ALLOWED_FILE_EXTENSIONS': ['.jpg', '.jpeg', '.png', '.gif', '.pdf'],
            'PAGINATION_SIZE': 10,
            'CACHE_TIMEOUT': 300,  # 5 minutes
        })
        
        # Override con variables de entorno
        config.update({
            'MAINTENANCE_MODE': os.getenv('MAINTENANCE_MODE', 'false').lower() == 'true',
            'MAX_UPLOAD_SIZE': int(os.getenv('MAX_UPLOAD_SIZE', config['MAX_UPLOAD_SIZE'])),
            'PAGINATION_SIZE': int(os.getenv('PAGINATION_SIZE', config['PAGINATION_SIZE'])),
        })
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene valor de configuración"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Establece valor de configuración (runtime only)"""
        self._config[key] = value
    
    @property
    def is_maintenance_mode(self) -> bool:
        """Verifica si está en modo mantenimiento"""
        return self._config.get('MAINTENANCE_MODE', False)

# Instancia global
app_config = AppConfig()

# EJERCICIO 2: Middleware personalizado para logging y maintenance mode
# core/middleware.py
import logging
import time
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from .config import app_config

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware para logging de requests"""
    
    def process_request(self, request):
        """Procesa el request entrante"""
        request.start_time = time.time()
        
        # Log del request
        logger.info(
            f"Request started: {request.method} {request.path} "
            f"from {request.META.get('REMOTE_ADDR')}"
        )
        
        return None
    
    def process_response(self, request, response):
        """Procesa la response saliente"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Request completed: {request.method} {request.path} "
                f"Status: {response.status_code} Duration: {duration:.2f}s"
            )
        
        return response

class MaintenanceModeMiddleware(MiddlewareMixin):
    """Middleware para modo mantenimiento"""
    
    def process_request(self, request):
        """Verifica si está en modo mantenimiento"""
        if app_config.is_maintenance_mode:
            # Permitir acceso al admin
            if request.path.startswith('/admin/'):
                return None
            
            # Permitir acceso a superusers
            if request.user.is_authenticated and request.user.is_superuser:
                return None
            
            # Mostrar página de mantenimiento
            html = render_to_string('core/maintenance.html')
            return HttpResponse(html, status=503)
        
        return None

# EJERCICIO 3: Sistema de URLs con namespaces avanzados
# core/url_patterns.py
from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

class URLPatternManager:
    """Gestor avanzado de patrones URL"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.patterns = []
        self.api_patterns = []
    
    def add_view(self, pattern: str, view, name: str, methods=None):
        """Añade un patrón URL para vista normal"""
        self.patterns.append(path(pattern, view, name=name))
        return self
    
    def add_api_view(self, pattern: str, view, name: str):
        """Añade un patrón URL para API"""
        self.api_patterns.append(path(f"api/{pattern}", view, name=f"{name}_api"))
        return self
    
    def add_redirect(self, old_pattern: str, new_pattern: str, name: str):
        """Añade un redirect permanente"""
        self.patterns.append(
            path(old_pattern, RedirectView.as_view(pattern_name=new_pattern, permanent=True), name=name)
        )
        return self
    
    def add_regex_pattern(self, regex: str, view, name: str):
        """Añade patrón con expresión regular"""
        self.patterns.append(re_path(regex, view, name=name))
        return self
    
    def get_patterns(self):
        """Retorna todos los patrones"""
        return self.patterns + self.api_patterns

# Uso del URL Pattern Manager
url_manager = URLPatternManager('core')
url_manager.add_view('', views.HomeView.as_view(), 'home') \
          .add_view('dashboard/', views.DashboardView.as_view(), 'dashboard') \
          .add_api_view('status/', views.StatusAPIView.as_view(), 'status') \
          .add_redirect('old-dashboard/', 'core:dashboard', 'old_dashboard_redirect')

urlpatterns = url_manager.get_patterns()

# EJERCICIO 4: Context Processor personalizado
# core/context_processors.py
from django.conf import settings
from .config import app_config

def global_context(request):
    """Context processor que añade variables globales a todos los templates"""
    return {
        'APP_NAME': app_config.get('APP_NAME'),
        'APP_VERSION': app_config.get('VERSION'),
        'DEBUG': settings.DEBUG,
        'MAINTENANCE_MODE': app_config.is_maintenance_mode,
        'USER_IS_AUTHENTICATED': request.user.is_authenticated,
        'CURRENT_PATH': request.path,
        'QUERY_STRING': request.GET.urlencode(),
    }

def navigation_context(request):
    """Context processor para datos de navegación"""
    navigation_items = [
        {'name': 'Home', 'url': 'home', 'icon': 'fas fa-home'},
        {'name': 'Dashboard', 'url': 'core:dashboard', 'icon': 'fas fa-tachometer-alt'},
        {'name': 'Blog', 'url': 'blog:post_list', 'icon': 'fas fa-blog'},
        {'name': 'About', 'url': 'core:about', 'icon': 'fas fa-info-circle'},
        {'name': 'Contact', 'url': 'core:contact', 'icon': 'fas fa-envelope'},
    ]
    
    return {
        'navigation_items': navigation_items,
        'current_section': request.resolver_match.app_name if request.resolver_match else None,
    }

# EJERCICIO 5: Comando de management personalizado
# core/management/__init__.py
# core/management/commands/__init__.py
# core/management/commands/setup_project.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Setup inicial completo del proyecto'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Crear superuser automáticamente'
        )
        parser.add_argument(
            '--load-fixtures',
            action='store_true',
            help='Cargar datos de prueba'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando setup del proyecto...'))
        
        # 1. Aplicar migraciones
        self.stdout.write('📦 Aplicando migraciones...')
        call_command('migrate', verbosity=0)
        
        # 2. Recopilar archivos estáticos
        self.stdout.write('🎨 Recopilando archivos estáticos...')
        call_command('collectstatic', verbosity=0, interactive=False)
        
        # 3. Crear superuser si se solicita
        if options['create_superuser']:
            self.create_superuser()
        
        # 4. Cargar fixtures si se solicita
        if options['load_fixtures']:
            self.load_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Setup completado exitosamente!')
        )
    
    def create_superuser(self):
        """Crea un superuser por defecto"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('👤 Superuser creado (admin/admin123)')
        else:
            self.stdout.write('👤 Superuser ya existe')
    
    def load_sample_data(self):
        """Carga datos de muestra"""
        # Aquí cargarías fixtures o crearías datos de prueba
        self.stdout.write('📊 Datos de muestra cargados')

# EJERCICIO 6: Pruebas para la configuración
# core/tests/test_config.py
from django.test import TestCase, override_settings
from core.config import AppConfig
import os

class AppConfigTestCase(TestCase):
    def setUp(self):
        self.config = AppConfig()
    
    def test_default_config_values(self):
        """Prueba valores por defecto de configuración"""
        self.assertEqual(self.config.get('APP_NAME'), 'Interview Project')
        self.assertEqual(self.config.get('VERSION'), '1.0.0')
        self.assertFalse(self.config.get('MAINTENANCE_MODE'))
    
    def test_environment_override(self):
        """Prueba override con variables de entorno"""
        with override_settings():
            os.environ['MAINTENANCE_MODE'] = 'true'
            config = AppConfig()
            self.assertTrue(config.is_maintenance_mode)
            del os.environ['MAINTENANCE_MODE']
    
    def test_runtime_configuration(self):
        """Prueba configuración en tiempo de ejecución"""
        self.config.set('TEST_VALUE', 'test')
        self.assertEqual(self.config.get('TEST_VALUE'), 'test')
    
    def test_nonexistent_key(self):
        """Prueba acceso a clave no existente"""
        self.assertIsNone(self.config.get('NONEXISTENT_KEY'))
        self.assertEqual(self.config.get('NONEXISTENT_KEY', 'default'), 'default')