# models.py - Sistema E-commerce Avanzado

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid

class BaseModel(models.Model):
    """Modelo base con timestamps y soft delete"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class Category(BaseModel):
    """Categorías jerárquicas de productos"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    # Relación jerárquica
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children'
    )
    
    # Metadata para SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Brand(BaseModel):
    """Marcas de productos"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class ProductManager(models.Manager):
    """Manager personalizado para productos"""
    
    def active(self):
        return self.filter(is_active=True)
    
    def featured(self):
        return self.active().filter(is_featured=True)
    
    def by_category(self, category_slug):
        return self.active().filter(category__slug=category_slug)

class Product(BaseModel):
    """Modelo principal de productos"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    
    # Pricing
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    compare_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Precio antes del descuento"
    )
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True, 
        null=True,
        help_text="Precio de costo interno"
    )
    
    # Product Info
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=50, blank=True, unique=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    # Relations
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Flags
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    track_inventory = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # JSON field para datos flexibles
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Atributos específicos del producto"
    )
    
    # Manager personalizado
    objects = ProductManager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def discount_percentage(self):
        """Calcula el porcentaje de descuento"""
        if self.compare_price and self.compare_price > self.price:
            return round(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    @property
    def is_on_sale(self):
        """Verifica si el producto está en oferta"""
        return self.compare_price and self.compare_price > self.price
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'price']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

class ProductImage(BaseModel):
    """Imágenes de productos"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['product', 'is_main']  # Solo una imagen principal

class ProductVariant(BaseModel):
    """Variantes de productos (talla, color, etc.)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    name = models.CharField(max_length=100)  # "Rojo - L"
    sku = models.CharField(max_length=50, unique=True)
    price_adjustment = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text="Ajuste al precio base"
    )
    
    # Attributes específicos
    attributes = models.JSONField(
        default=dict,
        help_text="Color, talla, etc."
    )
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"

class Inventory(BaseModel):
    """Control de inventario"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='inventory'
    )
    
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
    @property
    def is_low_stock(self):
        return self.available_quantity <= self.min_stock_level
    
    @property
    def is_in_stock(self):
        return self.available_quantity > 0
    
    def __str__(self):
        item = self.variant or self.product
        return f"{item} - Stock: {self.available_quantity}"

class Review(BaseModel):
    """Reseñas de productos"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Moderación
    is_approved = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['product', 'user']  # Una reseña por usuario
        ordering = ['-created_at']

# Signals para automatizar procesos
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Product)
def create_product_inventory(sender, instance, created, **kwargs):
    """Crea automáticamente el inventario cuando se crea un producto"""
    if created and instance.track_inventory:
        Inventory.objects.create(product=instance)

@receiver(post_save, sender=ProductImage)
def ensure_single_main_image(sender, instance, **kwargs):
    """Asegura que solo haya una imagen principal por producto"""
    if instance.is_main:
        ProductImage.objects.filter(
            product=instance.product,
            is_main=True
        ).exclude(id=instance.id).update(is_main=False)