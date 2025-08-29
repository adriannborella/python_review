# core/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DashboardView(TemplateView):
    """Vista del dashboard principal"""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Dashboard',
            'user_count': 100,  # Esto vendría de la base de datos
            'post_count': 50,   # Esto vendría de la base de datos
        })
        return context

class AboutView(TemplateView):
    """Vista de la página About"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'
        return context

class ContactView(FormView):
    """Vista del formulario de contacto"""
    template_name = 'core/contact.html'
    # form_class = ContactForm  # Definiremos esto más adelante
    success_url = reverse_lazy('core:contact_success')
    
    def form_valid(self, form):
        # Procesar el formulario
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        
        # Enviar email (en producción)
        try:
            send_mail(
                subject=f'Contact form submission from {name}',
                message=message,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(self.request, 'Your message has been sent successfully!')
            logger.info(f'Contact form submitted by {email}')
        except Exception as e:
            messages.error(self.request, 'There was an error sending your message.')
            logger.error(f'Error sending contact form: {e}')
        
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    """Vista de confirmación de contacto"""
    template_name = 'core/contact_success.html'

def health_check(request):
    """Health check endpoint para monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'django_version': '4.2.7',
        'debug': settings.DEBUG
    })

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)

# core/api/views.py
from django.http import JsonResponse
from django.views import View
import django

class SystemStatusAPIView(View):
    """API endpoint para el estado del sistema"""
    
    def get(self, request):
        return JsonResponse({
            'status': 'operational',
            'version': '1.0.0',
            'django_version': django.get_version(),
            'debug_mode': getattr(settings, 'DEBUG', False)
        })

class VersionAPIView(View):
    """API endpoint para la versión de la aplicación"""
    
    def get(self, request):
        return JsonResponse({
            'application_version': '1.0.0',
            'api_version': 'v1',
            'django_version': django.get_version(),
        })

# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core Application'
    
    def ready(self):
        """Llamado cuando la app está lista"""
        # Importar signals aquí si los hubiera
        # import core.signals
        pass