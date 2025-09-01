# Django Monitoring, Logging & Security - Día 46

## 🎯 Objetivos del Día
- Implementar logging avanzado y structured logging
- Configurar Sentry para error tracking y performance monitoring
- Aplicar Django security best practices
- Setup monitoring stack completo
- Prepararse para preguntas sobre production readiness

---

## 📚 HORA 1: TEORÍA - MONITORING Y SECURITY

### 1. Advanced Logging Configuration

#### Structured Logging Setup
```python
# settings.py - Production Logging Configuration
import os
from pythonjsonlogger import jsonlogger

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            '()': jsonlogger.JsonFormatter,
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'performance': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/performance.log',
            'formatter': 'json',
        },
        'security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'formatter': 'json',
        },
        'console': {
            'level': 'DEBUG',
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
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'performance': {
            'handlers': ['performance'],
            'level': 'INFO',
            'propagate': False,
        },
        'security': {
            'handlers': ['security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
```

#### Custom Logging Middleware
```python
# middleware.py
import logging
import time
import uuid
from django.utils.deprecation import MiddlewareMixin

performance_logger = logging.getLogger('performance')
security_logger = logging.getLogger('security')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Generate unique request ID
        request.id = str(uuid.uuid4())
        request.start_time = time.time()
        
        # Log request start
        performance_logger.info("Request started", extra={
            'request_id': request.id,
            'method': request.method,
            'path': request.path,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        })
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log response
            log_data = {
                'request_id': getattr(request, 'id', 'unknown'),
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration': round(duration, 3),
                'user_id': request.user.id if request.user.is_authenticated else None,
            }
            
            # Log based on response status
            if response.status_code >= 500:
                performance_logger.error("Server error", extra=log_data)
            elif response.status_code >= 400:
                performance_logger.warning("Client error", extra=log_data)
            elif duration > 1.0:
                performance_logger.warning("Slow request", extra=log_data)
            else:
                performance_logger.info("Request completed", extra=log_data)
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SecurityLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log suspicious activity
        suspicious_patterns = [
            'admin/', 'wp-admin/', '.php', 'eval(', '<script>',
            'union select', 'drop table', '../', 'etc/passwd'
        ]
        
        path_lower = request.path.lower()
        if any(pattern in path_lower for pattern in suspicious_patterns):
            security_logger.warning("Suspicious request detected", extra={
                'ip_address': self.get_client_ip(request),
                'path': request.path,
                'method': request.method,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referer': request.META.get('HTTP_REFERER', ''),
            })
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

### 2. Sentry Integration

#### Complete Sentry Setup
```python
# settings.py - Sentry Configuration
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[
        DjangoIntegration(
            transaction_style='url',
            middleware_spans=True,
            signals_spans=True,
            cache_spans=True,
        ),
        RedisIntegration(),
        CeleryIntegration(monitor_beat_tasks=True),
    ],
    traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
    send_default_pii=False,  # Don't send personally identifiable information
    environment=os.getenv('ENVIRONMENT', 'development'),
    release=os.getenv('GIT_COMMIT', 'unknown'),
)

# Custom error handling
from sentry_sdk import capture_exception, capture_message, set_user, set_tag

def custom_error_handler(request, exception):
    # Set user context for Sentry
    if request.user.is_authenticated:
        set_user({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })
    
    # Add custom tags
    set_tag('request_method', request.method)
    set_tag('request_path', request.path)
    
    # Capture exception with additional context
    capture_exception(exception)
```

#### Custom Sentry Error Classes
```python
# sentry_utils.py
from sentry_sdk import capture_message, set_context, add_breadcrumb
import functools

