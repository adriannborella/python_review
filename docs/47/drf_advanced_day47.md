# Production Deployment - Día 47

## 🎯 Objetivos del Día
- Dominar Docker containerization para Django
- Implementar CI/CD pipelines completos
- Configurar zero-downtime deployment strategies
- Setup infrastructure as code
- Prepararse para preguntas sobre DevOps y deployment

---

## 📚 HORA 1: TEORÍA - CONTAINERIZATION Y CI/CD

### 1. Docker Multi-Stage Builds

#### Production-Ready Dockerfile
```dockerfile
# Dockerfile - Multi-stage build optimizado
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
USER appuser
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base as production

# Copy application code
COPY --chown=appuser:appuser . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Security: run as non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Production command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "myproject.wsgi:application"]
```

#### Docker Compose para Development
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: .
      target: development
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery:
    build:
      context: .
      target: development
    command: celery -A myproject worker -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    build:
      context: .
      target: development
    command: celery -A myproject beat -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

#### Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build:
      context: .
      target: production
    restart: unless-stopped
    environment:
      - DEBUG=0
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - SENTRY_DSN=${SENTRY_DSN}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - "8000"
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web
    restart: unless-stopped

  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    expose:
      - "5432"

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_prod_data:/data
    expose:
      - "6379"

  celery:
    build:
      context: .
      target: production
    restart: unless-stopped
    command: celery -A myproject worker -l info --concurrency=4
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis

volumes:
  postgres_prod_data:
  redis_prod_data:
  static_volume:
  media_volume:
```

### 2. CI/CD Pipeline Implementation

#### GitHub Actions Workflow
```yaml
# .github/workflows/django.yml
name: Django CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: 3.11
  NODE_VERSION: 18

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check .
        isort --check-only .
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
        SECRET_KEY: test-secret-key
      run: |
        python manage.py test --parallel --keepdb
        coverage run --source='.' manage.py test
        coverage report --fail-under=80
        coverage xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  security:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security checks
      run: |
        pip install safety bandit
        safety check
        bandit -r . -x tests/
    
    - name: Django security check
      run: |
        pip install -r requirements.txt
        python manage.py check --deploy

  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to DockerHub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        target: production
        push: true
        tags: |
          myapp/django:latest
          myapp/django:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "Deploying to production server..."
        # SSH into production server and update containers
        ssh -o StrictHostKeyChecking=no ${{ secrets.PROD_SERVER_USER }}@${{ secrets.PROD_SERVER_HOST }} << 'EOF'
          cd /opt/myapp
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d --no-deps web
          docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
          docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
        EOF
```

### 3. Database Migration Strategies

#### Safe Migration Practices
```python
# migration_utils.py
from django.core.management.base import BaseCommand
from django.db import transaction, connection
import time

class SafeMigrationMixin:
    """Mixin for safe production migrations"""
    
    def run_with_lock(self, migration_func):
        """Run migration with advisory lock"""
        with connection.cursor() as cursor:
            # Acquire advisory lock
            cursor.execute("SELECT pg_advisory_lock(12345)")
            
            try:
                with transaction.atomic():
                    migration_func()
            finally:
                # Release advisory lock
                cursor.execute("SELECT pg_advisory_unlock(12345)")
    
    def create_index_concurrently(self, table_name, index_name, columns):
        """Create index without blocking writes"""
        with connection.cursor() as cursor:
            sql = f"""
                CREATE INDEX CONCURRENTLY {index_name} 
                ON {table_name} ({', '.join(columns)})
            """
            cursor.execute(sql)
    
    def add_column_with_default(self, table_name, column_name, column_type, default_value):
        """Add column with default value safely"""
        with connection.cursor() as cursor:
            # Step 1: Add column without default
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            
            # Step 2: Update existing rows in batches
            batch_size = 1000
            offset = 0
            
            while True:
                cursor.execute(f"""
                    UPDATE {table_name} 
                    SET {column_name} = %s 
                    WHERE {column_name} IS NULL 
                    AND id IN (
                        SELECT id FROM {table_name} 
                        WHERE {column_name} IS NULL 
                        LIMIT %s OFFSET %s
                    )
                """, [default_value, batch_size, offset])
                
                if cursor.rowcount == 0:
                    break
                
                offset += batch_size
                time.sleep(0.1)  # Brief pause to avoid overwhelming DB
            
            # Step 3: Add NOT NULL constraint
            cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL")

