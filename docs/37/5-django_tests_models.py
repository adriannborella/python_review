# blog/tests/test_models.py - Tests comprehensivos para modelos
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
import factory
from blog.models import Category, Tag, Post, Comment
from blog.utils import BlogUtils

User = get_user_model()

# Factories para crear datos de prueba
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=200)
    color = "#007bff"
    is_active = True

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
    
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=100)

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('text', max_nb_chars=1000)
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    status = 'published'
    published_date = factory.LazyFunction(timezone.now)
    is_featured = False
    allow_comments = True

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
    
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('text', max_nb_chars=500)
    is_approved = True

class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""
    
    def setUp(self):
        self.category = CategoryFactory()
    
    def test_category_creation(self):
        """Test creación básica de categoría"""
        self.assertIsInstance(self.category, Category)
        self.assertTrue(self.category.is_active)
        self.assertIsNotNone(self.category.slug)
    
    def test_slug_generation(self):
        """Test generación automática de slug"""
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.slug, "test-category")
    
    def test_unique_slug_constraint(self):
        """Test constraint de slug único"""
        Category.objects.create(name="Test", slug="test")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Test 2", slug="test")
    
    def test_string_representation(self):
        """Test método __str__"""
        self.assertEqual(str(self.category), self.category.name)
    
    def test_get_absolute_url(self):
        """Test URL absoluta"""
        expected_url = reverse('blog:category_posts', kwargs={'slug': self.category.slug})
        self.assertEqual(self.category.get_absolute_url(), expected_url)
    
    def test_category_manager_active(self):
        """Test manager de categorías activas"""
        active_category = CategoryFactory(is_active=True)
        inactive_category = CategoryFactory(is_active=False)
        
        active_categories = Category.objects.active()
        self.assertIn(active_category, active_categories)
        self.assertNotIn(inactive_category, active_categories)
    
    def test_category_with_post_count(self):
        """Test anotación de conteo de posts"""
        category = CategoryFactory()
        PostFactory.create_batch(3, category=category)
        
        categories = Category.objects.with_post_count()
        category_with_count = categories.get(id=category.id)
        self.assertEqual(category_with_count.post_count, 3)

