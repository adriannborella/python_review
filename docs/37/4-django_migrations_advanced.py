# Comandos para generar migrations
"""
# Crear migrations iniciales
python manage.py makemigrations users
python manage.py makemigrations blog
python manage.py makemigrations core

# Aplicar migrations
python manage.py migrate

# Ver migrations pendientes
python manage.py showmigrations

# Ver SQL de una migration específica
python manage.py sqlmigrate blog 0001

# Hacer rollback a una migration específica
python manage.py migrate blog 0001

# Crear migration vacía para operaciones customizadas
python manage.py makemigrations --empty blog
"""

# blog/migrations/0002_add_indexes.py - Migration con índices personalizados
from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('blog', '0001_initial'),
    ]
    
    operations = [
        # Índices para mejorar performance
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_post_status_published_date ON blog_post (status, published_date) WHERE status = 'published';",
            reverse_sql="DROP INDEX IF EXISTS idx_post_status_published_date;"
        ),
        
        # Índice compuesto para búsquedas
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_post_search ON blog_post USING gin(to_tsvector('english', title || ' ' || content));",
            reverse_sql="DROP INDEX IF EXISTS idx_post_search;"
        ),
        
        # Índice para comentarios aprobados
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_comment_approved_post ON blog_comment (post_id, is_approved, created_at) WHERE is_approved = true;",
            reverse_sql="DROP INDEX IF EXISTS idx_comment_approved_post;"
        ),
    ]

# blog/migrations/0003_data_migration.py - Data migration
from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    """Popula slugs para registros existentes"""
    Post = apps.get_model('blog', 'Post')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    
    # Generar slugs para posts
    for post in Post.objects.filter(slug=''):
        post.slug = slugify(post.title)
        # Asegurar uniqueness
        counter = 1
        original_slug = post.slug
        while Post.objects.filter(slug=post.slug).exists():
            post.slug = f"{original_slug}-{counter}"
            counter += 1
        post.save()
    
    # Generar slugs para categorías
    for category in Category.objects.filter(slug=''):
        category.slug = slugify(category.name)
        counter = 1
        original_slug = category.slug
        while Category.objects.filter(slug=category.slug).exists():
            category.slug = f"{original_slug}-{counter}"
            counter += 1
        category.save()
    
    # Generar slugs para tags
    for tag in Tag.objects.filter(slug=''):
        tag.slug = slugify(tag.name)
        counter = 1
        original_slug = tag.slug
        while Tag.objects.filter(slug=tag.slug).exists():
            tag.slug = f"{original_slug}-{counter}"
            counter += 1
        tag.save()

def reverse_populate_slugs(apps, schema_editor):
    """Reversa la data migration"""
    Post = apps.get_model('blog', 'Post')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    
    Post.objects.update(slug='')
    Category.objects.update(slug='')
    Tag.objects.update(slug='')

class Migration(migrations.Migration):
    
    dependencies = [
        ('blog', '0002_add_indexes'),
    ]
    
    operations = [
        migrations.RunPython(
            populate_slugs,
            reverse_populate_slugs
        ),
    ]

# blog/migrations/0004_add_full_text_search.py - Full text search
from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
    
    dependencies = [
        ('blog', '0003_data_migration'),
    ]
    
    operations = [
        # Habilitar extensión trigram (solo PostgreSQL)
        TrigramExtension(),
        
        # Añadir columna de búsqueda full text
        migrations.RunSQL(
            """
            ALTER TABLE blog_post 
            ADD COLUMN search_vector tsvector 
            GENERATED ALWAYS AS (
                to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, '') || ' ' || coalesce(excerpt, ''))
            ) STORED;
            """,
            reverse_sql="ALTER TABLE blog_post DROP COLUMN IF EXISTS search_vector;"
        ),
        
        # Crear índice GIN para búsqueda full text
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_post_search_vector ON blog_post USING gin(search_vector);",
            reverse_sql="DROP INDEX IF EXISTS idx_post_search_vector;"
        ),
        
        # Función para actualizar search_vector en updates
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION update_post_search_vector()
            RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := to_tsvector('english', coalesce(NEW.title, '') || ' ' || coalesce(NEW.content, '') || ' ' || coalesce(NEW.excerpt, ''));
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            reverse_sql="DROP FUNCTION IF EXISTS update_post_search_vector();"
        ),
        
        # Trigger para actualizar automáticamente
        migrations.RunSQL(
            """
            CREATE TRIGGER update_post_search_vector_trigger
            BEFORE INSERT OR UPDATE ON blog_post
            FOR EACH ROW EXECUTE FUNCTION update_post_search_vector();
            """,
            reverse_sql="DROP TRIGGER IF EXISTS update_post_search_vector_trigger ON blog_post;"
        ),
    ]

# blog/migrations/0005_optimize_queries.py - Optimización de queries
from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('blog', '0004_add_full_text_search'),
    ]
    
    operations = [
        # Añadir campos calculados para optimizar queries
        migrations.AddField(
            model_name='post',
            name='comments_count',
            field=models.PositiveIntegerField(default=0),
        ),
        
        migrations.AddField(
            model_name='category',
            name='posts_count',
            field=models.PositiveIntegerField(default=0),
        ),
        
        # Función para actualizar contadores
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION update_post_comments_count()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    UPDATE blog_post SET comments_count = comments_count + 1 
                    WHERE id = NEW.post_id AND NEW.is_approved = true;
                    RETURN NEW;
                ELSIF TG_OP = 'UPDATE' THEN
                    IF OLD.is_approved != NEW.is_approved THEN
                        IF NEW.is_approved = true THEN
                            UPDATE blog_post SET comments_count = comments_count + 1 WHERE id = NEW.post_id;
                        ELSE
                            UPDATE blog_post SET comments_count = comments_count - 1 WHERE id = NEW.post_id;
                        END IF;
                    END IF;
                    RETURN NEW;
                ELSIF TG_OP = 'DELETE' THEN
                    UPDATE blog_post SET comments_count = comments_count - 1 
                    WHERE id = OLD.post_id AND OLD.is_approved = true;
                    RETURN OLD;
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
            """,
            reverse_sql="DROP FUNCTION IF EXISTS update_post_comments_count();"
        ),
        
        # Trigger para comentarios
        migrations.RunSQL(
            """
            CREATE TRIGGER update_post_comments_count_trigger
            AFTER INSERT OR UPDATE OR DELETE ON blog_comment
            FOR EACH ROW EXECUTE FUNCTION update_post_comments_count();
            """,
            reverse_sql="DROP TRIGGER IF EXISTS update_post_comments_count_trigger ON blog_comment;"
        ),
        
        # Función para categorías
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION update_category_posts_count()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    IF NEW.category_id IS NOT NULL AND NEW.status = 'published' THEN
                        UPDATE blog_category SET posts_count = posts_count + 1 WHERE id = NEW.category_id;
                    END IF;
                    RETURN NEW;
                ELSIF TG_OP = 'UPDATE' THEN
                    -- Si cambió la categoría
                    IF OLD.category_id != NEW.category_id THEN
                        IF OLD.category_id IS NOT NULL AND OLD.status = 'published' THEN
                            UPDATE blog_category SET posts_count = posts_count - 1 WHERE id = OLD.category_id;
                        END IF;
                        IF NEW.category_id IS NOT NULL AND NEW.status = 'published' THEN
                            UPDATE blog_category SET posts_count = posts_count + 1 WHERE id = NEW.category_id;
                        END IF;
                    -- Si cambió el status
                    ELSIF OLD.status != NEW.status AND NEW.category_id IS NOT NULL THEN
                        IF NEW.status = 'published' AND OLD.status != 'published' THEN
                            UPDATE blog_category SET posts_count = posts_count + 1 WHERE id = NEW.category_id;
                        ELSIF NEW.status != 'published' AND OLD.status = 'published' THEN
                            UPDATE blog_category SET posts_count = posts_count - 1 WHERE id = NEW.category_id;
                        END IF;
                    END IF;
                    RETURN NEW;
                ELSIF TG_OP = 'DELETE' THEN
                    IF OLD.category_id IS NOT NULL AND OLD.status = 'published' THEN
                        UPDATE blog_category SET posts_count = posts_count - 1 WHERE id = OLD.category_id;
                    END IF;
                    RETURN OLD;
                END IF;
                RETURN NULL;
            END;
            $ LANGUAGE plpgsql;
            """,
            reverse_sql="DROP FUNCTION IF EXISTS update_category_posts_count();"
        ),
        
        # Trigger para categorías
        migrations.RunSQL(
            """
            CREATE TRIGGER update_category_posts_count_trigger
            AFTER INSERT OR UPDATE OR DELETE ON blog_post
            FOR EACH ROW EXECUTE FUNCTION update_category_posts_count();
            """,
            reverse_sql="DROP TRIGGER IF EXISTS update_category_posts_count_trigger ON blog_post;"
        ),
        
        # Inicializar contadores existentes
        migrations.RunSQL(
            """
            UPDATE blog_post SET comments_count = (
                SELECT COUNT(*) FROM blog_comment 
                WHERE post_id = blog_post.id AND is_approved = true
            );
            
            UPDATE blog_category SET posts_count = (
                SELECT COUNT(*) FROM blog_post 
                WHERE category_id = blog_category.id AND status = 'published'
            );
            """,
            reverse_sql="UPDATE blog_post SET comments_count = 0; UPDATE blog_category SET posts_count = 0;"
        ),
    ]