# Zero-downtime migration example
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]
    
    operations = [
        # Step 1: Add nullable column
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        # Step 2: Populate data (separate migration)
        # Step 3: Make non-nullable (separate migration)
    ]
```

---

## ⚡ HORA 2: IMPLEMENTACIÓN - DEPLOYMENT AUTOMATION

### 1. Complete Deployment Scripts

#### Deployment Automation
```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e  # Exit on any error

# Configuration
APP_NAME="myapp"
DEPLOY_USER="deploy"
PROD_SERVER="production.myapp.com"
DOCKER_IMAGE="myapp/django:latest"
BACKUP_RETENTION_DAYS=7

echo "🚀 Starting deployment process..."

# Pre-deployment checks
echo "📋 Running pre-deployment checks..."

# Check if all required environment variables are set
required_vars=("DATABASE_URL" "REDIS_URL" "SECRET_KEY" "SENTRY_DSN")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var environment variable is not set"
        exit 1
    fi
done

# Health check current production
echo "🏥 Checking current production health..."
if ! curl -f https://$PROD_SERVER/health/ > /dev/null 2>&1; then
    echo "⚠️  Warning: Current production is not healthy"
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Database backup
echo "💾 Creating database backup..."
ssh $DEPLOY_USER@$PROD_SERVER << 'EOF'
    cd /opt/myapp
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U $DB_USER $DB_NAME > backups/$BACKUP_FILE
    
    # Clean old backups
    find backups/ -name "backup_*.sql" -mtime +$BACKUP_RETENTION_DAYS -delete
EOF

# Pull latest image
echo "📦 Pulling latest Docker image..."
ssh $DEPLOY_USER@$PROD_SERVER << EOF
    cd /opt/myapp
    docker pull $DOCKER_IMAGE
EOF

# Run migrations
echo "🗄️  Running database migrations..."
ssh $DEPLOY_USER@$PROD_SERVER << 'EOF'
    cd /opt/myapp
    
    # Run migrations in maintenance mode
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --check
    if [ $? -eq 0 ]; then
        echo "✅ No pending migrations"
    else
        echo "📝 Running migrations..."
        docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
    fi
EOF

# Blue-green deployment
echo "🔄 Performing blue-green deployment..."
ssh $DEPLOY_USER@$PROD_SERVER << 'EOF'
    cd /opt/myapp
    
    # Start new containers with updated image
    docker-compose -f docker-compose.prod.yml up -d --no-deps --scale web=2 web
    
    # Wait for new containers to be ready
    sleep 30
    
    # Health check new containers
    for i in {1..5}; do
        if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
            echo "✅ New containers are healthy"
            break
        fi
        if [ $i -eq 5 ]; then
            echo "❌ New containers failed health check"
            docker-compose -f docker-compose.prod.yml logs web
            exit 1
        fi
        sleep 10
    done
    
    # Scale down old containers
    docker-compose -f docker-compose.prod.yml up -d --no-deps --scale web=1 web
    
    # Clean up old containers and images
    docker system prune -f
EOF

# Post-deployment verification
echo "✅ Running post-deployment verification..."
sleep 10

# Verify deployment
if curl -f https://$PROD_SERVER/health/ > /dev/null 2>&1; then
    echo "🎉 Deployment successful!"
    
    # Send deployment notification
    curl -X POST $SLACK_WEBHOOK_URL \
        -H 'Content-type: application/json' \
        --data "{\"text\":\"✅ $APP_NAME deployed successfully to production\"}"
else
    echo "❌ Deployment verification failed!"
    
    # Rollback procedure
    echo "🔄 Initiating rollback..."
    ssh $DEPLOY_USER@$PROD_SERVER << 'EOF'
        cd /opt/myapp
        docker-compose -f docker-compose.prod.yml down
        docker-compose -f docker-compose.prod.yml up -d
EOF
    
    exit 1
fi

echo "🏁 Deployment process completed successfully!"
```

### 2. Infrastructure as Code

#### Terraform Configuration
```hcl
# main.tf - AWS Infrastructure
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.app_name}-vpc"
    Environment = var.environment
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.app_name}-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.app_name}-public-${count.index + 1}"
    Type = "public"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.app_name}-private-${count.index + 1}"
    Type = "private"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name        = "${var.app_name}-cluster"
    Environment = var.environment
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.app_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = false
  
  tags = {
    Name        = "${var.app_name}-alb"
    Environment = var.environment
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier     = "${var.app_name}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.app_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  tags = {
    Name        = "${var.app_name}-db"
    Environment = var.environment
  }
}

