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
import re
from datetime import timedelta

class SecurityAuditor:
    def __init__(self):
        self.security_issues = []
        self.security_logger = logging.getLogger('security')
    
    def audit_user_accounts(self):
        """Audit user account security"""
        issues = []
        
        # Check for weak passwords
        weak_users = User.objects.filter(
            password__in=['password', '123456', 'admin']
        )
        if weak_users.exists():
            issues.append(f"Found {weak_users.count()} users with weak passwords")
        
        # Check for inactive admin accounts
        inactive_admins = User.objects.filter(
            is_staff=True,
            last_login__lt=timezone.now() - timedelta(days=90)
        )
        if inactive_admins.exists():
            issues.append(f"Found {inactive_admins.count()} inactive admin accounts")
        
        # Check for users without email
        users_no_email = User.objects.filter(email='')
        if users_no_email.exists():
            issues.append(f"Found {users_no_email.count()} users without email")
        
        return issues
    
    def audit_settings_security(self):
        """Audit Django settings for security issues"""
        issues = []
        
        # Check DEBUG setting
        if getattr(settings, 'DEBUG', False):
            issues.append("DEBUG is True in production")
        
        # Check SECRET_KEY
        if getattr(settings, 'SECRET_KEY', '') == 'django-insecure-default':
            issues.append("Using default SECRET_KEY")
        
        # Check ALLOWED_HOSTS
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        if '*' in allowed_hosts:
            issues.append("ALLOWED_HOSTS contains '*' - security risk")
        
        # Check SECURE settings
        security_settings = [
            'SECURE_SSL_REDIRECT',
            'SECURE_HSTS_SECONDS',
            'SESSION_COOKIE_SECURE',
            'CSRF_COOKIE_SECURE',
        ]
        
        for setting in security_settings:
            if not getattr(settings, setting, False):
                issues.append(f"{setting} is not properly configured")
        
        return issues
    
    def audit_database_permissions(self):
        """Audit database user permissions"""
        issues = []
        
        # Check for superuser database accounts
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT usename, usesuper, usecreatedb 
                FROM pg_user 
                WHERE usesuper = true OR usecreatedb = true
            """)
            
            superusers = cursor.fetchall()
            if len(superusers) > 1:  # More than just postgres user
                issues.append(f"Found {len(superusers)} database superusers")
        
        return issues
    
    def run_full_audit(self):
        """Run complete security audit"""
        audit_results = {
            'user_accounts': self.audit_user_accounts(),
            'settings': self.audit_settings_security(),
            'database': self.audit_database_permissions(),
            'timestamp': timezone.now().isoformat(),
        }
        
        # Log critical issues
        total_issues = sum(len(issues) for issues in audit_results.values() if isinstance(issues, list))
        
        if total_issues > 0:
            self.security_logger.error(f"Security audit found {total_issues} issues", extra=audit_results)
        else:
            self.security_logger.info("Security audit passed - no issues found")
        
        return audit_results

# Management command for security audit
class Command(BaseCommand):
    help = 'Run security audit'
    
    def handle(self, *args, **options):
        auditor = SecurityAuditor()
        results = auditor.run_full_audit()
        
        self.stdout.write(self.style.SUCCESS('Security Audit Results:'))
        
        for category, issues in results.items():
            if isinstance(issues, list) and issues:
                self.stdout.write(f"\n{category.upper()} ISSUES:")
                for issue in issues:
                    self.stdout.write(f"  ⚠️  {issue}")
            elif isinstance(issues, list):
                self.stdout.write(f"\n{category.upper()}: ✅ No issues found")
        
        total_issues = sum(len(issues) for issues in results.values() if isinstance(issues, list))
        
        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS('\n🎉 Security audit passed!'))
        else:
            self.stdout.write(self.style.ERROR(f'\n❌ Found {total_issues} security issues'))
```

### 3. Performance Monitoring Dashboard

#### Real-time Performance Tracking
```python
# performance_dashboard.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
import psutil
import time

@staff_member_required
def performance_dashboard(request):
    """Admin dashboard for performance monitoring"""
    context = {
        'title': 'Performance Dashboard',
        'metrics_endpoint': '/admin/api/metrics/',
    }
    return render(request, 'admin/performance_dashboard.html', context)

@staff_member_required
def real_time_metrics(request):
    """Real-time metrics API for dashboard"""
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Django metrics
    django_metrics = {
        'active_connections': len(connection.queries),
        'cache_stats': get_detailed_cache_stats(),
        'recent_errors': get_recent_errors(),
        'slow_queries': get_slow_queries(),
    }
    
    # Application metrics
    app_metrics = {
        'active_users': get_active_users_count(),
        'api_requests_last_hour': get_api_requests_count(),
        'average_response_time': get_average_response_time(),
        'error_rate': get_error_rate(),
    }
    
    metrics = {
        'system': {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_percent': round((disk.used / disk.total) * 100, 2),
            'disk_free_gb': round(disk.free / (1024**3), 2),
        },
        'django': django_metrics,
        'application': app_metrics,
        'timestamp': time.time(),
    }
    
    return JsonResponse(metrics)

def get_detailed_cache_stats():
    """Get detailed cache statistics"""
    try:
        import redis
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        info = r.info()
        
        return {
            'hits': info.get('keyspace_hits', 0),
            'misses': info.get('keyspace_misses', 0),
            'keys': r.dbsize(),
            'memory_usage_mb': round(info.get('used_memory', 0) / (1024**2), 2),
            'connected_clients': info.get('connected_clients', 0),
        }
    except:
        return {'error': 'Cannot connect to Redis'}

def get_slow_queries():
    """Get recent slow queries from logs"""
    # In production, you'd parse logs or use a monitoring tool
    return [
        {
            'query': 'SELECT * FROM blog_post WHERE...',
            'duration': 2.3,
            'timestamp': '2025-08-30T10:30:00Z'
        }
    ]
```

---

## 🧪 EJERCICIOS PRÁCTICOS AVANZADOS

### Ejercicio 1: Performance Regression Detection
```python
# Create a system that detects performance regressions
class PerformanceBaseline:
    def __init__(self):
        self.baseline_file = 'performance_baseline.json'
    
    def record_baseline(self, endpoint, response_time):
        """Record performance baseline for endpoint"""
        # Your implementation here
        pass
    
    def check_regression(self, endpoint, current_time):
        """Check if current performance is significantly worse than baseline"""
        # Your implementation here
        # Alert if performance is >50% worse than baseline
        pass

# Task: Implement complete regression detection system
```

### Ejercicio 2: Custom Metrics Collection
```python
# Implement custom business metrics
def track_business_metrics():
    """Track important business KPIs"""
    metrics = {
        'daily_active_users': None,  # Implement
        'content_engagement_rate': None,  # Implement
        'api_adoption_rate': None,  # Implement
        'user_retention_rate': None,  # Implement
    }
    
    # Your task: Implement each metric calculation
    # Store in time-series database (Redis Streams or InfluxDB)
    return metrics
```

### Ejercicio 3: Security Event Response
```python
# Implement automated security response
class SecurityEventHandler:
    def handle_brute_force_attack(self, ip_address, failed_attempts):
        """Handle detected brute force attack"""
        # Your implementation:
        # 1. Block IP temporarily
        # 2. Send alert to admins
        # 3. Log incident
        # 4. Update monitoring dashboard
        pass
    
    def handle_sql_injection_attempt(self, request_data):
        """Handle detected SQL injection attempt"""
        # Your implementation:
        # 1. Block request immediately
        # 2. Log full request details
        # 3. Alert security team
        # 4. Add IP to watchlist
        pass
```

---

## 📋 PRODUCTION READINESS CHECKLIST

### Security Checklist:
- [ ] **HTTPS Configuration**: SSL certificates, HSTS headers
- [ ] **Authentication Security**: Strong password policies, 2FA option
- [ ] **Input Validation**: XSS protection, SQL injection prevention
- [ ] **Rate Limiting**: API rate limits, brute force protection
- [ ] **Security Headers**: CSP, X-Frame-Options, etc.
- [ ] **Dependency Security**: Regular security updates
- [ ] **Access Control**: Proper permissions, least privilege principle

### Monitoring Checklist:
- [ ] **Error Tracking**: Sentry integration, alert configuration
- [ ] **Performance Monitoring**: Response times, query analysis
- [ ] **Health Checks**: Database, cache, external services
- [ ] **Business Metrics**: User engagement, API usage
- [ ] **Alerting**: Critical error alerts, performance thresholds
- [ ] **Dashboards**: Real-time monitoring interface

### Logging Checklist:
- [ ] **Structured Logging**: JSON format, consistent fields
- [ ] **Log Levels**: Appropriate use of DEBUG, INFO, WARNING, ERROR
- [ ] **Log Rotation**: Size limits, backup retention
- [ ] **Sensitive Data**: No passwords, tokens in logs
- [ ] **Correlation IDs**: Request tracking across services
- [ ] **Performance Logs**: Slow query logging, response times

---

## 🎯 PREGUNTAS DE ENTREVISTA - PRODUCTION

### 1. Monitoring Strategy
**P:** "¿Cómo monitorearías una aplicación Django en producción?"

**R:** Stack completo:
1. **Application Monitoring**: Sentry para errors y performance
2. **Infrastructure Monitoring**: Prometheus + Grafana para métricas de sistema
3. **Log Aggregation**: ELK stack o similar para centralized logging
4. **Health Checks**: Automated endpoints para service health
5. **Alerting**: PagerDuty o similar para critical incidents
6. **Business Metrics**: Custom dashboards para KPIs

### 2. Security Response
**P:** "Te reportan un security incident en producción. ¿Cuáles son tus primeros pasos?"

**R:** Incident Response Protocol:
1. **Assess**: Determinar scope y severity
2. **Contain**: Block attack vectors, isolate affected systems
3. **Document**: Log all actions y evidence
4. **Communicate**: Notify stakeholders apropiadamente
5. **Investigate**: Root cause analysis
6. **Remediate**: Fix vulnerabilities, update security measures
7. **Review**: Post-incident review y prevention measures

### 3. Performance Under Load
**P:** "Tu API está cayendo bajo high load. ¿Cómo la estabilizarías?"

**R:** Emergency Response:
1. **Immediate**: Enable aggressive caching, increase timeouts
2. **Scale Horizontally**: Add more application servers
3. **Database**: Enable read replicas, connection pooling
4. **Load Balancing**: Distribute traffic effectively
5. **Rate Limiting**: Protect against abuse
6. **Background Tasks**: Move heavy operations to Celery
7. **Monitor**: Watch metrics closely durante recovery

---

## 📊 PROYECTO FINAL DEL DÍA

### Production Monitoring Stack
Implementar un sistema completo que incluya:

1. **Real-time Dashboard**: Métricas de sistema y aplicación
2. **Alert System**: Notificaciones automáticas para issues críticos
3. **Security Monitoring**: Detection de suspicious activity
4. **Performance Tracking**: Baseline comparison y regression detection
5. **Health Check Suite**: Comprehensive service monitoring

### Entregables:
- [ ] Dashboard funcional con real-time metrics
- [ ] Sentry integration completa con custom tags
- [ ] Security audit script que detecte vulnerabilities
- [ ] Automated alerting para critical thresholds
- [ ] Performance baseline y regression detection

---

## 🔒 SECURITY BEST PRACTICES SUMMARY

### Input Validation:
```python
# Always validate and sanitize user input
def secure_input_validator(value):
    # Remove dangerous characters
    cleaned = re.sub(r'[<>"\']', '', value)
    
    # Check length limits
    if len(cleaned) > 1000:
        raise ValidationError("Input too long")
    
    # Check for SQL injection patterns
    sql_patterns = ['union', 'select', 'drop', 'delete', 'insert']
    if any(pattern in cleaned.lower() for pattern in sql_patterns):
        raise ValidationError("Invalid input detected")
    
    return cleaned
```

### Authentication Security:
```python
# Secure authentication practices
class SecureAuthenticationView(APIView):
    throttle_classes = [LoginThrottle]  # Rate limiting
    
    def post(self, request):
        # Log authentication attempt
        security_logger.info("Authentication attempt", extra={
            'ip_address': get_client_ip(request),
            'username': request.data.get('username', ''),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        })
        
        # Validate input
        username = secure_input_validator(request.data.get('username', ''))
        password = request.data.get('password', '')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            # Success logging
            security_logger.info("Authentication successful", extra={
                'user_id': user.id,
                'ip_address': get_client_ip(request),
            })
            
            # Generate secure token
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        else:
            # Failed attempt logging
            security_logger.warning("Authentication failed", extra={
                'username': username,
                'ip_address': get_client_ip(request),
            })
            
            return Response({
                'error': 'Invalid credentials'
            }, status=401)
```

---

## 🚀 TAREA PARA MAÑANA - DÍA 47

**Día 47: Production Deployment**
Prepárate estudiando:
- Docker multi-stage builds para Django
- CI/CD pipelines con GitHub Actions
- Database migrations en production
- Zero-downtime deployment strategies
- Infrastructure as Code (Terraform basics)

### Pre-study Resources:
- Django deployment checklist oficial
- Docker best practices para Python apps
- Kubernetes basics para container orchestration
- Cloud provider documentation (AWS/GCP/Azure)

---

## 💪 LO QUE HAS LOGRADO HOY

### Technical Skills:
- ✅ **Advanced Logging**: Structured logging con correlation IDs
- ✅ **Error Tracking**: Sentry integration completa con custom context
- ✅ **Security Auditing**: Automated security scanning y validation
- ✅ **Performance Monitoring**: Real-time metrics y alerting
- ✅ **Production Readiness**: Comprehensive health checks y monitoring

### Interview Preparation:
- ✅ **Production Experience**: Hands-on con production-grade tools
- ✅ **Security Awareness**: Understanding de common vulnerabilities
- ✅ **Monitoring Strategy**: Complete observability stack knowledge
- ✅ **Incident Response**: Structured approach para handling issues

### Portfolio Addition:
Tu monitoring dashboard y security audit system demuestran:
- **DevOps Knowledge**: Understanding de production operations
- **Security Mindset**: Proactive security measures
- **Observability**: Complete application monitoring
- **Reliability Engineering**: Production-ready applications

¡Estás desarrollando exactamente las skills que buscan en roles senior! El monitoring y security son diferenciadores clave. ¡Mañana cerramos con deployment strategies! 🚀🔒📊