# apps/authentication/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserAuthenticationTest(APITestCase):
    """Tests para autenticación de usuarios"""
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
    
    def test_user_registration_success(self):
        """Test de registro exitoso"""
        response = self.client.post(self.orders_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(len(response.data['items']), 1)
        
        # Verificar que el stock se actualizó
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)  # 10 - 2 = 8
        
        # Verificar que el carrito se limpió
        self.assertEqual(cart.items.count(), 0)
    
    def test_create_order_empty_cart(self):
        """Test para crear pedido con carrito vacío"""
        data = {
            'shipping_address': '123 Main St, City, Country'
        }
        
        response = self.client.post(self.orders_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_order_insufficient_stock(self):
        """Test para crear pedido con stock insuficiente"""
        # Crear carrito con cantidad mayor al stock
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        # Reducir stock del producto
        self.product.stock = 1
        self.product.save()
        
        data = {
            'shipping_address': '123 Main St, City, Country'
        }
        
        response = self.client.post(self.orders_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_orders(self):
        """Test para obtener pedidos del usuario"""
        # Crear un pedido
        order = Order.objects.create(
            user=self.user,
            shipping_address='123 Main St',
            total_amount=Decimal('99.99')
        )
        
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_order_detail(self):
        """Test para obtener detalle del pedido"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='123 Main St',
            total_amount=Decimal('99.99')
        )
        
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)
    
    def test_cannot_access_other_user_orders(self):
        """Test para verificar que no se puede acceder a pedidos de otros usuarios"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        order = Order.objects.create(
            user=other_user,
            shipping_address='456 Other St',
            total_amount=Decimal('149.99')
        )
        
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Integración de tests con coverage
# Archivo: conftest.py (en la raíz del proyecto)
import pytest
from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from decimal import Decimal

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='A test category'
    )

@pytest.fixture
def product(user, category):
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        description='A test product',
        category=category,
        price=Decimal('99.99'),
        stock=10,
        created_by=user
    )

# utils/test_helpers.py
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def create_authenticated_client(user=None):
    """Crea un cliente API autenticado"""
    if not user:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    return client, user

def create_test_data():
    """Crea datos de prueba básicos"""
    from apps.products.models import Category, Product
    from decimal import Decimal
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        name='Electronics',
        slug='electronics',
        description='Electronic products'
    )
    
    product = Product.objects.create(
        name='Smartphone',
        slug='smartphone',
        description='Latest smartphone',
        category=category,
        price=Decimal('699.99'),
        stock=50,
        created_by=user
    )
    
    return {
        'user': user,
        'category': category,
        'product': product
    }

# Performance Tests
# apps/products/performance_tests.py
import time
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product, ProductReview
from decimal import Decimal

User = get_user_model()