# ElastiCache for Redis
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.app_name}-cache-subnet"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.app_name}-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]
  
  tags = {
    Name        = "${var.app_name}-redis"
    Environment = var.environment
  }
}
```

### 3. Kubernetes Deployment

#### Kubernetes Manifests
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
  labels:
    app: django-app
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: django-app
  template:
    metadata:
      labels:
        app: django-app
        version: v1
    spec:
      containers:
      - name: django
        image: myapp/django:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: redis-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: secret-key
        
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 250m
            memory: 256Mi
        
        volumeMounts:
        - name: static-files
          mountPath: /app/staticfiles
        - name: media-files
          mountPath: /app/media
      
      volumes:
      - name: static-files
        persistentVolumeClaim:
          claimName: static-files-pvc
      - name: media-files
        persistentVolumeClaim:
          claimName: media-files-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: django-service
spec:
  selector:
    app: django-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: django-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - myapp.com
    secretName: django-tls
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: django-service
            port:
              number: 80
```

### 4. Monitoring y Observability en Production

#### Prometheus Metrics Integration
```python
# prometheus_metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from django.http import HttpResponse
import time

# Define metrics
REQUEST_COUNT = Counter(
    'django_requests_total',
    'Total Django requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'django_request_duration_seconds',
    'Django request duration',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'django_active_users',
    'Number of active users'
)

DATABASE_CONNECTIONS = Gauge(
    'django_database_connections',
    'Number of active database connections'
)

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.path
        ).observe(time.time() - start_time)
        
        return response

def metrics_view(request):
    """Prometheus metrics endpoint"""
    # Update gauge metrics
    ACTIVE_USERS.set(get_active_users_count())
    DATABASE_CONNECTIONS.set(len(connection.queries))
    
    return HttpResponse(generate_latest(), content_type='text/plain')

# Custom business metrics
POSTS_CREATED = Counter('posts_created_total', 'Total posts created')
USER_REGISTRATIONS = Counter('user_registrations_total', 'Total user registrations')
API_ERRORS = Counter('api_errors_total', 'Total API errors', ['error_type'])

# Usage in views
from .prometheus_metrics import POSTS_CREATED, API_ERRORS

class PostViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        POSTS_CREATED.inc()  # Track business metric
    
    def handle_exception(self, exc):
        API_ERRORS.labels(error_type=type(exc).__name__).inc()
        return super().handle_exception(exc)
```

### 5. Advanced Deployment Patterns

