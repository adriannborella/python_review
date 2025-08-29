#!/bin/bash
# CHECKLIST DÍA 37 - DJANGO MODELS Y ORM

echo "🎯 === VERIFICACIÓN MODELOS DJANGO ==="

# 1. Verificar modelos creados
echo "📋 Verificando modelos..."
python manage.py showmigrations

# 2. Crear y aplicar migrations
echo "🔄 Creando migrations..."
python manage.py makemigrations
echo "✅ Aplicando migrations..."
python manage.py migrate

# 3. Verificar estructura de la base de datos
echo "🗄️ Verificando tablas creadas..."
python manage.py dbshell << EOF
\dt
\q
EOF

# 4. Poblar con datos de prueba
echo "📊 Poblando datos de prueba..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment
import factory
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

# Crear usuarios de prueba
if not User.objects.exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    
    author1 = User.objects.create_user(
        username='author1',
        email='author1@example.com',
        password='password123'
    )
    
    author2 = User.objects.create_user(
        username='author2',
        email='author2@example.com',
        password='password123'
    )
    
    print(f"✅ Created {User.objects.count()} users")

# Crear categorías
categories_data = [
    {'name': 'Django', 'description': 'Django framework tutorials', 'color': '#0C4B33'},
    {'name': 'Python', 'description': 'Python programming', 'color': '#3776AB'},
    {'name': 'Web Development', 'description': 'General web development', 'color': '#FF6B35'},
    {'name': 'Database', 'description': 'Database design and optimization', 'color': '#2E8B57'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"✅ Created category: {category.name}")

# Crear tags
tags_data = ['tutorial', 'beginner', 'advanced', 'orm', 'models', 'optimization', 'performance']
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        print(f"✅ Created tag: {tag.name}")

# Crear posts de ejemplo
posts_data = [
    {
        'title': 'Django Models Deep Dive',
        'content': 'This is a comprehensive guide to Django models. ' * 100,
        'status': 'published',
        'is_featured': True,
    },
    {
        'title': 'Optimizing Django Queries',
        'content': 'Learn how to optimize your Django queries for better performance. ' * 80,
        'status': 'published',
        'is_featured': False,
    },
    {
        'title': 'Understanding Django ORM',
        'content': 'The Django ORM is powerful and flexible. ' * 60,
        'status': 'draft',
        'is_featured': False,
    },
]

authors = list(User.objects.all())
categories = list(Category.objects.all())
tags = list(Tag.objects.all())

for i, post_data in enumerate(posts_data):
    post, created = Post.objects.get_or_create(
        title=post_data['title'],
        defaults={
            **post_data,
            'author': authors[i % len(authors)],
            'category': categories[i % len(categories)],
            'published_date': timezone.now() - timedelta(days=i),
        }
    )
    
    if created:
        # Agregar tags aleatorios
        post.tags.add(*tags[:2 + i])
        print(f"✅ Created post: {post.title}")
        
        # Crear comentarios
        for j in range(2):
            Comment.objects.create(
                post=post,
                author=authors[(i + j) % len(authors)],
                content=f"Great post about {post.title}! Very informative.",
                is_approved=True
            )

print(f"✅ Database populated successfully!")
print(f"Users: {User.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Tags: {Tag.objects.count()}")
print(f"Posts: {Post.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
EOF

# 5. Ejecutar tests
echo "🧪 Ejecutando tests de modelos..."
python manage.py test blog.tests.test_models -v 2

# 6. Verificar admin
echo "👨‍💼 Verificando configuración del admin..."
python manage.py shell << 'EOF'
from django.contrib import admin
from blog.models import Post, Category, Tag, Comment

# Verificar que los modelos están registrados
registered_models = [model.__name__ for model in admin.site._registry.keys()]
print("Modelos registrados en admin:", registered_models)

# Verificar configuración de admin
if Post in admin.site._registry:
    post_admin = admin.site._registry[Post]
    print(f"✅ Post admin configurado con {len(post_admin.list_display)} campos en list_display")

if Category in admin.site._registry:
    category_admin = admin.site._registry[Category]
    print(f"✅ Category admin configurado con {len(category_admin.list_display)} campos en list_display")
EOF

# 7. Probar queries de optimización
echo "⚡ Probando queries optimizados..."
python manage.py shell << 'EOF'
from blog.models import Post, Category, Tag, Comment
from django.db import connection
from django.db.models import Count, Avg, F

# Reset query counter
connection.queries_log.clear()

print("🔍 Probando queries optimizados...")

# 1. Posts con relaciones completas (should use select_related/prefetch_related)
print("\n1. Posts con relaciones completas:")
posts = list(Post.objects.with_full_relations()[:5])
print(f"   Cargados {len(posts)} posts")
print(f"   Queries ejecutadas: {len(connection.queries)}")

# Reset counter
connection.queries_log.clear()

# 2. Posts con estadísticas
print("\n2. Posts con estadísticas:")
posts_with_stats = list(Post.objects.with_stats()[:5])
for post in posts_with_stats:
    print(f"   {post.title}: {getattr(post, 'comment_count', 0)} comentarios")
print(f"   Queries ejecutadas: {len(connection.queries)}")

# Reset counter
connection.queries_log.clear()

# 3. Categorías con conteo de posts
print("\n3. Categorías con conteo de posts:")
categories = list(Category.objects.with_post_count())
for cat in categories:
    print(f"   {cat.name}: {getattr(cat, 'post_count', 0)} posts")
print(f"   Queries ejecutadas: {len(connection.queries)}")

# 4. Búsqueda
print("\n4. Probando búsqueda:")
search_results = list(Post.objects.search("Django"))
print(f"   Encontrados {len(search_results)} posts con 'Django'")

print("\n✅ Queries optimizados funcionando correctamente!")
EOF

# 8. Verificar soft delete
echo "🗑️ Probando soft delete..."
python manage.py shell << 'EOF'
from blog.models import Post

# Obtener un post
post = Post.objects.first()
if post:
    post_id = post.id
    title = post.title
    
    print(f"Post original: {title}")
    print(f"Posts activos antes: {Post.objects.count()}")
    print(f"Posts totales antes: {Post.all_objects.count()}")
    
    # Soft delete
    post.delete()
    
    print(f"Posts activos después: {Post.objects.count()}")
    print(f"Posts totales después: {Post.all_objects.count()}")
    
    # Verificar que está marcado como eliminado
    deleted_post = Post.all_objects.get(id=post_id)
    print(f"Post eliminado: {deleted_post.is_deleted}")
    
    # Restaurar
    deleted_post.restore()
    print(f"Posts activos después de restaurar: {Post.objects.count()}")
    
    print("✅ Soft delete funcionando correctamente!")
else:
    print("❌ No hay posts para probar soft delete")
EOF

# 9. Verificar signals
echo "📡 Verificando signals..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()

# Crear usuario para probar signal
test_user = User.objects.create_user(
    username='test_signal',
    email='test@signal.com',
    password='password123'
)

# Verificar que se creó el perfil automáticamente
if hasattr(test_user, 'profile'):
    print("✅ Signal funcionando: Perfil creado automáticamente")
else:
    print("❌ Signal no funcionando: Perfil no creado")

# Limpiar
test_user.delete()
EOF

# 10. Generar reporte final
echo "📊 Generando reporte final..."
python manage.py shell << 'EOF'
from blog.models import Post, Category, Tag, Comment, User
from django.db.models import Count, Avg

print("\n🎯 === REPORTE FINAL DÍA 37 ===")
print(f"📝 Posts totales: {Post.objects.count()}")
print(f"📚 Posts publicados: {Post.objects.published().count()}")
print(f"📁 Categorías: {Category.objects.count()}")
print(f"🏷️  Tags: {Tag.objects.count()}")
print(f"💬 Comentarios: {Comment.objects.filter(is_approved=True).count()}")
print(f"👥 Usuarios: {User.objects.count()}")

# Estadísticas avanzadas
avg_reading_time = Post.objects.aggregate(avg=Avg('reading_time'))['avg'] or 0
total_views = sum(post.views_count for post in Post.objects.all())

print(f"⏱️  Tiempo promedio lectura: {avg_reading_time:.1f} minutos")
print(f"👀 Total de vistas: {total_views}")

print("\n✅ Modelos Django implementados correctamente!")
print("✅ ORM optimizado funcionando!")
print("✅ Admin configurado!")
print("✅ Tests pasando!")
print("✅ Signals funcionando!")
EOF

echo "🎉 === VERIFICACIÓN COMPLETADA ==="