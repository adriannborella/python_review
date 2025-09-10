# apps/authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Crear perfil automáticamente
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil del usuario"""
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'country', 'postal_code', 'date_of_birth']

class UserSerializer(serializers.ModelSerializer):
    """Serializer completo del usuario"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_verified', 'profile']
        read_only_fields = ['id', 'is_verified']

class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


# apps/products/serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Category, Product, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'is_active', 'products_count']
        read_only_fields = ['id']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()

class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer para reseñas de productos"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer para lista de productos (optimizado)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'stock', 'image', 'is_active',
            'category_name', 'average_rating', 'reviews_count', 'created_at'
        ]
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()

class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para productos"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        write_only=True,
        source='category'
    )
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'slug', 'category', 'category_id',
            'price', 'stock', 'image', 'is_active', 'created_at', 'updated_at',
            'created_by_name', 'reviews', 'average_rating', 'is_in_stock'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


# apps/orders/serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem, Cart, CartItem
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer para items del carrito"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        write_only=True,
        source='product'
    )
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal']
        read_only_fields = ['id', 'subtotal']
    
    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity', 1)
        
        if product and quantity > product.stock:
            raise serializers.ValidationError(
                f"Not enough stock. Available: {product.stock}"
            )
        
        return attrs

class CartSerializer(serializers.ModelSerializer):
    """Serializer para el carrito"""
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_amount', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer para items de pedido"""
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price', 'subtotal']

class OrderListSerializer(serializers.ModelSerializer):
    """Serializer para lista de pedidos"""
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_amount', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.items.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para pedidos"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'status', 'total_amount',
            'shipping_address', 'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear pedidos desde el carrito"""
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'notes']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        with transaction.atomic():
            # Verificar que el usuario tenga carrito con items
            try:
                cart = user.cart
                if not cart.items.exists():
                    raise serializers.ValidationError("Cart is empty")
            except Cart.DoesNotExist:
                raise serializers.ValidationError("No cart found")
            
            # Crear orden
            order = Order.objects.create(user=user, **validated_data)
            
            # Crear items del pedido y actualizar stock
            for cart_item in cart.items.select_related('product'):
                product = cart_item.product
                
                # Verificar stock disponible
                if product.stock < cart_item.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}. Available: {product.stock}"
                    )
                
                # Crear item del pedido
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item.quantity,
                    price=product.price
                )
                
                # Actualizar stock
                product.stock -= cart_item.quantity
                product.save()
            
            # Calcular total y limpiar carrito
            order.calculate_total()
            cart.items.all().delete()
            
            return order