#### Blue-Green Deployment with Health Checks
```python
# deployment_manager.py
import requests
import time
import logging

class DeploymentManager:
    def __init__(self, app_name, environment):
        self.app_name = app_name
        self.environment = environment
        self.logger = logging.getLogger('deployment')
    
    def health_check(self, url, timeout=30, retries=5):
        """Perform health check with retries"""
        for attempt in range(retries):
            try:
                response = requests.get(f"{url}/health/", timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get('overall_status') == 'healthy':
                        return True
                
                self.logger.warning(f"Health check failed, attempt {attempt + 1}")
                time.sleep(timeout / retries)
                
            except requests.RequestException as e:
                self.logger.error(f"Health check error: {e}")
                time.sleep(timeout / retries)
        
        return False
    
    def blue_green_deploy(self, new_image_tag):
        """Execute blue-green deployment"""
        try:
            # Step 1: Deploy to green environment
            self.logger.info("Starting blue-green deployment")
            
            # Update green environment
            self.update_container_image('green', new_image_tag)
            
            # Step 2: Health check green environment
            if not self.health_check('https://green.myapp.com'):
                raise Exception("Green environment health check failed")
            
            # Step 3: Run database migrations on green
            self.run_migrations('green')
            
            # Step 4: Final health check
            if not self.health_check('https://green.myapp.com'):
                raise Exception("Post-migration health check failed")
            
            # Step 5: Switch traffic to green
            self.switch_traffic_to_green()
            
            # Step 6: Verify production traffic
            time.sleep(60)  # Wait for traffic to stabilize
            if not self.health_check('https://myapp.com'):
                # Rollback
                self.switch_traffic_to_blue()
                raise Exception("Production health check failed after traffic switch")
            
            # Step 7: Success - keep green as new blue
            self.logger.info("Blue-green deployment completed successfully")
            self.cleanup_old_environment('blue')
            
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            # Ensure we're on stable environment
            self.switch_traffic_to_blue()
            return False
    
    def canary_deploy(self, new_image_tag, canary_percentage=10):
        """Execute canary deployment"""
        try:
            # Deploy canary version
            self.deploy_canary(new_image_tag, canary_percentage)
            
            # Monitor canary metrics
            canary_healthy = self.monitor_canary_metrics(duration_minutes=15)
            
            if canary_healthy:
                # Gradually increase canary traffic
                for percentage in [25, 50, 75, 100]:
                    self.update_canary_traffic(percentage)
                    if not self.monitor_canary_metrics(duration_minutes=5):
                        self.rollback_canary()
                        return False
                
                # Full deployment successful
                self.promote_canary_to_production()
                return True
            else:
                self.rollback_canary()
                return False
                
        except Exception as e:
            self.logger.error(f"Canary deployment failed: {e}")
            self.rollback_canary()
            return False

# Environment-specific configurations
class EnvironmentConfig:
    def __init__(self, environment):
        self.environment = environment
        self.configs = {
            'development': {
                'DEBUG': True,
                'ALLOWED_HOSTS': ['localhost', '127.0.0.1'],
                'DATABASE_POOL_SIZE': 5,
                'CACHE_TIMEOUT': 300,
                'LOG_LEVEL': 'DEBUG',
            },
            'staging': {
                'DEBUG': False,
                'ALLOWED_HOSTS': ['staging.myapp.com'],
                'DATABASE_POOL_SIZE': 10,
                'CACHE_TIMEOUT': 600,
                'LOG_LEVEL': 'INFO',
            },
            'production': {
                'DEBUG': False,
                'ALLOWED_HOSTS': ['myapp.com', 'www.myapp.com'],
                'DATABASE_POOL_SIZE': 20,
                'CACHE_TIMEOUT': 3600,
                'LOG_LEVEL': 'WARNING',
            }
        }
    
    def get_config(self):
        return self.configs.get(self.environment, self.configs['development'])
```

### 6. Production Maintenance Scripts

#### Database Maintenance
```python
# maintenance.py
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.core.cache import cache
import logging

class DatabaseMaintenanceManager:
    def __init__(self):
        self.logger = logging.getLogger('maintenance')
    
    def analyze_slow_queries(self):
        """Analyze and report slow queries"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    rows
                FROM pg_stat_statements 
                WHERE mean_time > 1000  -- Queries slower than 1 second
                ORDER BY mean_time DESC 
                LIMIT 20
            """)
            
            slow_queries = cursor.fetchall()
            
            for query_data in slow_queries:
                self.logger.warning("Slow query detected", extra={
                    'query': query_data[0][:200],  # Truncate for logging
                    'calls': query_data[1],
                    'total_time_ms': query_data[2],
                    'mean_time_ms': query_data[3],
                })
            
            return slow_queries
    
    def vacuum_analyze_tables(self):
        """Perform VACUUM ANALYZE on all tables"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT schemaname, tablename 
                FROM pg_tables 
                WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
            """)
            
            tables = cursor.fetchall()
            
            for schema, table in tables:
                try:
                    cursor.execute(f'VACUUM ANALYZE "{schema}"."{table}"')
                    self.logger.info(f"VACUUM ANALYZE completed for {schema}.{table}")
                except Exception as e:
                    self.logger.error(f"VACUUM ANALYZE failed for {schema}.{table}: {e}")
    
    def cleanup_old_data(self):
        """Clean up old data to maintain performance"""
        # Clean old log entries
        old_logs = LogEntry.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=90)
        )
        deleted_count = old_logs.count()
        old_logs.delete()
        
        self.logger.info(f"Cleaned up {deleted_count} old log entries")
        
        # Clean expired sessions
        from django.contrib.sessions.models import Session
        Session.objects.filter(expire_date__lt=timezone.now()).delete()
        
        # Clean old cache entries
        cache.clear()
        
        return deleted_count

# Management command for maintenance
class Command(BaseCommand):
    help = 'Run database maintenance tasks'
    
    def add_arguments(self, parser):
        parser.add_argument('--vacuum', action='store_true', help='Run VACUUM ANALYZE')
        parser.add_argument('--analyze-queries', action='store_true', help='Analyze slow queries')
        parser.add_argument('--cleanup', action='store_true', help='Clean up old data')
        parser.add_argument('--all', action='store_true', help='Run all maintenance tasks')
    
    def handle(self, *args, **options):
        manager = DatabaseMaintenanceManager()
        
        if options['all'] or options['vacuum']:
            self.stdout.write("Running VACUUM ANALYZE...")
            manager.vacuum_analyze_tables()
        
        if options['all'] or options['analyze_queries']:
            self.stdout.write("Analyzing slow queries...")
            slow_queries = manager.analyze_slow_queries()
            self.stdout.write(f"Found {len(slow_queries)} slow queries")
        
        if options['all'] or options['cleanup']:
            self.stdout.write("Cleaning up old data...")
            deleted_count = manager.cleanup_old_data()
            self.stdout.write(f"Cleaned up {deleted_count} records")
        
        self.stdout.write(self.style.SUCCESS("Maintenance completed successfully"))
```

