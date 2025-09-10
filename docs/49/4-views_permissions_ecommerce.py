# utils/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los dueños editar objetos.
    """
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura para cualquier request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permisos de escritura solo para el dueño del objeto
        return obj.created_by == request.user

class IsOwner(permissions.BasePermission):
    """
    Permiso que solo permite acceso al dueño del objeto.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# apps/authentication/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from .models import User

class UserRegistrationView(CreateAPIView):
    """Vista para registro de usuarios"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Vista para login de usuarios"""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    
    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

class UserProfileView(RetrieveUpdateAPIView):
    """Vista para ver y actualizar perfil de usuario"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


# apps/products/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer, 
    ProductReviewSerializer
)
from utils.permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet para productos"""
    queryset = Product.objects.filter(is_active=True).select_related(
        'category', 'created_by'
    ).prefetch_related('reviews')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por rango de precio
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, slug=None):
        """Agregar reseña a un producto"""
        product = self.get_object()
        
        # Verificar si ya existe una reseña del usuario
        existing_review = ProductReview.objects.filter(
            product=product, user=request.user
        ).first()
        
        if existing_review:
            return Response(
                {'detail': 'You have already reviewed this product'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Productos destacados (con mejor rating)"""
        products = self.get_queryset().annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=4.0).order_by('-avg_rating')[:10]
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


# apps/orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, Cart, CartItem
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    CartSerializer, CartItemSerializer
)
from apps.products.models import Product
from utils.permissions import IsOwner

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet para pedidos"""
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product'
        )
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Actualizar estado del pedido (solo para admin/staff)"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'detail': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        return Response({'status': order.status})

class CartViewSet(viewsets.ViewSet):
    """ViewSet para el carrito de compras"""
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Obtener carrito del usuario"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Agregar item al carrito"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar stock
        if quantity > product.stock:
            return Response(
                {'detail': f'Not enough stock. Available: {product.stock}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar o crear item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return Response(
                    {'detail': f'Not enough stock. Available: {product.stock}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        
        return Response(
            CartItemSerializer(cart_item).data, 
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        """Actualizar cantidad de item en carrito"""
        cart = get_object_or_404(Cart, user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        
        if quantity <= 0:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # Verificar stock
        if quantity > cart_item.product.stock:
            return Response(
                {'detail': f'Not enough stock. Available: {cart_item.product.stock}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Remover item del carrito"""
        cart = get_object_or_404(Cart, user=request.user)
        product_id = request.data.get('product_id')
        
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Limpiar todo el carrito"""
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)