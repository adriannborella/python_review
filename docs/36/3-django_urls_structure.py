# interview_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core import views as core_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home page
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    
    # Core app
    path('', include('core.urls', namespace='core')),
    
    # Users app
    path('users/', include('users.urls', namespace='users')),
    
    # Blog app
    path('blog/', include('blog.urls', namespace='blog')),
    
    # API endpoints
    path('api/v1/', include([
        path('core/', include('core.api_urls', namespace='core-api')),
        path('users/', include('users.api_urls', namespace='users-api')),
        path('blog/', include('blog.api_urls', namespace='blog-api')),
    ])),
    
    # Health check
    path('health/', core_views.health_check, name='health_check'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

# Admin customization
admin.site.site_header = "Interview Project Admin"
admin.site.site_title = "Interview Project Admin Portal"
admin.site.index_title = "Welcome to Interview Project Administration"

# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # About page
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
]

# core/api_urls.py
from django.urls import path
from .api import views as api_views

app_name = 'core-api'

urlpatterns = [
    # API endpoints
    path('status/', api_views.SystemStatusAPIView.as_view(), name='system_status'),
    path('version/', api_views.VersionAPIView.as_view(), name='version'),
]

# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    # Password management
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
]

# blog/urls.py
from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list and detail
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Categories and tags
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostsView.as_view(), name='tag_posts'),
    
    # Archive views
    re_path(
        r'^archive/(?P<year>[0-9]{4})/$',
        views.PostYearArchiveView.as_view(),
        name='post_year_archive'
    ),
    re_path(
        r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.PostMonthArchiveView.as_view(),
        name='post_month_archive'
    ),
    
    # Search
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    
    # RSS Feed
    path('feed/', views.PostsFeed(), name='posts_feed'),
]