---

## 🧪 EJERCICIOS PRÁCTICOS

### Ejercicio 1: Zero-Downtime Deployment
```python
# Implement a complete zero-downtime deployment strategy
class ZeroDowntimeDeployer:
    def deploy_new_version(self, image_tag):
        """
        Your task: Implement zero-downtime deployment that:
        1. Starts new containers alongside old ones
        2. Runs health checks on new containers
        3. Gradually shifts traffic to new containers
        4. Rolls back if any issues are detected
        5. Cleans up old containers after success
        """
        pass
    
    def rollback_deployment(self, previous_tag):
        """
        Your task: Implement rollback mechanism that:
        1. Quickly switches traffic back to previous version
        2. Logs rollback reason and metrics
        3. Notifies team of rollback
        """
        pass
```

### Ejercicio 2: Auto-Scaling Implementation
```python
# Implement auto-scaling based on metrics
class AutoScaler:
    def __init__(self):
        self.target_cpu = 70  # Target CPU percentage
        self.target_memory = 80  # Target memory percentage
        self.min_replicas = 2
        self.max_replicas = 10
    
    def check_scaling_needed(self):
        """
        Your task: Implement logic to determine if scaling is needed
        Check: CPU usage, memory usage, response times, queue length
        Return: 'scale_up', 'scale_down', or 'no_change'
        """
        pass
    
    def scale_application(self, action):
        """
        Your task: Implement actual scaling
        - Update Kubernetes deployment replicas
        - Update load balancer configuration
        - Log scaling events
        """
        pass
```

### Ejercicio 3: Disaster Recovery
```python
# Implement disaster recovery procedures
class DisasterRecoveryManager:
    def backup_critical_data(self):
        """
        Your task: Implement comprehensive backup strategy
        1. Database backup with point-in-time recovery
        2. Static/media files backup
        3. Configuration backup
        4. Verify backup integrity
        """
        pass
    
    def restore_from_backup(self, backup_timestamp):
        """
        Your task: Implement restore procedure
        1. Stop application safely
        2. Restore database from backup
        3. Restore files from backup
        4. Restart application
        5. Verify restoration success
        """
        pass
```

---

## 📋 PRODUCTION DEPLOYMENT CHECKLIST

### Pre-Deployment:
- [ ] **Code Review**: All changes peer-reviewed
- [ ] **Tests Passing**: 100% test suite success
- [ ] **Security Scan**: No critical vulnerabilities
- [ ] **Performance Baseline**: Established benchmarks
- [ ] **Database Backup**: Recent backup verified
- [ ] **Rollback Plan**: Clear rollback procedure documented

### Deployment Process:
- [ ] **Health Check**: Current production healthy
- [ ] **Maintenance Window**: Scheduled if needed
- [ ] **Database Migrations**: Tested and ready
- [ ] **Static Files**: Collected and uploaded to CDN
- [ ] **Environment Variables**: All configs updated
- [ ] **Load Balancer**: Ready for traffic switching

### Post-Deployment:
- [ ] **Health Verification**: All services healthy
- [ ] **Performance Check**: Response times within SLA
- [ ] **Error Monitoring**: No increase in error rates
- [ ] **Business Metrics**: Core functionality working
- [ ] **User Verification**: Sample user journeys tested
- [ ] **Documentation**: Deployment notes updated