class ProductPerformanceTest(TestCase):
    """Tests de performance para productos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        
        # Crear muchos productos para test de performance
        self.products = []
        for i in range(100):
            product = Product.objects.create(
                name=f'Product {i}',
                slug=f'product-{i}',
                description=f'Description for product {i}',
                category=self.category,
                price=Decimal(f'{i + 10}.99'),
                stock=10,
                created_by=self.user
            )
            self.products.append(product)
    
    def test_product_list_query_performance(self):
        """Test de performance para consulta de productos"""
        start_time = time.time()
        
        # Consulta optimizada con select_related y prefetch_related
        products = Product.objects.select_related('category', 'created_by')\
                                .prefetch_related('reviews')\
                                .filter(is_active=True)[:20]
        
        # Forzar evaluación del queryset
        list(products)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # La consulta debería tomar menos de 1 segundo
        self.assertLess(execution_time, 1.0)
    
    def test_product_with_reviews_performance(self):
        """Test de performance para productos con muchas reseñas"""
        product = self.products[0]
        
        # Crear muchas reseñas
        for i in range(50):
            user = User.objects.create_user(
                username=f'reviewer{i}',
                email=f'reviewer{i}@example.com',
                password='testpass123'
            )
            ProductReview.objects.create(
                product=product,
                user=user,
                rating=5,
                comment=f'Great product! Review {i}'
            )
        
        start_time = time.time()
        
        # Consulta con reseñas
        product_with_reviews = Product.objects.select_related('category')\
                                            .prefetch_related('reviews__user')\
                                            .get(id=product.id)
        
        # Acceder a las reseñas
        reviews_count = product_with_reviews.reviews.count()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(reviews_count, 50)
        self.assertLess(execution_time, 0.5)

# Script de carga masiva de datos para testing
# scripts/load_test_data.py
#!/usr/bin/env python
"""
Script para cargar datos de prueba masivos
Uso: python manage.py shell < scripts/load_test_data.py
"""

import os
import django
from decimal import Decimal
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')
django.setup()

from apps.products.models import Category, Product, ProductReview
from apps.orders.models import Order, OrderItem

User = get_user_model()

def create_test_users(count=10):
    """Crear usuarios de prueba"""
    users = []
    for i in range(count):
        user = User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password='testpass123',
            first_name=f'User{i}',
            last_name='Test'
        )
        users.append(user)
    return users

def create_test_categories():
    """Crear categorías de prueba"""
    categories_data = [
        ('Electronics', 'electronics', 'Electronic devices and accessories'),
        ('Clothing', 'clothing', 'Fashion and clothing items'),
        ('Books', 'books', 'Books and educational materials'),
        ('Home & Garden', 'home-garden', 'Home improvement and garden items'),
        ('Sports', 'sports', 'Sports equipment and accessories'),
    ]
    
    categories = []
    for name, slug, description in categories_data:
        category = Category.objects.create(
            name=name,
            slug=slug,
            description=description
        )
        categories.append(category)
    return categories

def create_test_products(categories, users, count_per_category=20):
    """Crear productos de prueba"""
    products = []
    for category in categories:
        for i in range(count_per_category):
            product = Product.objects.create(
                name=f'{category.name} Product {i}',
                slug=f'{category.slug}-product-{i}',
                description=f'High quality {category.name.lower()} product {i}',
                category=category,
                price=Decimal(f'{10 + (i * 5)}.99'),
                stock=50 + i,
                created_by=users[i % len(users)]
            )
            products.append(product)
    return products

def create_test_reviews(products, users):
    """Crear reseñas de prueba"""
    import random
    
    for product in products[:50]:  # Solo para los primeros 50 productos
        review_count = random.randint(1, 10)
        selected_users = random.sample(users, min(review_count, len(users)))
        
        for user in selected_users:
            ProductReview.objects.create(
                product=product,
                user=user,
                rating=random.randint(3, 5),
                comment=f'Great {product.name.lower()}! Highly recommended.'
            )

def main():
    """Función principal para crear todos los datos de prueba"""
    print("Creando datos de prueba...")
    
    # Crear usuarios
    print("Creando usuarios...")
    users = create_test_users(20)
    
    # Crear categorías
    print("Creando categorías...")
    categories = create_test_categories()
    
    # Crear productos
    print("Creando productos...")
    products = create_test_products(categories, users, 30)
    
    # Crear reseñas
    print("Creando reseñas...")
    create_test_reviews(products, users)
    
    print(f"""
    Datos de prueba creados exitosamente:
    - {len(users)} usuarios
    - {len(categories)} categorías  
    - {len(products)} productos
    - Reseñas para los primeros 50 productos
    """)

if __name__ == '__main__':
    main().client.post(self.register_url, self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        
        # Verificar que el perfil fue creado automáticamente
        user = User.objects.get(email='test@example.com')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
    
    def test_user_registration_password_mismatch(self):
        """Test de registro con contraseñas que no coinciden"""
        data = self.user_data.copy()
        data['password_confirm'] = 'differentpass'
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_success(self):
        """Test de login exitoso"""
        # Crear usuario primero
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test de login con credenciales inválidas"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpass'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_profile_access_authenticated(self):
        """Test de acceso al perfil con usuario autenticado"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=user)
        
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_profile_access_unauthenticated(self):
        """Test de acceso al perfil sin autenticación"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# apps/products/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category, Product, ProductReview
from decimal import Decimal

User = get_user_model()

class ProductAPITest(APITestCase):
    """Tests para API de productos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic products'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            category=self.category,
            price=Decimal('99.99'),
            stock=10,
            created_by=self.user
        )
        
        self.products_url = reverse('product-list')
        self.categories_url = reverse('category-list')
    
    def test_get_products_list(self):
        """Test para obtener lista de productos"""
        response = self.client.get(self.products_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Product')
    
    def test_get_product_detail(self):
        """Test para obtener detalle de producto"""
        url = reverse('product-detail', kwargs={'slug': 'test-product'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['category']['name'], 'Electronics')
    
    def test_create_product_authenticated(self):
        """Test para crear producto con usuario autenticado"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'A new product',
            'category_id': self.category.id,
            'price': '149.99',
            'stock': 5
        }
        
        response = self.client.post(self.products_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
    
    def test_create_product_unauthenticated(self):
        """Test para crear producto sin autenticación"""
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'A new product',
            'category_id': self.category.id,
            'price': '149.99',
            'stock': 5
        }
        
        response = self.client.post(self.products_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_product_owner(self):
        """Test para actualizar producto por el propietario"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-detail', kwargs={'slug': 'test-product'})
        data = {'name': 'Updated Product Name'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product Name')
    
    def test_update_product_non_owner(self):
        """Test para actualizar producto por usuario no propietario"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)
        
        url = reverse('product-detail', kwargs={'slug': 'test-product'})
        data = {'name': 'Updated Product Name'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_add_product_review(self):
        """Test para agregar reseña a producto"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-add-review', kwargs={'slug': 'test-product'})
        data = {
            'rating': 5,
            'comment': 'Excellent product!'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
    
    def test_add_duplicate_review(self):
        """Test para agregar reseña duplicada"""
        # Crear reseña existente
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Good product'
        )
        
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-add-review', kwargs={'slug': 'test-product'})
        data = {
            'rating': 5,
            'comment': 'Excellent product!'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_featured_products(self):
        """Test para obtener productos destacados"""
        # Crear productos con reseñas
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Great!'
        )
        
        url = reverse('product-featured')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_filtering(self):
        """Test para filtrado de productos"""
        # Test filtro por categoría
        response = self.client.get(f"{self.products_url}?category={self.category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test filtro por precio
        response = self.client.get(f"{self.products_url}?min_price=50&max_price=150")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test búsqueda
        response = self.client.get(f"{self.products_url}?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


# apps/orders/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Order, Cart, CartItem
from apps.products.models import Category, Product
from decimal import Decimal

User = get_user_model()

class CartAPITest(APITestCase):
    """Tests para API del carrito"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            category=self.category,
            price=Decimal('99.99'),
            stock=10,
            created_by=self.user
        )
        
        self.cart_url = reverse('cart-list')
        self.client.force_authenticate(user=self.user)
    
    def test_get_empty_cart(self):
        """Test para obtener carrito vacío"""
        response = self.client.get(self.cart_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)
        self.assertEqual(float(response.data['total_amount']), 0.0)
    
    def test_add_item_to_cart(self):
        """Test para agregar item al carrito"""
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)
    
    def test_add_item_insufficient_stock(self):
        """Test para agregar item con stock insuficiente"""
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 15  # Más que el stock disponible (10)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_cart_item(self):
        """Test para actualizar item del carrito"""
        # Agregar item primero
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        url = reverse('cart-update-item')
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 3)
    
    def test_remove_cart_item(self):
        """Test para remover item del carrito"""
        # Agregar item primero
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        url = reverse('cart-remove-item')
        data = {'product_id': self.product.id}
        
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el item fue removido
        self.assertFalse(CartItem.objects.filter(cart=cart, product=self.product).exists())
    
    def test_clear_cart(self):
        """Test para limpiar carrito"""
        # Agregar items primero
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        url = reverse('cart-clear')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart.items.count(), 0)

class OrderAPITest(APITestCase):
    """Tests para API de pedidos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            category=self.category,
            price=Decimal('99.99'),
            stock=10,
            created_by=self.user
        )
        
        self.orders_url = reverse('order-list')
        self.client.force_authenticate(user=self.user)
    
    def test_create_order_from_cart(self):
        """Test para crear pedido desde carrito"""
        # Crear carrito con items
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        data = {
            'shipping_address': '123 Main St, City, Country',
            'notes': 'Please deliver carefully'
        }
        
        response = self