# Comando de management para migrations complejas
# blog/management/commands/migrate_blog_data.py
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import Post, Category, Tag
from blog.utils import BlogUtils
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migra y optimiza datos del blog'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--update-reading-times',
            action='store_true',
            help='Actualiza tiempos de lectura de todos los posts'
        )
        parser.add_argument(
            '--generate-excerpts',
            action='store_true',
            help='Genera excerpts para posts que no los tienen'
        )
        parser.add_argument(
            '--fix-slugs',
            action='store_true',
            help='Repara slugs duplicados'
        )
    
    def handle(self, *args, **options):
        if options['update_reading_times']:
            self.update_reading_times()
        
        if options['generate_excerpts']:
            self.generate_excerpts()
        
        if options['fix_slugs']:
            self.fix_slugs()
    
    @transaction.atomic
    def update_reading_times(self):
        """Actualiza tiempos de lectura"""
        self.stdout.write('Updating reading times...')
        
        posts = Post.objects.all()
        updated_count = 0
        
        for post in posts:
            old_time = post.reading_time
            new_time = BlogUtils.calculate_reading_time(post.content)
            
            if old_time != new_time:
                post.reading_time = new_time
                post.save(update_fields=['reading_time'])
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Updated reading times for {updated_count} posts')
        )
    
    @transaction.atomic
    def generate_excerpts(self):
        """Genera excerpts faltantes"""
        self.stdout.write('Generating excerpts...')
        
        posts = Post.objects.filter(excerpt='')
        updated_count = 0
        
        for post in posts:
            post.excerpt = BlogUtils.generate_excerpt(post.content)
            post.save(update_fields=['excerpt'])
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated excerpts for {updated_count} posts')
        )
    
    @transaction.atomic
    def fix_slugs(self):
        """Repara slugs duplicados"""
        self.stdout.write('Fixing duplicate slugs...')
        
        # Reparar posts
        posts_fixed = 0
        for post in Post.objects.all():
            original_slug = post.slug
            new_slug = BlogUtils.generate_unique_slug(Post, post.title, post)
            if original_slug != new_slug:
                post.slug = new_slug
                post.save(update_fields=['slug'])
                posts_fixed += 1
        
        # Reparar categorías
        categories_fixed = 0
        for category in Category.objects.all():
            original_slug = category.slug
            new_slug = BlogUtils.generate_unique_slug(Category, category.name, category)
            if original_slug != new_slug:
                category.slug = new_slug
                category.save(update_fields=['slug'])
                categories_fixed += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Fixed slugs: {posts_fixed} posts, {categories_fixed} categories'
            )
        )