---

## 🎯 PREGUNTAS DE ENTREVISTA - DEPLOYMENT

### 1. Deployment Strategy
**P:** "¿Cómo realizarías un deployment sin downtime para una aplicación crítica?"

**R:** Multi-step approach:
1. **Blue-Green**: Mantener dos environments idénticos
2. **Health Checks**: Automated verification antes de traffic switch
3. **Database Migrations**: Backward-compatible migrations
4. **Load Balancer**: Gradual traffic shifting
5. **Monitoring**: Real-time metrics durante deployment
6. **Rollback Plan**: Immediate rollback si issues detectados

### 2. Container Orchestration
**P:** "¿Cuáles son las ventajas de usar Kubernetes vs Docker Compose?"

**R:** 
**Kubernetes:**
- Auto-scaling horizontal y vertical
- Service discovery y load balancing built-in
- Rolling updates y health checks
- Resource management avanzado
- Multi-node clusters

**Docker Compose:**
- Simplicity para single-node deployments
- Rapid development environment setup
- Less infrastructure overhead
- Easier debugging y troubleshooting

### 3. Database Migrations en Production
**P:** "¿Cómo manejarías una migration que podría tomar horas en una tabla con millones de registros?"

**R:** Strategy:
1. **Online Schema Change**: Tools como pt-online-schema-change
2. **Batched Operations**: Process en chunks pequeños
3. **Non-blocking**: Add columns nullable first, populate later
4. **Monitoring**: Track migration progress
5. **Rollback Plan**: Ability to revert changes safely
6. **Maintenance Window**: Schedule during low traffic

---

## 🏗️ INFRASTRUCTURE AS CODE

### Complete Infrastructure Setup
```python
# infrastructure/aws_setup.py
import boto3
import json

class AWSInfrastructureManager:
    def __init__(self, region='us-west-2'):
        self.region = region
        self.ecs_client = boto3.client('ecs', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.rds_client = boto3.client('rds', region_name=region)
    
    def create_ecs_service(self, cluster_name, service_name, task_definition):
        """Create ECS service with auto-scaling"""
        response = self.ecs_client.create_service(
            cluster=cluster_name,
            serviceName=service_name,
            taskDefinition=task_definition,
            desiredCount=2,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': self.get_private_subnets(),
                    'securityGroups': [self.get_app_security_group()],
                    'assignPublicIp': 'DISABLED'
                }
            },
            loadBalancers=[
                {
                    'targetGroupArn': self.get_target_group_arn(),
                    'containerName': 'django-app',
                    'containerPort': 8000
                }
            ],
            enableExecuteCommand=True,  # For debugging
        )
        
        # Setup auto-scaling
        self.setup_auto_scaling(cluster_name, service_name)
        
        return response
    
    def setup_auto_scaling(self, cluster_name, service_name):
        """Configure ECS auto-scaling"""
        autoscaling_client = boto3.client('application-autoscaling')
        
        # Register scalable target
        autoscaling_client.register_scalable_target(
            ServiceNamespace='ecs',
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            MinCapacity=2,
            MaxCapacity=10,
        )
        
        # CPU-based scaling policy
        autoscaling_client.put_scaling_policy(
            PolicyName=f'{service_name}-cpu-scaling',
            ServiceNamespace='ecs',
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
                },
                'ScaleOutCooldown': 300,
                'ScaleInCooldown': 300,
            }
        )
```

