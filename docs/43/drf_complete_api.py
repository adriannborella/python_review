# blog/serializers.py - Serializers completos
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Post, Category, Comment, Tag, PostLike, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'website', 'twitter', 'github']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    posts_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'profile', 'posts_count', 'date_joined'
        ]
        extra_kwargs = {
            'email': {'write_only': True},
            'date_joined': {'read_only': True}
        }
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'slug']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()

class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'posts_count']
        read_only_fields = ['slug']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'created_at', 'updated_at',
            'active', 'parent', 'replies', 'is_reply'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'active']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(active=True),
                many=True,
                context=self.context
            ).data
        return []
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    excerpt_generated = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'excerpt_generated',
            'author', 'category', 'tags', 'status', 'featured_image',
            'views_count', 'likes_count', 'comments_count',
            'read_time', 'created_at', 'updated_at'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.filter(active=True).count()
    
    def get_excerpt_generated(self, obj):
        if obj.excerpt:
            return obj.excerpt
        return obj.content[:300] + '...' if len(obj.content) > 300 else obj.content
    
    def get_read_time(self, obj):
        words = len(obj.content.split())
        return max(1, round(words / 200))  # 200 palabras por minuto

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'author', 'slug', 'created_at', 'updated_at',
            'views_count', 'likes_count'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.filter(active=True).count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_read_time(self, obj):
        words = len(obj.content.split())
        return max(1, round(words / 200))
    
    def get_related_posts(self, obj):
        related = Post.objects.filter(
            category=obj.category,
            status='published'
        ).exclude(pk=obj.pk)[:3]
        
        return PostListSerializer(related, many=True, context=self.context).data
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        
        if tags_data:
            # Actualizar tags
            tag_objects = []
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    name=tag_data['name'],
                    defaults={'slug': tag_data['name'].lower().replace(' ', '-')}
                )
                tag_objects.append(tag)
            instance.tags.set(tag_objects)
        
        return instance

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category',
            'status', 'featured_image', 'tags'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user
        
        post = super().create(validated_data)
        
        # Procesar tags
        if tags_data:
            tag_objects = []
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.strip(),
                    defaults={'slug': tag_name.strip().lower().replace(' ', '-')}
                )
                tag_objects.append(tag)
            post.tags.set(tag_objects)
        
        return post

