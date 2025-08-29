# 1. Crear entorno virtual y instalar Django
python -m venv django_interview_prep
source django_interview_prep/bin/activate  # En Windows: django_interview_prep\Scripts\activate
pip install django==4.2.7 python-decouple

# 2. Crear proyecto con estructura profesional
django-admin startproject interview_project .

# 3. Reestructurar settings
mkdir interview_project/settings
touch interview_project/settings/__init__.py
touch interview_project/settings/base.py
touch interview_project/settings/development.py
touch interview_project/settings/production.py

# 4. Crear aplicación principal
python manage.py startapp core
python manage.py startapp users
python manage.py startapp blog

# 5. Crear estructura de directorios adicional
mkdir -p static/css static/js static/img
mkdir -p media/uploads
mkdir templates
mkdir requirements

# 6. Configurar archivos de requirements
touch requirements/base.txt
touch requirements/development.txt
touch requirements/production.txt

# 7. Crear archivo de variables de entorno
touch .env
echo ".env" >> .gitignore
echo "media/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore