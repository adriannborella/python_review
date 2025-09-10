# E-commerce API - Estructura Completa del Proyecto
# Día 49: DRF Project

"""
ecommerce_api/
├── manage.py
├── requirements.txt
├── ecommerce_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── products/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── permissions.py
│   │   └── tests.py
│   └── orders/
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       └── tests.py
└── utils/
    ├── __init__.py
    ├── pagination.py
    ├── exceptions.py
    └── mixins.py
"""

# requirements.txt
REQUIREMENTS = """
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-filter==23.3
Pillow==10.0.1
psycopg2-binary==2.9.7
python-decouple==3.8
"""

print("Estructura del proyecto definida")
print("Instalación: pip install -r requirements.txt")