# blog/viewsets.py - ViewSets completos
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly
from .serializers import *
from .models import *

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para usuarios (solo lectura)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Actualizar perfil del usuario"""
        user = request.user
        profile = user.profile
        
        # Actualizar datos del usuario
        user_data = {
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
        }
        
        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()
        
        # Actualizar perfil
        profile_data = {
            'bio': request.data.get('bio', profile.bio),
            'website': request.data.get('website', profile.website),
            'twitter': request.data.get('twitter', profile.twitter),
            'github': request.data.get('github', profile.github),
        }
        
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        )
        return queryset

class TagViewSet(viewsets.ModelViewSet):
    """ViewSet para tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Obtener tags más populares"""
        tags = Tag.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(posts_count__gt=0).order_by('-posts_count')[:20]
        
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet principal para posts"""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status', 'tags']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category')\
                              .prefetch_related('tags', 'comments')
        
        if self.action == 'list':
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve para incrementar vistas"""
        instance = self.get_object()
        
        # Incrementar vistas solo si no es el autor
        if request.user != instance.author:
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Toggle like en un post"""
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        # Actualizar contador
        post.likes_count = post.likes.count()
        post.save(update_fields=['likes_count'])
        
        return Response({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Obtener comentarios de un post"""
        post = self.get_object()
        comments = post.comments.filter(active=True, parent=None)\
                              .select_related('author')\
                              .prefetch_related('replies__author')\
                              .order_by('created_at')
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Agregar comentario a un post"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    """API para logout (eliminar token)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logged out successfully'}, 
                          status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Error during logout'}, 
                          status=status.HTTP_400_BAD_REQUEST)

class SearchAPIView(APIView):
    """API de búsqueda avanzada"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category')
        author = request.query_params.get('author')
        tags = request.query_params.getlist('tags')
        
        posts = Post.objects.filter(status='published')\
                           .select_related('author', 'category')\
                           .prefetch_related('tags')
        
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        
        if category:
            posts = posts.filter(category__slug=category)
        
        if author:
            posts = posts.filter(author__username=author)
        
        if tags:
            posts = posts.filter(tags__slug__in=tags).distinct()
        
        # Ordenar por relevancia
        posts = posts.order_by('-created_at')
        
        # Paginación manual
        page_size = min(int(request.query_params.get('page_size', 10)), 50)
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = posts.count()
        posts_page = posts[start:end]
        
        serializer = PostListSerializer(posts_page, many=True, context={'request': request})
        
        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'results': serializer.data
        })

class BlogStatsAPIView(APIView):
    """API de estadísticas del blog"""
    
    def get(self, request):
        from datetime import timedelta
        from django.utils import timezone
        
        last_week = timezone.now() - timedelta(days=7)
        last_month = timezone.now() - timedelta(days=30)
        
        stats = {
            'total_posts': Post.objects.filter(status='published').count(),
            'total_authors': User.objects.filter(posts__status='published').distinct().count(),
            'total_categories': Category.objects.count(),
            'total_comments': Comment.objects.filter(active=True).count(),
            'posts_this_week': Post.objects.filter(
                status='published',
                created_at__gte=last_week
            ).count(),
            'posts_this_month': Post.objects.filter(
                status='published',
                created_at__gte=last_month
            ).count(),
        }
        
        # Top categorías
        top_categories = Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(posts_count__gt=0).order_by('-posts_count')[:5]
        
        # Top autores
        top_authors = User.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(posts_count__gt=0).order_by('-posts_count')[:5]
        
        stats.update({
            'top_categories': [
                {'name': cat.name, 'posts_count': cat.posts_count}
                for cat in top_categories
            ],
            'top_authors': [
                {'username': user.username, 'posts_count': user.posts_count}
                for user in top_authors
            ]
        })
        
        return Response(stats)

# blog/permissions.py - Permisos personalizados completos
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Solo el autor puede modificar el objeto"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Solo el propietario puede modificar el objeto"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Buscar campo de usuario (user, author, owner)
        owner_field = getattr(obj, 'user', getattr(obj, 'author', 
                            getattr(obj, 'owner', None)))
        return owner_field == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """Solo admin puede modificar, todos pueden leer"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CanModerateComments(permissions.BasePermission):
    """Permiso para moderar comentarios"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or 
            request.user.groups.filter(name='Moderators').exists()
        )

# blog/authentication.py - Autenticación personalizada
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class ExpiringTokenAuthentication(TokenAuthentication):
    """Token con expiración"""
    
    def authenticate_credentials(self, key):
        from datetime import timedelta
        from django.utils import timezone
        
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')
        
        # Verificar expiración (7 días)
        if token.created < timezone.now() - timedelta(days=7):
            token.delete()
            raise AuthenticationFailed('Token expired')
        
        return (token.user, token)

# blog/throttling.py - Rate limiting
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class PostCreateRateThrottle(UserRateThrottle):
    scope = 'post_create'

class CommentCreateRateThrottle(UserRateThrottle):
    scope = 'comment_create'

class SearchRateThrottle(AnonRateThrottle):
    scope = 'search'

# blog/renderers.py - Renderizadores personalizados
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json

class CustomJSONRenderer(JSONRenderer):
    """Renderer JSON personalizado con metadatos"""
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context and renderer_context['response'].status_code >= 400:
            # Formato de error consistente
            custom_data = {
                'error': True,
                'message': data.get('detail', 'Error occurred'),
                'data': data
            }
        else:
            # Formato de éxito
            custom_data = {
                'success': True,
                'data': data,
                'timestamp': json.datetime.datetime.now().isoformat()
            }
        
        return super().render(custom_data, accepted_media_type, renderer_context)

# blog/exceptions.py - Manejo de excepciones
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Manejador personalizado de excepciones"""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log del error
        logger.error(f"API Error: {exc}", exc_info=True, extra={'context': context})
        
        # Respuesta personalizada
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'status_code': response.status_code,
            'details': response.data
        }
        
        response.data = custom_response_data
    
    return response

# settings.py - Configuración de DRF
"""
# Agregar a INSTALLED_APPS
INSTALLED_APPS = [
    # ... otras apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',  # Para CORS si tienes frontend separado
]

# Configuración de DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'blog.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'blog.renderers.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'blog.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'post_create': '10/day',
        'comment_create': '50/day',
        'search': '200/hour'
    },
    'EXCEPTION_HANDLER': 'blog.exceptions.custom_exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
}

# CORS (si tienes frontend separado)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
"""

# blog/tests/test_api.py - Tests para la API
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from blog.models import Post, Category, Comment
import json