def track_performance(threshold_seconds=1.0):
    """Decorator to track slow function performance"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                if duration > threshold_seconds:
                    capture_message(
                        f"Slow function: {func.__name__} took {duration:.2f}s",
                        level='warning'
                    )
                
                return result
            except Exception as e:
                # Add context before re-raising
                set_context('function_context', {
                    'function_name': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs),
                    'duration': time.time() - start_time,
                })
                raise
        return wrapper
    return decorator

class SentryContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add breadcrumb for each request
        add_breadcrumb(
            message=f"{request.method} {request.path}",
            category='request',
            level='info',
        )
        
        response = self.get_response(request)
        return response
```

### 3. Django Security Best Practices

#### Security Headers y Middleware
```python
# settings.py - Security Configuration
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "*.amazonaws.com")

# Rate limiting for authentication
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 hour
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
```

#### Input Validation y Sanitization
```python
# validators.py
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import re

class SecurityValidator:
    @staticmethod
    def validate_no_script_tags(value):
        """Prevent XSS through script injection"""
        if '<script' in value.lower() or 'javascript:' in value.lower():
            raise ValidationError('Script tags are not allowed')
        return value
    
    @staticmethod
    def validate_sql_injection(value):
        """Basic SQL injection prevention"""
        sql_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(--|#|/\*|\*/)',
            r'(\b(or|and)\s+\d+\s*=\s*\d+)',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                raise ValidationError('Invalid characters detected')
        return value
    
    @staticmethod
    def sanitize_html_input(value):
        """Clean HTML input"""
        # Strip dangerous tags
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form']
        for tag in dangerous_tags:
            value = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', value, flags=re.IGNORECASE)
        
        return value

# Secure serializer with validation
class SecurePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,
        validators=[SecurityValidator.validate_no_script_tags]
    )
    content = serializers.CharField(
        validators=[SecurityValidator.validate_no_script_tags]
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt']
    
    def validate_content(self, value):
        # Additional content validation
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content too short")
        
        # Sanitize HTML
        return SecurityValidator.sanitize_html_input(value)
```

### 4. Authentication Security

#### Secure JWT Implementation
```python
# authentication.py - Production JWT Security
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import User
import logging

security_logger = logging.getLogger('security')

class SecureJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Log authentication attempts
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            # Log successful authentication
            security_logger.info("Successful JWT authentication", extra={
                'user_id': user.id,
                'ip_address': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            })
            
            return (user, validated_token)
            
        except TokenError as e:
            # Log failed authentication attempts
            security_logger.warning("Failed JWT authentication", extra={
                'error': str(e),
                'ip_address': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'token_preview': str(raw_token)[:20] + '...' if raw_token else None,
            })
            raise InvalidToken(e)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

# Two-Factor Authentication Integration
class TwoFactorMixin:
    def verify_2fa(self, user, token):
        """Verify TOTP token"""
        import pyotp
        
        if not hasattr(user, 'profile') or not user.profile.totp_secret:
            return False
        
        totp = pyotp.TOTP(user.profile.totp_secret)
        return totp.verify(token, valid_window=1)
    
    def require_2fa(self, request):
        """Check if 2FA is required and verified"""
        if not request.user.is_authenticated:
            return False
        
        # Require 2FA for admin actions
        if request.user.is_staff and not request.session.get('2fa_verified'):
            return True
        
        return False
```

---

## 🔧 HORA 2: IMPLEMENTACIÓN PRÁCTICA

### 1. Comprehensive Monitoring System

#### Health Check Endpoints
```python
# health_checks.py
from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import redis
import time

class HealthCheckManager:
    @staticmethod
    def check_database():
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            duration = time.time() - start_time
            return {
                'status': 'healthy',
                'response_time': round(duration * 1000, 2),  # ms
                'message': 'Database connection OK'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': 'Database connection failed'
            }
    
    @staticmethod
    def check_cache():
        """Check Redis cache connectivity"""
        try:
            start_time = time.time()
            test_key = 'health_check_test'
            cache.set(test_key, 'test_value', timeout=10)
            result = cache.get(test_key)
            cache.delete(test_key)
            
            duration = time.time() - start_time
            
            if result == 'test_value':
                return {
                    'status': 'healthy',
                    'response_time': round(duration * 1000, 2),
                    'message': 'Cache connection OK'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': 'Cache read/write failed'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'message': 'Cache connection failed'
            }
    
    @staticmethod
    def check_external_services():
        """Check external service dependencies"""
        import requests
        
        services = {
            'email_service': getattr(settings, 'EMAIL_SERVICE_URL', None),
            'payment_gateway': getattr(settings, 'PAYMENT_GATEWAY_URL', None),
        }
        
        results = {}
        for service_name, url in services.items():
            if url:
                try:
                    start_time = time.time()
                    response = requests.get(f"{url}/health", timeout=5)
                    duration = time.time() - start_time
                    
                    results[service_name] = {
                        'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                        'response_time': round(duration * 1000, 2),
                        'status_code': response.status_code
                    }
                except Exception as e:
                    results[service_name] = {
                        'status': 'unhealthy',
                        'error': str(e)
                    }
            else:
                results[service_name] = {'status': 'not_configured'}
        
        return results

# Health check views
@api_view(['GET'])
def health_check(request):
    """Comprehensive health check endpoint"""
    checks = {
        'database': HealthCheckManager.check_database(),
        'cache': HealthCheckManager.check_cache(),
        'external_services': HealthCheckManager.check_external_services(),
        'timestamp': timezone.now().isoformat(),
        'version': getattr(settings, 'APP_VERSION', 'unknown'),
    }
    
    # Determine overall health
    overall_status = 'healthy'
    for check_name, check_result in checks.items():
        if isinstance(check_result, dict) and check_result.get('status') == 'unhealthy':
            overall_status = 'unhealthy'
            break
        elif isinstance(check_result, dict):
            for service_status in check_result.values():
                if isinstance(service_status, dict) and service_status.get('status') == 'unhealthy':
                    overall_status = 'unhealthy'
                    break
    
    checks['overall_status'] = overall_status
    
    status_code = 200 if overall_status == 'healthy' else 503
    return Response(checks, status=status_code)

@api_view(['GET'])
def metrics(request):
    """Application metrics endpoint"""
    from django.db.models import Count, Avg
    
    metrics_data = {
        'posts': {
            'total': Post.objects.count(),
            'published': Post.objects.filter(status='published').count(),
            'draft': Post.objects.filter(status='draft').count(),
        },
        'users': {
            'total': User.objects.count(),
            'active_last_30_days': User.objects.filter(
                last_login__gte=timezone.now() - timedelta(days=30)
            ).count(),
        },
        'performance': {
            'avg_response_time': get_avg_response_time(),
            'cache_hit_rate': get_cache_hit_rate(),
        }
    }
    
    return Response(metrics_data)
```

### 2. Advanced Error Tracking

#### Custom Error Handling
```python
# error_handlers.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sentry_sdk import capture_exception
import json
import logging

error_logger = logging.getLogger('django')

def custom_404_handler(request, exception):
    """Custom 404 handler with logging"""
    error_logger.warning("404 Error", extra={
        'path': request.path,
        'method': request.method,
        'ip_address': get_client_ip(request),
        'user_id': request.user.id if request.user.is_authenticated else None,
        'referer': request.META.get('HTTP_REFERER', ''),
    })
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Resource not found',
            'status_code': 404,
            'path': request.path
        }, status=404)
    
    return render(request, '404.html', status=404)

def custom_500_handler(request):
    """Custom 500 handler with error tracking"""
    error_logger.error("500 Error", extra={
        'path': request.path,
        'method': request.method,
        'ip_address': get_client_ip(request),
        'user_id': request.user.id if request.user.is_authenticated else None,
    })
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal server error',
            'status_code': 500,
            'message': 'Something went wrong. Our team has been notified.'
        }, status=500)
    
    return render(request, '500.html', status=500)

# Exception handling decorator
def handle_api_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return JsonResponse({
                'error': 'Validation error',
                'details': e.message_dict if hasattr(e, 'message_dict') else str(e)
            }, status=400)
        except PermissionDenied as e:
            return JsonResponse({
                'error': 'Permission denied',
                'message': str(e)
            }, status=403)
        except Exception as e:
            # Log unexpected errors
            capture_exception(e)
            error_logger.exception("Unexpected API error")
            
            return JsonResponse({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }, status=500)
    return wrapper
```

### 3. Production Security Implementation

#### API Security Middleware
```python
# security_middleware.py
import hashlib
import hmac
import time
from django.http import JsonResponse
from django.conf import settings

class APISecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.security_logger = logging.getLogger('security')
    
    def __call__(self, request):
        # Rate limiting check
        if self.is_rate_limited(request):
            self.security_logger.warning("Rate limit exceeded", extra={
                'ip_address': self.get_client_ip(request),
                'path': request.path,
            })
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'retry_after': 60
            }, status=429)
        
        # API signature verification for webhooks
        if request.path.startswith('/webhooks/'):
            if not self.verify_webhook_signature(request):
                self.security_logger.error("Invalid webhook signature", extra={
                    'path': request.path,
                    'ip_address': self.get_client_ip(request),
                })
                return JsonResponse({'error': 'Invalid signature'}, status=401)
        
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    def is_rate_limited(self, request):
        """Implement custom rate limiting"""
        ip = self.get_client_ip(request)
        cache_key = f'rate_limit_{ip}'
        
        current_requests = cache.get(cache_key, 0)
        if current_requests >= 100:  # 100 requests per minute
            return True
        
        cache.set(cache_key, current_requests + 1, timeout=60)
        return False
    
    def verify_webhook_signature(self, request):
        """Verify webhook signature"""
        signature = request.META.get('HTTP_X_SIGNATURE_256')
        if not signature:
            return False
        
        secret = settings.WEBHOOK_SECRET
        body = request.body
        
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, f"sha256={expected_signature}")
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
```

### 4. Monitoring Dashboard Implementation

#### Real-time Metrics Collection
```python
# metrics.py
from django.core.cache import cache
from django.db.models import Count, Avg
from datetime import datetime, timedelta
import time

class MetricsCollector:
    @staticmethod
    def collect_api_metrics():
        """Collect API performance metrics"""
        now = timezone.now()
        hour_ago = now - timedelta(hours=1)
        
        # Get from cache or calculate
        cache_key = 'api_metrics_hourly'
        metrics = cache.get(cache_key)
        
        if metrics is None:
            # Sample metrics - in production, you'd collect these from logs
            metrics = {
                'requests_per_hour': 1250,
                'avg_response_time': 0.245,
                'error_rate': 0.02,
                'active_users': User.objects.filter(
                    last_login__gte=hour_ago
                ).count(),
                'top_endpoints': [
                    {'path': '/api/v1/posts/', 'count': 450, 'avg_time': 0.180},
                    {'path': '/api/v1/posts/{id}/', 'count': 320, 'avg_time': 0.290},
                    {'path': '/api/v1/comments/', 'count': 180, 'avg_time': 0.150},
                ],
                'timestamp': now.isoformat(),
            }
            
            cache.set(cache_key, metrics, timeout=300)  # 5 minutes
        
        return metrics
    
    @staticmethod
    def collect_database_metrics():
        """Collect database performance metrics"""
        cache_key = 'db_metrics'
        metrics = cache.get(cache_key)
        
        if metrics is None:
            # Database statistics
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        n_tup_ins as inserts,
                        n_tup_upd as updates,
                        n_tup_del as deletes,
                        seq_scan as sequential_scans,
                        idx_scan as index_scans
                    FROM pg_stat_user_tables 
                    ORDER BY (n_tup_ins + n_tup_upd + n_tup_del) DESC 
                    LIMIT 10
                """)
                
                db_stats = cursor.fetchall()
            
            metrics = {
                'connection_count': len(connection.queries),
                'table_stats': [
                    {
                        'table': f"{row[0]}.{row[1]}",
                        'inserts': row[2],
                        'updates': row[3],
                        'deletes': row[4],
                        'seq_scans': row[5],
                        'idx_scans': row[6],
                    }
                    for row in db_stats
                ],
                'timestamp': timezone.now().isoformat(),
            }
            
            cache.set(cache_key, metrics, timeout=600)  # 10 minutes
        
        return metrics

# API endpoints for monitoring
@api_view(['GET'])
@permission_classes([IsAdminUser])
def system_metrics(request):
    """System health and performance metrics"""
    metrics = {
        'api': MetricsCollector.collect_api_metrics(),
        'database': MetricsCollector.collect_database_metrics(),
        'cache': {
            'hit_rate': get_cache_hit_rate(),
            'memory_usage': get_cache_memory_usage(),
        },
        'system': {
            'uptime': get_system_uptime(),
            'memory_usage': get_memory_usage(),
            'cpu_usage': get_cpu_usage(),
        }
    }
    
    return Response(metrics)

def get_cache_hit_rate():
    """Calculate cache hit rate from Redis"""
    try:
        import redis
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        info = r.info()
        
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        
        if total == 0:
            return 0
        
        return round((hits / total) * 100, 2)
    except:
        return None
```

### 2. Security Audit Implementation

#### Security Scanning Utilities
```python
# security_audit.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings