# ================================
# DJANGO CRUD COMPLETO - DÍA 40
# ================================

# ===== 1. MODELS (articles/models.py) =====
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

# ===== 2. FORMS (articles/forms.py) =====
from django import forms
from django.utils.text import slugify
from .models import Article, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'status', 'featured_image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your article content here...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            if len(tag_list) > 10:
                raise forms.ValidationError("Maximum 10 tags allowed.")
        return tags
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

class ArticleSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...'
        }),
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Article.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

# ===== 3. VIEWS (articles/views.py) =====
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Article, Category
from .forms import ArticleForm, ArticleSearchForm

# ===== FUNCTION-BASED VIEWS =====
def article_list(request):
    """FBV: Lista de artículos con búsqueda y filtros"""
    articles = Article.objects.select_related('author', 'category').filter(status='published')
    form = ArticleSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data['category']
        status = form.cleaned_data['status']
        
        if query:
            articles = articles.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(tags__icontains=query)
            )
        
        if category:
            articles = articles.filter(category=category)
        
        if status:
            articles = articles.filter(status=status)
    
    # Paginación
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_articles': articles.count()
    }
    return render(request, 'articles/list.html', context)

def article_detail(request, slug):
    """FBV: Detalle de artículo"""
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Artículos relacionados
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id)[:3]
    
    context = {
        'article': article,
        'related_articles': related_articles
    }
    return render(request, 'articles/detail.html', context)

# ===== CLASS-BASED VIEWS =====
class ArticleListView(ListView):
    """CBV: Lista de artículos"""
    model = Article
    template_name = 'articles/cbv_list.html'
    context_object_name = 'articles'
    paginate_by = 6
    
    def get_queryset(self):
        return Article.objects.select_related('author', 'category').filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleDetailView(DetailView):
    """CBV: Detalle de artículo"""
    model = Article
    template_name = 'articles/cbv_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Article.objects.filter(status='published')

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """CBV: Crear artículo"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create.html'
    success_url = reverse_lazy('article_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Article created successfully!')
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """CBV: Actualizar artículo"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/update.html'
    slug_field = 'slug'
    
    def get_queryset(self):
        # Solo el autor puede editar
        return Article.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Article updated successfully!')
        return super().form_valid(form)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """CBV: Eliminar artículo"""
    model = Article
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('article_list')
    slug_field = 'slug'
    
    def get_queryset(self):
        # Solo el autor puede eliminar
        return Article.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Article deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ===== DASHBOARD VIEW =====
@login_required
def dashboard(request):
    """Dashboard del usuario"""
    user_articles = Article.objects.filter(author=request.user)
    
    stats = {
        'total_articles': user_articles.count(),
        'published': user_articles.filter(status='published').count(),
        'drafts': user_articles.filter(status='draft').count(),
        'archived': user_articles.filter(status='archived').count(),
    }
    
    recent_articles = user_articles.order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_articles': recent_articles
    }
    return render(request, 'articles/dashboard.html', context)

# ===== 4. URLS (articles/urls.py) =====
from django.urls import path
from . import views

urlpatterns = [
    # Function-based views
    path('', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Class-based views
    path('cbv/', views.ArticleListView.as_view(), name='article_cbv_list'),
    path('cbv/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_cbv_detail'),
    
    # CRUD operations
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('update/<slug:slug>/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('delete/<slug:slug>/', views.ArticleDeleteView.as_view(), name='article_delete'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]

# ===== 5. TEMPLATE FILTERS (articles/templatetags/article_extras.py) =====
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def truncate_words_html(value, arg):
    """Trunca palabras preservando HTML"""
    try:
        length = int(arg)
    except ValueError:
        return value
    
    words = value.split()
    if len(words) <= length:
        return value
    
    truncated = ' '.join(words[:length])
    return mark_safe(f"{truncated}...")

@register.filter
def reading_time(value):
    """Calcula tiempo de lectura estimado"""
    word_count = len(value.split())
    minutes = max(1, word_count // 200)  # 200 words per minute
    return f"{minutes} min read"

@register.simple_tag
def article_status_badge(status):
    """Genera badge HTML para el status"""
    badge_classes = {
        'published': 'badge bg-success',
        'draft': 'badge bg-warning',
        'archived': 'badge bg-secondary'
    }
    
    badge_class = badge_classes.get(status, 'badge bg-light')
    return format_html(f'<span class="{badge_class}">{status.title()}</span>')

@register.inclusion_tag('articles/tags/popular_tags.html')
def show_popular_tags(limit=10):
    """Template tag de inclusión para tags populares"""
    from ..models import Article
    
    # Obtener todos los tags
    all_tags = []
    for article in Article.objects.filter(status='published'):
        all_tags.extend(article.get_tags_list())
    
    # Contar frecuencia
    from collections import Counter
    tag_counts = Counter(all_tags).most_common(limit)
    
    return {'tags': tag_counts}

# ===== 6. CONTEXT PROCESSORS (articles/context_processors.py) =====
from .models import Category, Article

def global_context(request):
    """Context processor para variables globales"""
    return {
        'all_categories': Category.objects.all()[:5],
        'recent_articles': Article.objects.filter(status='published')[:3],
        'site_stats': {
            'total_articles': Article.objects.filter(status='published').count(),
            'total_categories': Category.objects.count(),
        }
    }

# ===== 7. ADMIN CONFIGURATION (articles/admin.py) =====
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'created_at']
    search_fields = ['name', 'description']
    
    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = 'Articles'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'status_badge']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'featured_image', 'tags')
        }),
        ('Publication', {
            'fields': ('status', 'published_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_badge(self, obj):
        colors = {
            'published': 'green',
            'draft': 'orange',
            'archived': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

# ===== COMANDOS DE GESTIÓN (management/commands/populate_articles.py) =====
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Article, Category
from faker import Faker

class Command(BaseCommand):
    help = 'Populate database with sample articles'
    
    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=10, help='Number of articles to create')
    
    def handle(self, *args, **options):
        fake = Faker()
        
        # Crear categorías si no existen
        categories = ['Technology', 'Science', 'Health', 'Travel', 'Food']
        for cat_name in categories:
            Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': fake.text(max_nb_chars=200)}
            )
        
        # Crear artículos
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Create some users first.'))
            return
        
        categories = list(Category.objects.all())
        
        for i in range(options['number']):
            article = Article.objects.create(
                title=fake.sentence(nb_words=4),
                slug=fake.slug(),
                author=fake.choice(users),
                category=fake.choice(categories),
                content=fake.text(max_nb_chars=2000),
                status=fake.choice(['draft', 'published', 'archived']),
                tags=', '.join(fake.words(nb=3))
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created article: {article.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {options["number"]} articles!')
        )