class BlogAPITest(APITestCase):
    """Tests para la API del blog"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Crear usuarios
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        # Crear tokens
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        
        # Crear datos de prueba
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def authenticate(self, user='default'):
        """Helper para autenticar usuarios"""
        token = self.token if user == 'default' else self.other_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    def test_user_registration(self):
        """Test registro de usuario"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_login(self):
        """Test login con token"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_post_list(self):
        """Test obtener lista de posts"""
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post')
    
    def test_post_detail(self):
        """Test obtener detalle de post"""
        response = self.client.get(f'/api/v1/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertIn('related_posts', response.data)
    
    def test_post_create_requires_auth(self):
        """Test que crear post requiere autenticación"""
        data = {
            'title': 'New Post',
            'content': 'New content',
            'category': self.category.id,
            'status': 'published'
        }
        
        response = self.client.post('/api/v1/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_post_create_authenticated(self):
        """Test crear post autenticado"""
        self.authenticate()
        
        data = {
            'title': 'New Post',
            'content': 'New content',
            'category': self.category.id,
            'status': 'published',
            'tags': ['python', 'django']
        }
        
        response = self.client.post('/api/v1/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(title='New Post').exists())
    
    def test_post_update_authorization(self):
        """Test que solo el autor puede actualizar"""
        self.authenticate('other')  # Usuario diferente
        
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/v1/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_like(self):
        """Test dar like a un post"""
        self.authenticate()
        
        response = self.client.post(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])
        self.assertEqual(response.data['likes_count'], 1)
        
        # Toggle unlike
        response = self.client.post(f'/api/v1/posts/{self.post.id}/like/')
        self.assertFalse(response.data['liked'])
        self.assertEqual(response.data['likes_count'], 0)
    
    def test_comment_creation(self):
        """Test crear comentario"""
        self.authenticate()
        
        data = {
            'content': 'Great post!',
            'post': self.post.id
        }
        
        response = self.client.post('/api/v1/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content='Great post!').exists())
    
    def test_search_api(self):
        """Test API de búsqueda"""
        response = self.client.get('/api/v1/search/?q=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_pagination(self):
        """Test paginación"""
        # Crear más posts
        for i in range(15):
            Post.objects.create(
                title=f'Post {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category,
                status='published'
            )
        
        response = self.client.get('/api/v1/posts/?page_size=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['links']['next'])
    
    def test_filtering(self):
        """Test filtros"""
        # Crear post en diferente categoría
        other_category = Category.objects.create(name='Other', slug='other')
        Post.objects.create(
            title='Other Post',
            content='Other content',
            author=self.user,
            category=other_category,
            status='published'
        )
        
        response = self.client.get(f'/api/v1/posts/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_api_versioning(self):
        """Test versionado de API"""
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_rate_limiting(self):
        """Test rate limiting (requiere configuración específica)"""
        # Este test requeriría configurar el throttling para tests
        pass

class APIDocumentationTest(APITestCase):
    """Tests para documentación de API"""
    
    def test_api_root_accessible(self):
        """Test que la raíz de la API sea accesible"""
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_options_requests(self):
        """Test requests OPTIONS para CORS"""
        response = self.client.options('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Allow', response)

# blog/docs.py - Documentación automática con drf-spectacular
"""
# Instalar: pip install drf-spectacular

# En settings.py:
INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    # ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'API REST completa para el sistema de blog',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
}

# En urls.py del proyecto:
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
"""_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtener posts destacados"""
        posts = Post.objects.filter(status='published')\
                           .annotate(
                               popularity=Count('comments') + Count('likes')
                           )\
                           .order_by('-popularity')[:6]
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Obtener posts por categoría"""
        category_slug = request.query_params.get('slug')
        if not category_slug:
            return Response({'error': 'Se requiere parámetro slug'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(slug=category_slug)
            posts = self.get_queryset().filter(category=category)
            
            page = self.paginate_queryset(posts)
            if page is not None:
                serializer = PostListSerializer(page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
            
            serializer = PostListSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data)
            
        except Category.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet para comentarios"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Comment.objects.filter(active=True)\
                             .select_related('author', 'post')\
                             .prefetch_related('replies__author')
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = Post.objects.get(id=post_id, status='published')
        serializer.save(post=post)

# blog/pagination.py - Paginación personalizada
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })

# blog/filters.py - Filtros personalizados
import django_filters
from .models import Post, Comment

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_views = django_filters.NumberFilter(field_name='views_count', lookup_expr='gte')
    min_likes = django_filters.NumberFilter(field_name='likes_count', lookup_expr='gte')
    
    class Meta:
        model = Post
        fields = ['category', 'author', 'status', 'tags']

# blog/urls.py - URLs de la API
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import viewsets, api_views

# Router principal
router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'categories', viewsets.CategoryViewSet)
router.register(r'tags', viewsets.TagViewSet)
router.register(r'posts', viewsets.PostViewSet, basename='post')
router.register(r'comments', viewsets.CommentViewSet, basename='comment')

app_name = 'blog_api'

urlpatterns = [
    # API principal
    path('', include(router.urls)),
    
    # Autenticación
    path('auth/login/', obtain_auth_token, name='auth_login'),
    path('auth/register/', api_views.UserRegistrationAPIView.as_view(), name='auth_register'),
    path('auth/logout/', api_views.LogoutAPIView.as_view(), name='auth_logout'),
    
    # Endpoints especiales
    path('search/', api_views.SearchAPIView.as_view(), name='search'),
    path('stats/', api_views.BlogStatsAPIView.as_view(), name='stats'),
]

# blog/api_views.py - Views especiales de API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count, Q
from .serializers import UserRegistrationSerializer, PostListSerializer
from .models import Post, Category, Comment, User

class UserRegistrationAPIView(APIView):
    """API para registro de usuarios"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP