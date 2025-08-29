# performance_examples.py - Casos reales de optimización para entrevistas

from django.db.models import Count, Avg, Prefetch, Q, F
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
import time

# =============================================================================
# CASO 1: PÁGINA DE CATÁLOGO - Problema N+1 Classic
# =============================================================================

class ProductCatalogBadExample:
    """❌ Ejemplo MALO - Problema N+1"""
    
    def get_products(self, category_slug=None):
        products = Product.objects.filter(is_active=True)
        
        if category_slug:
            products = products.filter(category__slug=category_slug)
        
        # ❌ Esto genera N+1 queries en el template
        return products[:20]

class ProductCatalogGoodExample:
    """✅ Ejemplo BUENO - Optimizado"""
    
    def get_products(self, category_slug=None):
        # Optimización 1: select_related para ForeignKey
        products = Product.objects.select_related(
            'category', 'brand'
        ).prefetch_related(
            # Optimización 2: prefetch para ManyToMany
            Prefetch(
                'images',
                queryset=ProductImage.objects.filter(is_main=True),
                to_attr='main_image'
            )
        ).filter(is_active=True)
        
        if category_slug:
            products = products.filter(category__slug=category_slug)
        
        # Optimización 3: Añadir datos calculados en DB
        return products.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
            is_in_stock=Case(
                When(inventory__quantity__gt=0, then=Value(True)),
                default=Value(False)
            )
        )[:20]

# Comparación de performance:
def compare_catalog_performance():
    """Función para demostrar la diferencia en entrevistas"""
    
    print("=== COMPARACIÓN DE PERFORMANCE ===\n")
    
    # Método malo
    start = time.time()
    bad_products = ProductCatalogBadExample().get_products()
    # Simular acceso a relaciones (como en template)
    for product in bad_products:
        _ = product.category.name
        _ = product.brand.name if product.brand else "No brand"
        _ = product.images.filter(is_main=True).first()
    bad_time = time.time() - start
    
    # Método bueno
    start = time.time()
    good_products = ProductCatalogGoodExample().get_products()
    # Simular mismo acceso
    for product in good_products:
        _ = product.category.name
        _ = product.brand.name if product.brand else "No brand"
        _ = getattr(product, 'main_image', [None])[0] if hasattr(product, 'main_image') else None
    good_time = time.time() - start
    
    print(f"Método malo: {bad_time:.4f}s")
    print(f"Método bueno: {good_time:.4f}s")
    print(f"Mejora: {bad_time/good_time:.1f}x más rápido")

# =============================================================================
# CASO 2: BÚSQUEDA CON FILTROS - Performance con múltiples condiciones
# =============================================================================

class ProductSearchOptimized:
    """Búsqueda optimizada con filtros múltiples"""
    
    def __init__(self):
        self.base_queryset = Product.objects.select_related(
            'category', 'brand'
        ).prefetch_related('images')
    
    def search(self, query=None, filters=None, page=1, per_page=20):
        """
        Búsqueda con filtros optimizada
        Demuestra: Dynamic filtering, caching, pagination
        """
        filters = filters or {}
        
        # Crear cache key basado en parámetros
        cache_key = f"search_{hash(str(sorted(filters.items())))}{query or ''}_p{page}"
        
        # Intentar obtener de cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        queryset = self.base_queryset.filter(is_active=True)
        
        # Filtro de texto optimizado
        if query:
            # Usar Q objects para OR conditions eficientes
            text_filter = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__name__icontains=query)
            )
            queryset = queryset.filter(text_filter)
        
        # Filtros dinámicos
        queryset = self._apply_filters(queryset, filters)
        
        # Añadir anotaciones una sola vez
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).distinct()
        
        # Paginación
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        result = {
            'products': page_obj.object_list,
            'page_obj': page_obj,
            'total_count': paginator.count
        }
        
        # Cache por 5 minutos
        cache.set(cache_key, result, 300)
        
        return result
    
    def _apply_filters(self, queryset, filters):
        """Aplica filtros de forma eficiente"""
        
        if filters.get('category'):
            queryset = queryset.filter(category__slug=filters['category'])
        
        if filters.get('min_price'):
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if filters.get('max_price'):
            queryset = queryset.filter(price__lte=filters['max_price'])
        
        if filters.get('brands'):
            queryset = queryset.filter(brand__slug__in=filters['brands'])
        
        if filters.get('rating'):
            # Usar subquery para filtrar por rating promedio
            queryset = queryset.annotate(
                temp_rating=Avg('reviews__rating')
            ).filter(temp_rating__gte=filters['rating'])
        
        if filters.get('in_stock'):
            queryset = queryset.filter(
                inventory__quantity__gt=F('inventory__reserved_quantity')
            )
        
        return queryset

# =============================================================================
# CASO 3: DASHBOARD ANALYTICS - Queries complejas optimizadas
# =============================================================================

class DashboardAnalytics:
    """Analytics optimizadas para dashboard administrativo"""
    
    @staticmethod
    def get_dashboard_stats():
        """
        Estadísticas del dashboard con queries optimizadas
        Demuestra: Aggregations, subqueries, window functions
        """
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Una sola query para múltiples estadísticas
        stats = {
            'products': {
                'total': Product.objects.count(),
                'active': Product.objects.filter(is_active=True).count(),
                'low_stock': Product.objects.filter(
                    inventory__quantity__lte=F('inventory__min_stock_level')
                ).count(),
                'out_of_stock': Product.objects.filter(
                    inventory__quantity=0
                ).count()
            }
        }
        
        # Estadísticas por categoría (una sola query)
        category_stats = Category.objects.annotate(
            product_count=Count('products'),
            active_products=Count('products', filter=Q(products__is_active=True)),
            avg_price=Avg('products__price'),
            total_value=Sum(
                F('products__price') * F('products__inventory__quantity')
            )
        ).filter(product_count__gt=0).order_by('-product_count')[:10]
        
        stats['categories'] = list(category_stats.values())
        
        # Top productos por reseñas (query optimizada)
        top_rated = Product.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).filter(
            review_count__gte=5
        ).order_by('-avg_rating', '-review_count')[:10]
        
        stats['top_rated'] = list(top_rated.values(
            'name', 'avg_rating', 'review_count', 'price'
        ))
        
        return stats

# =============================================================================
# CASO 4: API ENDPOINTS - Optimización para APIs REST
# =============================================================================

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSetOptimized(ReadOnlyModelViewSet):
    """ViewSet optimizado para API REST"""
    
    def get_queryset(self):
        """Queryset base optimizado"""
        return Product.objects.select_related(
            'category', 'brand'
        ).prefetch_related(
            'images', 'variants'
        ).filter(is_active=True)
    
    @method_decorator(cache_page(300))  # Cache 5 minutos
    def list(self, request):
        """Lista paginada optimizada"""
        queryset = self.get_queryset()
        
        # Filtros desde query params
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        min_price = request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        # Añadir anotaciones
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        
        # Paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Productos trending - query compleja optimizada"""
        from django.utils import timezone
        from datetime import timedelta
        
        recent_date = timezone.now() - timedelta(days=7)
        
        trending = self.get_queryset().annotate(
            recent_reviews=Count(
                'reviews',
                filter=Q(reviews__created_at__gte=recent_date)
            ),
            avg_rating=Avg('reviews__rating'),
            total_reviews=Count('reviews')
        ).filter(
            recent_reviews__gte=3,
            avg_rating__gte=4.0
        ).order_by('-recent_reviews', '-avg_rating')[:20]
        
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

# =============================================================================
# CASO 5: BULK OPERATIONS - Operaciones masivas eficientes
# =============================================================================

