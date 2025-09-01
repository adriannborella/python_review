# models.py - E-commerce models con problemas de performance
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['name']),  # Índice para búsquedas
        ]
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'brands'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['category', 'is_active']),  # Compound index
            models.Index(fields=['brand', 'is_active']),
        ]
    
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['rating']),
        ]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    
    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio al momento de compra
    
    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

# views.py - Views con problemas de performance (ANTES de optimizar)

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, F, Count, Avg, Sum
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time

# ❌ PROBLEMA: N+1 queries - MAL EJEMPLO
def product_list_slow(request):
    """Vista con problemas de performance - N+1 queries"""
    products = Product.objects.filter(is_active=True)[:20]
    
    product_data = []
    for product in products:
        # ❌ Cada iteración hace queries adicionales
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        review_count = product.reviews.count()
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category.name,  # ❌ Query adicional
            'brand': product.brand.name,        # ❌ Query adicional
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
        })
    
    return JsonResponse({'products': product_data})

# ✅ OPTIMIZADO: Select related y agregaciones eficientes
def product_list_optimized(request):
    """Vista optimizada - Una sola query con joins"""
    products = Product.objects.select_related('category', 'brand').annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(is_active=True)[:20]
    
    product_data = [{
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'category': product.category.name,
        'brand': product.brand.name,
        'avg_rating': round(product.avg_rating or 0, 1),
        'review_count': product.review_count,
    } for product in products]
    
    return JsonResponse({'products': product_data})

# ❌ PROBLEMA: Query compleja sin optimización
def user_dashboard_slow(request):
    """Dashboard con múltiples queries ineficientes"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    
    # ❌ Multiple queries separadas
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    order_data = []
    
    for order in orders:
        # ❌ N+1 para items de cada order
        items = order.items.all()
        item_data = []
        
        for item in items:
            # ❌ Query adicional por cada producto
            item_data.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price)
            })
        
        order_data.append({
            'id': order.id,
            'created_at': order.created_at.isoformat(),
            'total': str(order.total),
            'status': order.status,
            'items': item_data
        })
    
    # ❌ Query separada para estadísticas
    total_spent = Order.objects.filter(
        user=user, 
        status='completed'
    ).aggregate(Sum('total'))['total__sum'] or 0
    
    return JsonResponse({
        'recent_orders': order_data,
        'total_spent': str(total_spent)
    })

# ✅ OPTIMIZADO: Prefetch y optimización de queries
def user_dashboard_optimized(request):
    """Dashboard optimizado con prefetch_related"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    
    # ✅ Una query principal con prefetch_related
    orders = Order.objects.select_related('user').prefetch_related(
        'items__product'  # Prefetch items y sus productos
    ).filter(user=user).order_by('-created_at')[:5]
    
    order_data = []
    for order in orders:
        item_data = [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': str(item.price)
        } for item in order.items.all()]  # ✅ No queries adicionales
        
        order_data.append({
            'id': order.id,
            'created_at': order.created_at.isoformat(),
            'total': str(order.total),
            'status': order.status,
            'items': item_data
        })
    
    # ✅ Estadística en la misma consulta inicial si es posible
    # O al menos una query separada pero optimizada
    total_spent = user.orders.filter(status='completed').aggregate(
        Sum('total')
    )['total__sum'] or 0
    
    return JsonResponse({
        'recent_orders': order_data,
        'total_spent': str(total_spent)
    })

# ✅ TÉCNICA AVANZADA: Query optimizada con anotaciones complejas
def category_stats_optimized(request):
    """Estadísticas por categoría con una sola query compleja"""
    categories = Category.objects.annotate(
        product_count=Count('products', filter=Q(products__is_active=True)),
        avg_price=Avg('products__price', filter=Q(products__is_active=True)),
        total_reviews=Count('products__reviews'),
        avg_rating=Avg('products__reviews__rating')
    ).filter(product_count__gt=0).order_by('-product_count')
    
    category_data = [{
        'id': cat.id,
        'name': cat.name,
        'product_count': cat.product_count,
        'avg_price': round(float(cat.avg_price or 0), 2),
        'total_reviews': cat.total_reviews,
        'avg_rating': round(float(cat.avg_rating or 0), 1)
    } for cat in categories]
    
    return JsonResponse({'categories': category_data})

# ✅ PAGINACIÓN OPTIMIZADA
class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 20
    context_object_name = 'products'
    
    def get_queryset(self):
        """Queryset optimizado con select_related y annotate"""
        queryset = Product.objects.select_related(
            'category', 'brand'
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).filter(is_active=True)
        
        # Filtros opcionales
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand_id=brand)
        
        # Ordenamiento
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by in ['name', 'price', '-price', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ✅ Context data adicional con queries optimizadas
        context['categories'] = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).filter(product_count__gt=0)
        
        context['brands'] = Brand.objects.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).filter(product_count__gt=0)
        
        return context

# ✅ TÉCNICA: Cache con decorador
@cache_page(60 * 15)  # Cache 15 minutos
def popular_products(request):
    """Productos populares con cache"""
    products = Product.objects.select_related('category', 'brand').annotate(
        order_count=Count('orderitem'),
        avg_rating=Avg('reviews__rating')
    ).filter(
        is_active=True,
        order_count__gt=0
    ).order_by('-order_count', '-avg_rating')[:10]
    
    product_data = [{
        'id': p.id,
        'name': p.name,
        'price': str(p.price),
        'category': p.category.name,
        'brand': p.brand.name,
        'order_count': p.order_count,
        'avg_rating': round(float(p.avg_rating or 0), 1)
    } for p in products]
    
    return JsonResponse({'popular_products': product_data})

# UTILIDADES PARA PROFILING

def profile_view_performance(view_func):
    """Decorator para medir performance de views"""
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        
        # Contar queries antes
        from django.db import connection
        queries_before = len(connection.queries)
        
        response = view_func(request, *args, **kwargs)
        
        # Métricas después
        queries_after = len(connection.queries)
        execution_time = time.time() - start_time
        
        print(f"View: {view_func.__name__}")
        print(f"Execution time: {execution_time:.4f}s")
        print(f"Database queries: {queries_after - queries_before}")
        print("-" * 50)
        
        return response
    
    return wrapper

# Ejemplo de uso del decorator
@profile_view_performance
def test_performance_view(request):
    return product_list_optimized(request)