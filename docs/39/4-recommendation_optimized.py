# recommendation_service.py - Sistema de Recomendaciones Optimizado

from django.db.models import Q, Count, Avg, F, Exists, OuterRef
from django.core.cache import cache
from collections import defaultdict
from .models import Product, Review, Category

class RecommendationService:
    """Servicio optimizado de recomendaciones"""
    
    @staticmethod
    def get_product_recommendations(user_id, limit=10):
        """
        Versión OPTIMIZADA del sistema de recomendaciones
        Demuestra: Subqueries, annotations, caching, single-query approach
        """
        cache_key = f'recommendations_user_{user_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 1. Obtener categorías y rangos de precio de productos que le gustaron al usuario
        user_preferences = Review.objects.filter(
            user_id=user_id,
            rating__gte=4
        ).select_related('product__category').values(
            'product__category_id',
            'product__price'
        )
        
        if not user_preferences:
            return []
        
        # 2. Extraer categorías y calcular rango de precios
        categories = set()
        prices = []
        
        for pref in user_preferences:
            categories.add(pref['product__category_id'])
            prices.append(pref['product__price'])
        
        if not prices:
            return []
        
        min_price = min(prices) * 0.8
        max_price = max(prices) * 1.2
        
        # 3. Una sola query optimizada para obtener recomendaciones
        recommended_products = Product.objects.filter(
            category_id__in=categories,
            price__range=(min_price, max_price),
            is_active=True
        ).exclude(
            # Excluir productos que ya reseñó
            id__in=Review.objects.filter(user_id=user_id).values('product_id')
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            good_review_count=Count('reviews', filter=Q(reviews__rating__gte=4))
        ).filter(
            good_review_count__gt=5,
            avg_rating__gte=4.0
        ).select_related('category', 'brand').order_by(
            '-avg_rating', '-good_review_count'
        )[:limit]
        
        result = list(recommended_products)
        cache.set(cache_key, result, 3600)  # Cache 1 hora
        
        return result
    
    @staticmethod
    def get_collaborative_recommendations(user_id, limit=10):
        """
        Recomendaciones colaborativas: "Usuarios similares también compraron"
        Demuestra: Subqueries complejas, window functions
        """
        cache_key = f'collaborative_rec_{user_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 1. Encontrar usuarios con gustos similares
        user_liked_products = Review.objects.filter(
            user_id=user_id,
            rating__gte=4
        ).values_list('product_id', flat=True)
        
        if not user_liked_products:
            return []
        
        # 2. Usuarios que también calificaron bien esos productos
        similar_users = Review.objects.filter(
            product_id__in=user_liked_products,
            rating__gte=4
        ).exclude(user_id=user_id).values('user_id').annotate(
            common_products=Count('product_id')
        ).filter(common_products__gte=2).values_list('user_id', flat=True)
        
        # 3. Productos que les gustaron a usuarios similares
        recommended_products = Product.objects.filter(
            reviews__user_id__in=similar_users,
            reviews__rating__gte=4,
            is_active=True
        ).exclude(
            id__in=Review.objects.filter(user_id=user_id).values('product_id')
        ).annotate(
            recommendation_score=Count('reviews', filter=Q(
                reviews__user_id__in=similar_users,
                reviews__rating__gte=4
            )),
            avg_rating=Avg('reviews__rating')
        ).filter(
            recommendation_score__gte=2
        ).select_related('category', 'brand').order_by(
            '-recommendation_score', '-avg_rating'
        )[:limit]
        
        result = list(recommended_products)
        cache.set(cache_key, result, 3600)
        
        return result
    
    @staticmethod
    def get_trending_recommendations(category_slug=None, limit=10):
        """
        Productos trending basados en actividad reciente
        Demuestra: Date filtering, complex scoring
        """
        from django.utils import timezone
        from datetime import timedelta
        
        recent_date = timezone.now() - timedelta(days=7)
        
        queryset = Product.objects.filter(is_active=True)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        trending = queryset.annotate(
            recent_reviews=Count(
                'reviews',
                filter=Q(reviews__created_at__gte=recent_date)
            ),
            recent_avg_rating=Avg(
                'reviews__rating',
                filter=Q(reviews__created_at__gte=recent_date)
            ),
            total_reviews=Count('reviews'),
            # Score compuesto: actividad reciente + calidad
            trending_score=F('recent_reviews') * 2 + F('recent_avg_rating')
        ).filter(
            recent_reviews__gte=3,
            recent_avg_rating__gte=4.0
        ).select_related('category', 'brand').order_by(
            '-trending_score'
        )[:limit]
        
        return list(trending)
    
    @staticmethod
    def get_category_recommendations(category_slug, exclude_product_id=None, limit=5):
        """
        Recomendaciones dentro de una categoría
        Optimizado para páginas de detalle de producto
        """
        cache_key = f'category_rec_{category_slug}_{exclude_product_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        queryset = Product.objects.filter(
            category__slug=category_slug,
            is_active=True
        )
        
        if exclude_product_id:
            queryset = queryset.exclude(id=exclude_product_id)
        
        recommendations = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
            # Score balanceando rating y popularidad
            score=Coalesce(F('avg_rating'), 3.0) * F('review_count')
        ).filter(
            review_count__gte=1
        ).select_related('brand').prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.filter(is_main=True),
                to_attr='main_image'
            )
        ).order_by('-score', '-created_at')[:limit]
        
        result = list(recommendations)
        cache.set(cache_key, result, 1800)  # Cache 30 min
        
        return result

# =============================================================================
# SISTEMA DE ANÁLISIS Y TESTING
# =============================================================================

class RecommendationAnalyzer:
    """Herramientas para analizar y testear el sistema de recomendaciones"""
    
    @staticmethod
    def analyze_recommendation_coverage(user_ids_sample=None):
        """
        Analiza la cobertura del sistema de recomendaciones
        Útil para optimización y presentación en entrevistas
        """
        from django.contrib.auth.models import User
        
        if not user_ids_sample:
            # Muestra de usuarios activos
            user_ids_sample = User.objects.filter(
                reviews__isnull=False
            ).distinct().values_list('id', flat=True)[:100]
        
        coverage_stats = {
            'users_analyzed': len(user_ids_sample),
            'users_with_recommendations': 0,
            'avg_recommendations_per_user': 0,
            'total_recommendations': 0
        }
        
        total_recs = 0
        
        for user_id in user_ids_sample:
            recs = RecommendationService.get_product_recommendations(user_id)
            if recs:
                coverage_stats['users_with_recommendations'] += 1
                total_recs += len(recs)
        
        coverage_stats['total_recommendations'] = total_recs
        coverage_stats['avg_recommendations_per_user'] = (
            total_recs / len(user_ids_sample) if user_ids_sample else 0
        )
        coverage_stats['coverage_percentage'] = (
            coverage_stats['users_with_recommendations'] / len(user_ids_sample) * 100
            if user_ids_sample else 0
        )
        
        return coverage_stats
    
    @staticmethod
    def benchmark_recommendation_methods():
        """
        Compara performance entre diferentes métodos de recomendación
        """
        from django.contrib.auth.models import User
        import time
        
        # Obtener muestra de usuarios
        user_ids = User.objects.filter(
            reviews__isnull=False
        ).distinct().values_list('id', flat=True)[:10]
        
        methods = {
            'content_based': RecommendationService.get_product_recommendations,
            'collaborative': RecommendationService.get_collaborative_recommendations,
        }
        
        results = {}
        
        for method_name, method_func in methods.items():