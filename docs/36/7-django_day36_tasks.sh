# CHECKLIST DÍA 36 - DJANGO ARCHITECTURE

echo "🎯 === VERIFICACIÓN DEL SETUP DJANGO ==="

# 1. Verificar estructura del proyecto
echo "📁 Verificando estructura del proyecto..."
tree -I '__pycache__|*.pyc|.git' -L 3

# 2. Verificar configuración de settings
echo "⚙️ Verificando configuración..."
python manage.py check --settings=interview_project.settings.development

# 3. Ejecutar migraciones
echo "🗄️ Aplicando migraciones..."
python manage.py migrate --settings=interview_project.settings.development

# 4. Crear superuser (opcional)
echo "👤 Creando superuser..."
python manage.py createsuperuser --settings=interview_project.settings.development

# 5. Recopilar archivos estáticos
echo "🎨 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --settings=interview_project.settings.development

# 6. Ejecutar servidor de desarrollo
echo "🚀 Iniciando servidor de desarrollo..."
python manage.py runserver --settings=interview_project.settings.development

# 7. Ejecutar tests
echo "🧪 Ejecutando tests..."
python manage.py test --settings=interview_project.settings.development

# 8. Verificar URLs
echo "🔗 Verificando configuración de URLs..."
python manage.py show_urls --settings=interview_project.settings.development

# COMANDOS ADICIONALES PARA DEBUGGING

# Verificar configuración actual
python manage.py diffsettings --settings=interview_project.settings.development

# Shell interactivo con configuración específica
python manage.py shell --settings=interview_project.settings.development

# Verificar modelos
python manage.py validate

# === ARCHIVO .env DE EJEMPLO ===
cat > .env << 'EOF'
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (para producción)
DB_NAME=interview_project
DB_USER=django_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Email Settings
DEFAULT_FROM_EMAIL=noreply@interviewproject.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Application Settings
MAINTENANCE_MODE=False
MAX_UPLOAD_SIZE=5242880
PAGINATION_SIZE=10
EOF

# === REQUIREMENTS FILES ===

# requirements/base.txt
cat > requirements/base.txt << 'EOF'
Django==4.2.7
python-decouple==3.8
Pillow==10.0.1
EOF

# requirements/development.txt
cat > requirements/development.txt << 'EOF'
-r base.txt
django-debug-toolbar==4.2.0
django-extensions==3.2.3
ipython==8.15.0
pytest-django==4.5.2
factory-boy==3.3.0
EOF

# requirements/production.txt
cat > requirements/production.txt << 'EOF'
-r base.txt
gunicorn==21.2.0
psycopg2-binary==2.9.7
whitenoise==6.5.0
sentry-sdk==1.32.0
redis==5.0.0
celery==5.3.1
EOF

# === ARCHIVOS ESTÁTICOS BÁSICOS ===

# static/css/main.css
mkdir -p static/css
cat > static/css/main.css << 'EOF'
/* Custom styles for Interview Project */

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
}

.navbar-brand {
    font-weight: bold;
}

.jumbotron {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
    transition: transform 0.2s ease-in-out;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

footer {
    margin-top: auto;
}

/* Maintenance mode styles */
.maintenance-mode {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
EOF

# static/js/main.js
mkdir -p static/js
cat > static/js/main.js << 'EOF'
// Main JavaScript for Interview Project

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    console.log('Interview Project loaded successfully!');
});
EOF

echo "✅ === SETUP COMPLETADO ==="
echo "🌐 Visita http://127.0.0.1:8000/ para ver tu aplicación"
echo "⚡ Admin: http://127.0.0.1:8000/admin/"
echo "📊 Dashboard: http://127.0.0.1:8000/dashboard/"
echo "🔧 API Status: http://127.0.0.1:8000/api/v1/core/status/"