class BulkOperationsService:
    """Servicio para operaciones masivas eficientes"""
    
    @staticmethod
    def bulk_update_prices(category_slug, percentage_increase):
        """
        Actualización masiva de precios
        Demuestra: bulk_update, F expressions, transactions
        """
        from django.db import transaction
        
        with transaction.atomic():
            # Usar F expressions para actualizar en DB
            updated_count = Product.objects.filter(
                category__slug=category_slug,
                is_active=True
            ).update(
                price=F('price') * (1 + percentage_increase / 100),
                updated_at=timezone.now()
            )
            
            return updated_count
    
    @staticmethod
    def bulk_create_products(products_data):
        """
        Creación masiva de productos
        Demuestra: bulk_create, batch processing
        """
        from django.db import transaction
        
        batch_size = 1000
        products_to_create = []
        
        with transaction.atomic():
            for data in products_data:
                product = Product(
                    name=data['name'],
                    price=data['price'],
                    category_id=data['category_id'],
                    # ... otros campos
                )
                products_to_create.append(product)
                
                # Procesar en lotes
                if len(products_to_create) >= batch_size:
                    Product.objects.bulk_create(products_to_create)
                    products_to_create = []
            
            # Procesar último lote
            if products_to_create:
                Product.objects.bulk_create(products_to_create)
    
    @staticmethod
    def update_product_ratings():
        """
        Actualizar ratings calculados de todos los productos
        Demuestra: bulk_update con annotations
        """
        from django.db import transaction
        
        # Calcular ratings en una query
        products_with_ratings = Product.objects.annotate(
            calculated_rating=Avg('reviews__rating'),
            calculated_review_count=Count('reviews')
        ).filter(calculated_rating__isnull=False)
        
        # Preparar objetos para bulk_update
        products_to_update = []
        for product in products_with_ratings:
            product.avg_rating = product.calculated_rating
            product.review_count = product.calculated_review_count
            products_to_update.append(product)
        
        # Actualizar en lotes
        with transaction.atomic():
            Product.objects.bulk_update(
                products_to_update,
                ['avg_rating', 'review_count'],
                batch_size=1000
            )

# =============================================================================
# HERRAMIENTAS DE BENCHMARKING PARA ENTREVISTAS
# =============================================================================

class PerformanceBenchmark:
    """Herramienta para comparar performance de queries"""
    
    @staticmethod
    def compare_queries(query_functions, iterations=10):
        """
        Compara performance entre diferentes implementaciones
        Útil para demostrar optimizaciones en entrevistas
        """
        results = {}
        
        for name, query_func in query_functions.items():
            times = []
            
            for _ in range(iterations):
                start_time = time.time()
                
                # Resetear queries para contar solo las de esta función
                connection.queries_log.clear()
                
                # Ejecutar función
                result = query_func()
                
                # Forzar evaluación del queryset si es necesario
                if hasattr(result, '__iter__'):
                    list(result)
                
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            query_count = len(connection.queries)
            
            results[name] = {
                'avg_time': avg_time,
                'query_count': query_count,
                'times': times
            }
        
        # Mostrar resultados
        print(f"\n{'='*60}")
        print("BENCHMARK RESULTS")
        print('='*60)
        
        for name, result in results.items():
            print(f"{name}:")
            print(f"  Average time: {result['avg_time']:.4f}s")
            print(f"  Query count: {result['query_count']}")
            print(f"  Min time: {min(result['times']):.4f}s")
            print(f"  Max time: {max(result['times']):.4f}s")
            print()
        
        return results

# Ejemplo de uso para entrevistas:
"""
def test_optimization():
    # Definir diferentes implementaciones
    query_functions = {
        'unoptimized': lambda: Product.objects.all()[:10],
        'with_select_related': lambda: Product.objects.select_related('category', 'brand')[:10],
        'fully_optimized': lambda: Product.objects.select_related('category', 'brand')
                                     .prefetch_related('images')
                                     .annotate(avg_rating=Avg('reviews__rating'))[:10]
    }
    
    # Comparar performance
    PerformanceBenchmark.compare_queries(query_functions)

# Ejecutar: test_optimization()
"""