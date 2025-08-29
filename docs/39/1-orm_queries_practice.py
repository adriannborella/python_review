# queries.py - Django ORM Avanzado para Entrevistas

from django.db.models import (
    Q, F, Value, Case, When, Count, Avg, Sum, Max, Min,
    Prefetch, Exists, OuterRef, Subquery
)
from django.db.models.functions import Concat, Coalesce, Extract
from django.utils import timezone
from datetime import timedelta
from .models import Product, Category, Review, ProductImage, Inventory

# =============================================================================
# 1. BÚSQUEDA Y FILTRADO AVANZADO
# =============================================================================

class ProductQueryService:
    """Servicio para queries complejas de productos"""
    
    @staticmethod
    def search_products(query, category_slug=None, **filters):
        """
        Búsqueda inteligente de productos
        Demuestra: Q objects, dynamic filtering, performance
        """
        queryset = Product.objects.active().select_related(
            'category', 'brand'
        ).prefetch_related('images')
        
        # Búsqueda por texto
        if query:
            search_filter = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query) |
                Q(sku__iexact=query)
            )
            queryset = queryset.filter(search_filter)
        
        # Filtro por categoría (incluyendo subcategorías)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            category_filter = Q(category=category)
            
            # Incluir subcategorías si existen
            if category.children.exists():
                subcategories = category.children.all()
                category_filter |= Q(category__in=subcategories)
            
            queryset = queryset.filter(category_filter)
        
        # Filtros dinámicos
        if filters.get('min_price'):
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if filters.get('max_price'):
            queryset = queryset.filter(price__lte=filters['max_price'])
        
        if filters.get('brands'):
            queryset = queryset.filter(brand__slug__in=filters['brands'])
        
        if filters.get('on_sale'):
            queryset = queryset.filter(compare_price__gt=F('price'))
        
        if filters.get('in_stock'):
            queryset = queryset.filter(
                inventory__quantity__gt=F('inventory__reserved_quantity')
            )
        
        if filters.get('featured'):
            queryset = queryset.filter(is_featured=True)
        
        return queryset.distinct()
    
    @staticmethod
    def get_trending_products(days=7, limit=10):
        """
        Productos trending basados en reseñas recientes
        Demuestra: Subqueries, date filtering, complex annotations
        """
        recent_date = timezone.now() - timedelta(days=days)
        
        return Product.objects.annotate(
            recent_reviews=Count(
                'reviews',
                filter=Q(reviews__created_at__gte=recent_date)
            ),
            avg_rating=Avg('reviews__rating'),
            total_reviews=Count('reviews')
        ).filter(
            recent_reviews__gte=3,
            avg_rating__gte=4.0
        ).order_by('-recent_reviews', '-avg_rating')[:limit]
    
    @staticmethod
    def get_products_with_low_stock(threshold=5):
        """
        Productos con stock bajo
        Demuestra: Joins con OneToOne, F expressions
        """
        return Product.objects.select_related('inventory').filter(
            track_inventory=True,
            inventory__quantity__lte=F('inventory__min_stock_level')
        ).annotate(
            available_stock=F('inventory__quantity') - F('inventory__reserved_quantity')
        ).filter(available_stock__lte=threshold)

# =============================================================================
# 2. AGREGACIONES Y ESTADÍSTICAS
# =============================================================================

class ProductStatsService:
    """Servicio para estadísticas y reportes"""
    
    @staticmethod
    def category_performance():
        """
        Rendimiento por categoría
        Demuestra: Complex aggregations, multiple annotations
        """
        return Category.objects.annotate(
            total_products=Count('products'),
            active_products=Count('products', filter=Q(products__is_active=True)),
            avg_price=Avg('products__price'),
            min_price=Min('products__price'),
            max_price=Max('products__price'),
            total_reviews=Count('products__reviews'),
            avg_rating=Avg('products__reviews__rating'),
            products_in_stock=Count(
                'products',
                filter=Q(
                    products__inventory__quantity__gt=F('products__inventory__reserved_quantity')
                )
            )
        ).filter(total_products__gt=0).order_by('-total_products')
    
    @staticmethod
    def top_rated_products(min_reviews=5):
        """
        Productos mejor valorados
        Demuestra: Filtering annotations, ordering
        """
        return Product.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
            rating_score=Avg('reviews__rating') * Count('reviews')  # Peso por cantidad
        ).filter(
            review_count__gte=min_reviews
        ).order_by('-rating_score', '-avg_rating')[:20]
    
    @staticmethod
    def monthly_product_stats():
        """
        Estadísticas mensuales de productos
        Demuestra: Date functions, grouping
        """
        return Product.objects.annotate(
            created_month=Extract('created_at', 'month'),
            created_year=Extract('created_at', 'year')
        ).values('created_year', 'created_month').annotate(
            products_created=Count('id'),
            avg_price=Avg('price'),
            total_value=Sum('price')
        ).order_by('-created_year', '-created_month')

# =============================================================================
# 3. SUBQUERIES Y EXISTS
# =============================================================================

class AdvancedProductQueries:
    """Queries avanzadas con subqueries y exists"""
    
    @staticmethod
    def products_without_reviews():
        """
        Productos sin reseñas
        Demuestra: Subquery con EXISTS
        """
        return Product.objects.filter(
            ~Exists(
                Review.objects.filter(product=OuterRef('pk'))
            )
        )
    
    @staticmethod
    def products_with_highest_rated_review():
        """
        Productos con su reseña mejor puntuada
        Demuestra: Subquery para obtener datos relacionados
        """
        highest_rated_review = Review.objects.filter(
            product=OuterRef('pk')
        ).order_by('-rating').values('rating', 'title', 'user__username')[:1]
        
        return Product.objects.annotate(
            highest_rating=Subquery(highest_rated_review.values('rating')),
            best_review_title=Subquery(highest_rated_review.values('title')),
            best_reviewer=Subquery(highest_rated_review.values('user__username'))
        ).filter(highest_rating__isnull=False)
    
    @staticmethod
    def categories_with_expensive_products(min_price=1000):
        """
        Categorías que tienen productos caros
        Demuestra: EXISTS con filtering
        """
        return Category.objects.filter(
            Exists(
                Product.objects.filter(
                    category=OuterRef('pk'),
                    price__gte=min_price
                )
            )
        ).annotate(
            expensive_product_count=Count(
                'products',
                filter=Q(products__price__gte=min_price)
            )
        )

# =============================================================================
# 4. OPTIMIZACIÓN Y PERFORMANCE
# =============================================================================

class OptimizedProductViews:
    """Queries optimizadas para vistas comunes"""
    
    @staticmethod
    def product_list_optimized():
        """
        Lista de productos optimizada para vista de catálogo
        Demuestra: select_related, prefetch_related, annotations
        """
        main_image_prefetch = Prefetch(
            'images',
            queryset=ProductImage.objects.filter(is_main=True),
            to_attr='main_image'
        )
        
        return Product.objects.active().select_related(
            'category', 'brand', 'inventory'
        ).prefetch_related(
            main_image_prefetch
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
            is_in_stock=Case(
                When(
                    inventory__quantity__gt=F('inventory__reserved_quantity'),
                    then=Value(True)
                ),
                default=Value(False)
            )
        )
    
    @staticmethod
    def product_detail_optimized(slug):
        """
        Detalle de producto optimizado
        Demuestra: Custom prefetch, complex relationships
        """
        approved_reviews_prefetch = Prefetch(
            'reviews',
            queryset=Review.objects.filter(is_approved=True).select_related('user'),
            to_attr='approved_reviews'
        )
        
        related_products_prefetch = Prefetch(
            'category__products',
            queryset=Product.objects.active().exclude(slug=slug)[:4],
            to_attr='related_products'
        )
        
        return Product.objects.select_related(
            'category', 'brand', 'inventory'
        ).prefetch_related(
            'images',
            'variants',
            approved_reviews_prefetch,
            related_products_prefetch
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
            stock_level=F('inventory__quantity') - F('inventory__reserved_quantity')
        ).get(slug=slug)

# =============================================================================
# 5. QUERIES PARA ENTREVISTAS COMUNES
# =============================================================================

class InterviewQueries:
    """Queries típicas que preguntan en entrevistas"""
    
    @staticmethod
    def find_duplicate_products():
        """
        Encontrar productos duplicados por nombre
        Pregunta típica: "¿Cómo encontrarías duplicados?"
        """
        return Product.objects.values('name').annotate(
            count=Count('id')
        ).filter(count__gt=1)
    
    @staticmethod
    def products_price_above_category_average():
        """
        Productos con precio mayor al promedio de su categoría
        Pregunta típica: "Productos más caros que el promedio de su categoría"
        """
        category_avg_price = Category.objects.filter(
            id=OuterRef('category_id')
        ).annotate(
            avg_price=Avg('products__price')
        ).values('avg_price')
        
        return Product.objects.annotate(
            category_avg_price=Subquery(category_avg_price)
        ).filter(price__gt=F('category_avg_price'))
    
    @staticmethod
    def top_customers_by_reviews():
        """
        Top usuarios por cantidad de reseñas
        Pregunta típica: "Usuarios más activos"
        """
        from django.contrib.auth.models import User
        
        return User.objects.annotate(
            review_count=Count('reviews'),
            avg_rating_given=Avg('reviews__rating'),
            recent_reviews=Count(
                'reviews',
                filter=Q(reviews__created_at__gte=timezone.now() - timedelta(days=30))
            )
        ).filter(review_count__gt=0).order_by('-review_count')
    
    @staticmethod
    def products_never_reviewed_but_in_stock():
        """
        Productos en stock que nunca fueron reseñados
        Demuestra: Multiple conditions, NOT EXISTS
        """
        return Product.objects.filter(
            ~Exists(Review.objects.filter(product=OuterRef('pk'))),
            inventory__quantity__gt=F('inventory__reserved_quantity'),
            is_active=True
        ).select_related('category', 'inventory')

# =============================================================================
# 6. FUNCIONES HELPER PARA DEBUGGING
# =============================================================================

def analyze_query(queryset, print_sql=True):
    """
    Analiza una query para debugging
    Útil para entrevistas: mostrar que sabes debuggear
    """
    if print_sql:
        print("SQL Query:")
        print(queryset.query)
        print("\n" + "="*50 + "\n")
    
    # Ejecutar y medir tiempo
    import time
    start_time = time.time()
    results = list(queryset)
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    print(f"Results count: {len(results)}")
    
    return results

def explain_query(queryset):
    """
    EXPLAIN de la query (solo PostgreSQL)
    """
    from django.db import connection
    
    cursor = connection.cursor()
    cursor.execute(f"EXPLAIN ANALYZE {queryset.query}")
    return cursor.fetchall()

# Ejemplo de uso para debugging en entrevistas:
"""
# Analizar performance de una query
products = ProductQueryService.search_products("smartphone", min_price=200)
analyze_query(products)

# Comparar queries optimizadas vs no optimizadas
print("Query NO optimizada:")
slow_query = Product.objects.all()
for product in slow_query[:5]:  # N+1 problem
    print(f"{product.name} - {product.category.name}")

print("\nQuery OPTIMIZADA:")
fast_query = Product.objects.select_related('category').all()
for product in fast_query[:5]:  # Single query
    print(f"{product.name} - {product.category.name}")
"""