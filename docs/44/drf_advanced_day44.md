# DRF Advanced - Día 44: Authentication, Permissions & Throttling

## 🎯 Objetivos del Día
- Implementar JWT authentication completo
- Crear custom permissions complejos
- Configurar throttling strategies
- Dominar API versioning y filtering
- Prepararse para preguntas senior sobre arquitectura de APIs

---

## 📚 HORA 1: TEORÍA AVANZADA

### 1. Authentication Deep Dive

#### JWT vs Session vs Token Authentication
```python
# settings.py - Multiple Authentication Classes
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Custom JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

#### Custom Authentication Backend
```python
# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth.models import User

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except (jwt.ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token')
            
    def authenticate_header(self, request):
        return 'Bearer'
```

### 2. Advanced Permissions System

#### Custom Permission Classes
```python
# permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions only to owner
        return obj.owner == request.user

class IsAuthorOrModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Edit if owner or moderator
        return (obj.author == request.user or 
                request.user.groups.filter(name='moderators').exists())

class RoleBasedPermission(BasePermission):
    """Permission based on user roles"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        required_role = getattr(view, 'required_role', None)
        if not required_role:
            return True
            
        return request.user.profile.role == required_role
```

### 3. Throttling Strategies

#### Built-in Throttling Classes
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'premium': '5000/hour',
        'login': '5/min',
    }
}

# Custom Throttle Class
from rest_framework.throttling import UserRateThrottle

class PremiumUserThrottle(UserRateThrottle):
    scope = 'premium'
    
    def allow_request(self, request, view):
        if request.user.profile.is_premium:
            return super().allow_request(request, view)
        return False

class LoginThrottle(UserRateThrottle):
    scope = 'login'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
```

### 4. API Versioning Patterns

```python
# versioning.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
}

# Version-specific serializers
class PostSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']

class PostSerializerV2(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_name', 'tags', 'created_at', 'updated_at']

# Version-aware ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return PostSerializerV2
        return PostSerializerV1
```

---

## ⚡ HORA 2: IMPLEMENTACIÓN PRÁCTICA

### Proyecto: Sistema de Blog Avanzado con DRF

Vamos a crear una API REST completa que demuestre todos los conceptos avanzados:

#### 1. Modelos Base
```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES = [
        ('author', 'Author'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='author')
    is_premium = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
```

#### 2. Serializers Avanzados
```python
# serializers.py
from rest_framework import serializers
from .models import Post, Comment, Category, UserProfile

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'replies']
        
    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for top-level comments
            replies = Comment.objects.filter(parent=obj)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category_name', 
                 'status', 'created_at', 'comment_count']
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 
                 'status', 'featured', 'created_at', 'updated_at', 'comments', 'can_edit']
    
    def get_can_edit(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.author == user or user.profile.role in ['editor', 'admin']
```

#### 3. ViewSets con Permisos Complejos
```python
# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrEditorOrReadOnly, CanModerateComments

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('comments')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrEditorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'featured']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status based on user permissions
        if not self.request.user.is_authenticated:
            return queryset.filter(status='published')
        
        if self.request.user.profile.role in ['editor', 'admin']:
            return queryset  # Can see all posts
        
        # Authors can see their own posts + published posts
        return queryset.filter(
            models.Q(status='published') | models.Q(author=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_featured(self, request, pk=None):
        """Only editors and admins can feature posts"""
        if request.user.profile.role not in ['editor', 'admin']:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post = self.get_object()
        post.featured = not post.featured
        post.save()
        
        return Response({
            'featured': post.featured,
            'message': f'Post {"featured" if post.featured else "unfeatured"} successfully'
        })
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        posts = self.get_queryset().filter(author=request.user)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return self.queryset.filter(post_id=post_id, parent=None)
        return self.queryset.filter(parent=None)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[CanModerateComments])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'message': 'Comment approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[CanModerateComments])
    def reject(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        return Response({'message': 'Comment rejected'})
```

#### 4. URLs con Versionado
```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    # API v1
    path('api/v1/', include([
        path('', include(router.urls)),
        path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]
```

---

## 🧪 EJERCICIOS PRÁCTICOS

### Ejercicio 1: Custom Permission para Rate Limiting
Crear un permission que limite las acciones según el rol del usuario:
- Authors: 10 posts/day
- Editors: 50 posts/day  
- Admins: ilimitado

### Ejercicio 2: API Key Authentication
Implementar un sistema de API keys para acceso programático:
```python
class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None
        
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            return (api_key_obj.user, api_key_obj)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
```

### Ejercicio 3: Advanced Filtering
Implementar filtros complejos con Q objects:
```python
def get_queryset(self):
    queryset = super().get_queryset()
    
    # Complex filtering logic
    date_from = self.request.query_params.get('date_from')
    date_to = self.request.query_params.get('date_to')
    author_name = self.request.query_params.get('author')
    
    if date_from and date_to:
        queryset = queryset.filter(
            created_at__date__range=[date_from, date_to]
        )
    
    if author_name:
        queryset = queryset.filter(
            author__username__icontains=author_name
        )
    
    return queryset
```

---

## 📋 CHECKLIST DEL DÍA

- [ ] JWT authentication implementado correctamente
- [ ] Custom permissions creados y probados
- [ ] Throttling configurado para diferentes roles
- [ ] API versioning funcional
- [ ] Filtering y searching implementados
- [ ] Nested serializers para relaciones complejas
- [ ] Custom actions en ViewSets
- [ ] Manejo de permisos a nivel de objeto
- [ ] Tests para todos los endpoints críticos

---

## 🎯 PREGUNTAS DE ENTREVISTA TÍPICAS

### 1. Autenticación y Seguridad
**P:** "¿Cuál es la diferencia entre authentication y authorization en DRF?"
**R:** Authentication verifica la identidad del usuario (quién es), mientras que authorization determina qué puede hacer (permisos). Authentication occurs first, then authorization.

**P:** "¿Por qué elegirías JWT over session-based auth en una API?"
**R:** JWT es stateless, escalable, y funciona bien con microservicios. No requiere storage server-side y puede incluir claims personalizados.

### 2. Performance y Escalabilidad
**P:** "¿Cómo optimizarías una API que está siendo muy lenta?"
**R:** 
1. Database queries optimization (select_related, prefetch_related)
2. Pagination en large datasets  
3. Caching con Redis
4. Throttling para prevenir abuse
5. Database indexing
6. Async views donde sea apropiado

### 3. Diseño de APIs
**P:** "¿Cómo diseñarías un sistema de permisos granular?"
**R:** Combination of:
- Role-based permissions (RBAC)
- Object-level permissions
- Custom permission classes
- Groups y user permissions
- Context-aware permissions

---

## 🚀 TAREA PARA MAÑANA
Prepárate para el Día 45 estudiando:
- Django performance optimization
- Caching strategies (Redis, Memcached)
- Database query optimization
- Django Debug Toolbar
- Profiling tools

¡Excelente trabajo implementando DRF avanzado! Mañana profundizaremos en optimización de performance. 🔥