### Monitoring Stack Setup
```yaml
# monitoring/docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

---

## 🔥 PROYECTO FINAL: COMPLETE DEPLOYMENT PIPELINE

### Implementación Completa
```python
# deployment_pipeline.py
class ProductionDeploymentPipeline:
    def __init__(self, app_name, environment_config):
        self.app_name = app_name
        self.config = environment_config
        self.logger = logging.getLogger('deployment')
    
    def execute_full_pipeline(self, git_commit_sha):
        """Execute complete deployment pipeline"""
        pipeline_steps = [
            ('Pre-deployment Checks', self.pre_deployment_checks),
            ('Build Docker Image', lambda: self.build_image(git_commit_sha)),
            ('Security Scan', self.security_scan_image),
            ('Database Backup', self.backup_database),
            ('Run Migrations', self.run_migrations),
            ('Deploy Application', lambda: self.deploy_application(git_commit_sha)),
            ('Health Verification', self.verify_deployment_health),
            ('Performance Check', self.verify_performance),
            ('Smoke Tests', self.run_smoke_tests),
            ('Update Monitoring', self.update_monitoring_config),
            ('Cleanup', self.cleanup_old_resources),
        ]
        
        for step_name, step_func in pipeline_steps:
            try:
                self.logger.info(f"🔄 Executing: {step_name}")
                step_func()
                self.logger.info(f"✅ Completed: {step_name}")
            except Exception as e:
                self.logger.error(f"❌ Failed: {step_name} - {e}")
                self.rollback_deployment()
                raise
        
        self.logger.info("🎉 Deployment pipeline completed successfully!")
        self.send_deployment_notification(success=True, commit_sha=git_commit_sha)
    
    def pre_deployment_checks(self):
        """Comprehensive pre-deployment validation"""
        checks = [
            self.check_database_health,
            self.check_cache_health,
            self.check_external_services,
            self.verify_environment_config,
            self.check_disk_space,
            self.verify_ssl_certificates,
        ]
        
        for check in checks:
            if not check():
                raise Exception(f"Pre-deployment check failed: {check.__name__}")
    
    def build_image(self, commit_sha):
        """Build and tag Docker image"""
        build_args = {
            'GIT_COMMIT': commit_sha,
            'BUILD_DATE': timezone.now().isoformat(),
            'VERSION': self.config.get('version', '1.0.0'),
        }
        
        # Build image with multiple tags
        tags = [
            f"{self.app_name}:latest",
            f"{self.app_name}:{commit_sha}",
            f"{self.app_name}:v{self.config.get('version', '1.0.0')}",
        ]
        
        # Docker build command would go here
        self.logger.info(f"Building image with tags: {tags}")
    
    def security_scan_image(self):
        """Scan Docker image for vulnerabilities"""
        # Integration with security scanning tools
        scan_results = {
            'critical': 0,
            'high': 0,
            'medium': 2,
            'low': 5,
        }
        
        if scan_results['critical'] > 0 or scan_results['high'] > 0:
            raise Exception("Security vulnerabilities found in image")
    
    def verify_deployment_health(self):
        """Comprehensive deployment health verification"""
        health_checks = [
            ('Application Health', 'https://myapp.com/health/'),
            ('API Health', 'https://myapp.com/api/v1/health/'),
            ('Database Health', self.check_database_connections),
            ('Cache Health', self.check_cache_performance),
        ]
        
        for check_name, check_target in health_checks:
            if isinstance(check_target, str):
                # URL health check
                if not self.url_health_check(check_target):
                    raise Exception(f"{check_name} failed")
            else:
                # Function health check
                if not check_target():
                    raise Exception(f"{check_name} failed")
    
    def run_smoke_tests(self):
        """Critical user journey testing"""
        smoke_tests = [
            self.test_user_registration,
            self.test_user_login,
            self.test_post_creation,
            self.test_api_endpoints,
        ]
        
        for test in smoke_tests:
            if not test():
                raise Exception(f"Smoke test failed: {test.__name__}")
    
    def send_deployment_notification(self, success, commit_sha):
        """Send deployment notification to team"""
        status_emoji = "🎉" if success else "❌"
        message = f"{status_emoji} Deployment {'successful' if success else 'failed'}"
        
        notification_data = {
            'text': message,
            'attachments': [
                {
                    'color': 'good' if success else 'danger',
                    'fields': [
                        {'title': 'Application', 'value': self.app_name, 'short': True},
                        {'title': 'Environment', 'value': self.config['environment'], 'short': True},
                        {'title': 'Commit', 'value': commit_sha[:8], 'short': True},
                        {'title': 'Timestamp', 'value': timezone.now().isoformat(), 'short': True},
                    ]
                }
            ]
        }
        
        # Send to Slack/Teams/Discord
        self.send_webhook_notification(notification_data)