class PostModelTest(TestCase):
    """Tests para el modelo Post"""
    
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.post = PostFactory(author=self.user, category=self.category)
    
    def test_post_creation(self):
        """Test creación básica de post"""
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertIsNotNone(self.post.slug)
    
    def test_slug_generation_from_title(self):
        """Test generación de slug desde título"""
        post = Post.objects.create(
            title="This is a Test Post",
            content="Content here",
            author=self.user
        )
        self.assertEqual(post.slug, "this-is-a-test-post")
    
    def test_auto_excerpt_generation(self):
        """Test generación automática de excerpt"""
        long_content = "This is a very long content. " * 20
        post = Post.objects.create(
            title="Test",
            content=long_content,
            author=self.user
        )
        self.assertIsNotNone(post.excerpt)
        self.assertTrue(len(post.excerpt) <= 203)  # 200 + "..."
    
    def test_reading_time_calculation(self):
        """Test cálculo de tiempo de lectura"""
        content = "word " * 200  # 200 palabras = ~1 minuto
        post = Post.objects.create(
            title="Test",
            content=content,
            author=self.user
        )
        self.assertEqual(post.reading_time, 1)
    
    def test_auto_publish_date(self):
        """Test asignación automática de fecha de publicación"""
        post = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user,
            status='published'
        )
        self.assertIsNotNone(post.published_date)
    
    def test_is_published_property(self):
        """Test propiedad is_published"""
        # Post publicado
        published_post = PostFactory(
            status='published',
            published_date=timezone.now() - timedelta(hours=1)
        )
        self.assertTrue(published_post.is_published)
        
        # Post borrador
        draft_post = PostFactory(status='draft')
        self.assertFalse(draft_post.is_published)
        
        # Post programado para el futuro
        future_post = PostFactory(
            status='published',
            published_date=timezone.now() + timedelta(hours=1)
        )
        self.assertFalse(future_post.is_published)
    
    def test_get_related_posts(self):
        """Test obtención de posts relacionados"""
        tag1 = TagFactory(name="tag1")
        tag2 = TagFactory(name="tag2")
        
        # Post principal con tags
        main_post = PostFactory()
        main_post.tags.add(tag1, tag2)
        
        # Posts relacionados
        related_post1 = PostFactory()
        related_post1.tags.add(tag1)
        
        related_post2 = PostFactory()
        related_post2.tags.add(tag2)
        
        # Post no relacionado
        unrelated_post = PostFactory()
        
        related_posts = main_post.get_related_posts()
        
        self.assertIn(related_post1, related_posts)
        self.assertIn(related_post2, related_posts)
        self.assertNotIn(unrelated_post, related_posts)
        self.assertNotIn(main_post, related_posts)  # No debe incluirse a sí mismo
    
    def test_get_next_and_previous_posts(self):
        """Test navegación entre posts"""
        # Crear posts con fechas específicas
        old_post = PostFactory(
            published_date=timezone.now() - timedelta(days=2)
        )
        current_post = PostFactory(
            published_date=timezone.now() - timedelta(days=1)
        )
        new_post = PostFactory(
            published_date=timezone.now()
        )
        
        # Test post anterior
        previous = current_post.get_previous_post()
        self.assertEqual(previous, old_post)
        
        # Test post siguiente
        next_post = current_post.get_next_post()
        self.assertEqual(next_post, new_post)
    
    def test_post_manager_published(self):
        """Test manager de posts publicados"""
        published_post = PostFactory(status='published')
        draft_post = PostFactory(status='draft')
        
        published_posts = Post.objects.published()
        
        self.assertIn(published_post, published_posts)
        self.assertNotIn(draft_post, published_posts)
    
    def test_post_queryset_with_relations(self):
        """Test queryset optimizado con relaciones"""
        post = PostFactory()
        
        with self.assertNumQueries(1):  # Solo una query gracias a select_related
            posts = list(
                Post.objects.with_full_relations()
                .filter(id=post.id)
            )
            # Acceder a relaciones no debe generar queries adicionales
            str(posts[0].author.username)
            str(posts[0].category.name)

class CommentModelTest(TestCase):
    """Tests para el modelo Comment"""
    
    def setUp(self):
        self.post = PostFactory()
        self.user = UserFactory()
        self.comment = CommentFactory(post=self.post, author=self.user)
    
    def test_comment_creation(self):
        """Test creación básica de comentario"""
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertTrue(self.comment.is_approved)
    
    def test_reply_functionality(self):
        """Test funcionalidad de respuestas"""
        reply = CommentFactory(
            post=self.post,
            parent=self.comment
        )
        
        self.assertTrue(reply.is_reply)
        self.assertFalse(self.comment.is_reply)
        self.assertIn(reply, self.comment.get_replies())
    
    def test_string_representation(self):
        """Test método __str__"""
        expected = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(self.comment), expected)

class SoftDeleteModelTest(TestCase):
    """Tests para funcionalidad de soft delete"""
    
    def setUp(self):
        self.post = PostFactory()
    
    def test_soft_delete(self):
        """Test eliminación suave"""
        post_id = self.post.id
        
        # Soft delete
        self.post.delete()
        
        # No debe aparecer en queryset normal
        self.assertFalse(Post.objects.filter(id=post_id).exists())
        
        # Debe aparecer en all_objects
        self.assertTrue(Post.all_objects.filter(id=post_id).exists())
        
        # Debe tener deleted_at
        deleted_post = Post.all_objects.get(id=post_id)
        self.assertIsNotNone(deleted_post.deleted_at)
        self.assertTrue(deleted_post.is_deleted)
    
    def test_restore_functionality(self):
        """Test restauración de registro eliminado"""
        self.post.delete()
        
        # Restaurar
        deleted_post = Post.all_objects.get(id=self.post.id)
        deleted_post.restore()
        
        # Debe aparecer en queryset normal
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
        self.assertFalse(deleted_post.is_deleted)
    
    def test_hard_delete(self):
        """Test eliminación definitiva"""
        post_id = self.post.id
        
        # Hard delete
        self.post.hard_delete()
        
        # No debe existir en ningún manager
        self.assertFalse(Post.objects.filter(id=post_id).exists())
        self.assertFalse(Post.all_objects.filter(id=post_id).exists())

