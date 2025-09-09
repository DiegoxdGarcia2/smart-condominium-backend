# Guía de Despliegue - Smart Condominium Backend

## Preparación para Producción

### 1. Variables de Entorno
Crea un archivo `.env` basado en `.env.example`:

```env
# Configuración de Django
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Configuración de PostgreSQL
DB_NAME=smartcondo_prod
DB_USER=smartcondo_user
DB_PASSWORD=password-super-seguro
DB_HOST=localhost
DB_PORT=5432
```

### 2. Configuración de Base de Datos PostgreSQL

```sql
-- Crear la base de datos y usuario
CREATE DATABASE smartcondo_prod;
CREATE USER smartcondo_user WITH PASSWORD 'password-super-seguro';
GRANT ALL PRIVILEGES ON DATABASE smartcondo_prod TO smartcondo_user;
ALTER USER smartcondo_user CREATEDB;
```

### 3. Modificar settings.py para Producción

Descomenta la configuración de PostgreSQL en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='smartcondo_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 4. Instalar Dependencias para Producción

```bash
pip install psycopg2-binary gunicorn
```

### 5. Ejecutar Migraciones en Producción

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### 6. Configuración de Gunicorn

Crea `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### 7. Ejecutar con Gunicorn

```bash
gunicorn smartcondo_backend.wsgi:application -c gunicorn.conf.py
```

### 8. Configuración de Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

### 9. Configuración con Docker (Opcional)

Crea `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "smartcondo_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Crea `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: smartcondo_prod
      POSTGRES_USER: smartcondo_user
      POSTGRES_PASSWORD: password-super-seguro
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 10. Configuraciones de Seguridad Adicionales

En `settings.py` para producción:

```python
# Seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Si usas HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 11. Monitoreo y Logs

Configura logging en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/smartcondo.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### 12. Backup de Base de Datos

```bash
# Crear backup
pg_dump -U smartcondo_user -h localhost smartcondo_prod > backup.sql

# Restaurar backup
psql -U smartcondo_user -h localhost smartcondo_prod < backup.sql
```

## Comandos Útiles para Producción

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Cargar datos iniciales
python manage.py load_initial_data

# Verificar configuración
python manage.py check --deploy

# Crear cache tables (si usas cache de DB)
python manage.py createcachetable
```