```

---

## 🛡️ PRODUCTION SECURITY CONFIGURATION

### Nginx Security Configuration
```nginx
# nginx/nginx.conf - Production security
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Security headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    
    # Hide nginx version
    server_tokens off;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    upstream django {
        server web:8000;
        keepalive 32;
    }
    
    server {
        listen 80;
        server_name myapp.com www.myapp.com;
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name myapp.com www.myapp.com;
        
        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_stapling on;
        ssl_stapling_verify on;
        
        # SSL Security
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Login rate limiting
        location /auth/login/ {
            limit_req zone=login burst=3 nodelay;
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Media files
        location /media/ {
            alias /app/media/;
            expires 1M;
            add_header Cache-Control "public";
        }
        
        # Application
        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

---

## 📊 MONITORING EN PRODUCTION

### CloudWatch Custom Metrics
```python
# cloudwatch_metrics.py
import boto3
from datetime import datetime

class CloudWatchMetrics:
    def __init__(self, namespace='MyApp/Production'):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = namespace
    
    def put_custom_metric(self, metric_name, value, unit='Count', dimensions=None):
        """Send custom metric to CloudWatch"""
        metric_data = {
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Timestamp': datetime.utcnow(),
        }
        
        if dimensions:
            metric_data['Dimensions'] = [
                {'Name': k, 'Value': v} for k, v in dimensions.items()
            ]
        
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=[metric_data]
        )
    
    def put_business_metrics(self):
        """Send business metrics to CloudWatch"""
        metrics = {
            'ActiveUsers': User.objects.filter(
                last_login__gte=timezone.now() - timedelta(hours=24)
            ).count(),
            'PostsCreatedToday': Post.objects.filter(
                created_at__date=timezone.now().date()
            ).count(),
            'APIRequestsPerHour': self.get_api_requests_last_hour(),
            'ErrorRate': self.calculate_error_rate(),
        }
        
        for metric_name, value in metrics.items():
            self.put_custom_metric(metric_name, value)

# Management command for metrics
class Command(BaseCommand):
    help = 'Send custom metrics to CloudWatch'
    
    def handle(self, *args, **options):
        metrics = CloudWatchMetrics()
        metrics.put_business_metrics()
        self.stdout.write(self.style.SUCCESS('Metrics sent to CloudWatch'))
```

---

## 🎯 ENTREGA FINAL DEL DÍA

### Production-Ready Application Stack
Debes haber implementado:

1. **Complete Containerization**:
   - Multi-stage Dockerfile optimizado
   - Docker Compose para dev y production
   - Security best practices en containers

2. **CI/CD Pipeline**:
   - Automated testing y quality gates
   - Security scanning integration
   - Blue-green o canary deployment

3. **Infrastructure as Code**:
   - Terraform o CloudFormation templates
   - Auto-scaling configuration
   - Load balancer setup

4. **Monitoring Stack**:
   - Prometheus + Grafana dashboards
   - Custom business metrics
   - Alerting rules configuration

5. **Security Hardening**:
   - Nginx security configuration
   - SSL/TLS setup
   - Rate limiting y DDoS protection

---

## 🏆 ACHIEVEMENT UNLOCKED: PRODUCTION DEPLOYMENT MASTER

### Skills Mastered:
- ✅ **Container Orchestration**: Docker + Kubernetes/ECS
- ✅ **CI/CD Automation**: Complete pipeline automation
- ✅ **Infrastructure Management**: IaC + cloud services
- ✅ **Security Hardening**: Production-grade security
- ✅ **Monitoring & Observability**: Complete monitoring stack
- ✅ **Disaster Recovery**: Backup y rollback strategies

### Interview Readiness:
- ✅ **DevOps Knowledge**: End-to-end deployment understanding
- ✅ **Cloud Platforms**: AWS/GCP/Azure deployment patterns
- ✅ **Scalability**: Auto-scaling y load management
- ✅ **Reliability Engineering**: High availability systems
- ✅ **Security Mindset**: Production security practices

---

## 🚀 PREPARACIÓN SEMANA 8: FLASK + FASTAPI

Mañana empezamos la **Semana 8** con frameworks alternativos:

**Día 48-49: Flask Fundamentals**
- Application factory pattern
- Blueprints y modular architecture
- Flask extensions ecosystem
- SQLAlchemy integration

**Pre-study para mañana:**
- Revisa Flask documentation básica
- Compara Flask vs Django philosophy
- Estudia Flask application patterns

### Portfolio Impact:
Con el día 47 completado, tu portfolio demuestra:
- **Full-Stack DevOps**: From code to production
- **Enterprise Readiness**: Production-grade deployment skills
- **Cloud Native**: Modern containerized applications
- **Reliability