class BlogUtilsTest(TestCase):
    """Tests para utilidades del blog"""
    
    def test_generate_unique_slug(self):
        """Test generación de slug único"""
        # Crear post existente
        existing_post = PostFactory(title="Test Title")
        
        # Generar slug para nuevo post con mismo título
        new_slug = BlogUtils.generate_unique_slug(Post, "Test Title")
        
        self.assertNotEqual(new_slug, existing_post.slug)
        self.assertTrue(new_slug.startswith("test-title"))
    
    def test_calculate_reading_time(self):
        """Test cálculo de tiempo de lectura"""
        # 200 palabras = 1 minuto
        content = "word " * 200
        reading_time = BlogUtils.calculate_reading_time(content)
        self.assertEqual(reading_time, 1)
        
        # 400 palabras = 2 minutos
        content = "word " * 400
        reading_time = BlogUtils.calculate_reading_time(content)
        self.assertEqual(reading_time, 2)
        
        # Contenido vacío
        reading_time = BlogUtils.calculate_reading_time("")
        self.assertEqual(reading_time, 0)
    
    def test_generate_excerpt(self):
        """Test generación de excerpt"""
        long_text = "This is a very long text. " * 50
        excerpt = BlogUtils.generate_excerpt(long_text, max_length=100)
        
        self.assertLess(len(excerpt), len(long_text))
        self.assertTrue(excerpt.endswith("..."))
    
    def test_extract_keywords(self):
        """Test extracción de palabras clave"""
        content = "Django is a powerful web framework. Django makes development easy. Web development with Django is fun."
        keywords = BlogUtils.extract_keywords(content, max_keywords=5)
        
        self.assertIn("django", keywords)
        self.assertIn("development", keywords)
        self.assertNotIn("is", keywords)  # Stop word
        self.assertNotIn("a", keywords)   # Stop word

# Integration Tests
class BlogIntegrationTest(TestCase):
    """Tests de integración para el sistema de blog"""
    
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.tags = TagFactory.create_batch(3)
    
    def test_complete_post_workflow(self):
        """Test workflow completo de un post"""
        # Crear post borrador
        post = Post.objects.create(
            title="Test Post",
            content="This is test content. " * 100,  # ~200 palabras
            author=self.user,
            category=self.category,
            status='draft'
        )
        post.tags.add(*self.tags)
        
        # Verificar estado inicial
        self.assertEqual(post.status, 'draft')
        self.assertFalse(post.is_published)
        self.assertIsNone(post.published_date)
        
        # Publicar
        post.status = 'published'
        post.save()
        
        # Verificar estado publicado
        self.assertTrue(post.is_published)
        self.assertIsNotNone(post.published_date)
        self.assertEqual(post.reading_time, 1)  # ~200 palabras = 1 minuto
        
        # Crear comentario
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Great post!"
        )
        
        # Verificar relación
        self.assertIn(comment, post.comments.all())
        
        # Crear respuesta
        reply = Comment.objects.create(
            post=post,
            author=self.user,
            parent=comment,
            content="Thank you!"
        )
        
        # Verificar respuesta
        self.assertTrue(reply.is_reply)
        self.assertIn(reply, comment.get_replies())
    
    def test_post_search_functionality(self):
        """Test funcionalidad de búsqueda"""
        # Crear posts con contenido específico
        post1 = PostFactory(
            title="Django Tutorial",
            content="Learn Django web development"
        )
        post2 = PostFactory(
            title="Python Guide",
            content="Python programming basics"
        )
        post3 = PostFactory(
            title="Web Design",
            content="HTML and CSS fundamentals"
        )
        
        # Buscar por "Django"
        results = Post.objects.search("Django")
        self.assertIn(post1, results)
        self.assertNotIn(post2, results)
        self.assertNotIn(post3, results)
        
        # Buscar por "Python"
        results = Post.objects.search("Python")
        self.assertIn(post2, results)
        self.assertNotIn(post1, results)
        self.assertNotIn(post3, results)