# Smart Condominium Backend

🏢 **Sistema de gestión integral para condominios desarrollado con Django REST Framework**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15.1-orange.svg)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://postgresql.org)

## 📋 Descripción

Smart Condominium Backend es una API REST robusta diseñada para la gestión completa de condominios. El sistema permite administrar residentes, unidades, comunicados y finanzas de manera eficiente y segura.


## Características

- **✅ Autenticación JWT**: Sistema de autenticación basado en JSON Web Tokens
- **✅ API RESTful**: API completa para gestión de usuarios, roles y unidades residenciales  
- **✅ Sistema de Comunicados**: Gestión de anuncios y comunicados
- **✅ Gestión Financiera**: Cuotas, pagos y estados financieros
- **✅ Admin Interface**: Interface administrativa de Django personalizada
- **✅ Endpoint /me/**: Obtener datos del usuario autenticado
- **✅ Modelos Personalizados**: Usuario personalizado con roles y unidades residenciales

## Tecnologías Utilizadas

- Django 5.0.6
- Django REST Framework 3.15.1
- djangorestframework-simplejwt 5.3.0
- python-decouple 3.8
- psycopg2-binary 2.9.10
- PostgreSQL (recomendado) / SQLite (desarrollo)

## Instalación y Configuración

### 1. Clona el repositorio o usa el código fuente

### 2. Crea un entorno virtual
```bash
python -m venv .venv
```

### 3. Activa el entorno virtual
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 5. Configura las variables de entorno
```bash
cp .env.example .env
```
Edita el archivo `.env` con tus configuraciones.

### 6. Ejecuta las migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crea un superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecuta el servidor de desarrollo
```bash
python manage.py runserver
```

## Endpoints de la API

### Autenticación
- `POST /api/token/` - Obtener token de acceso
- `POST /api/token/refresh/` - Refrescar token

### Administración
- `GET/POST /api/administration/roles/` - Listar/Crear roles
- `GET/PUT/PATCH/DELETE /api/administration/roles/{id}/` - Operaciones sobre rol específico
- `GET/POST /api/administration/users/` - Listar/Crear usuarios
- `GET/PUT/PATCH/DELETE /api/administration/users/{id}/` - Operaciones sobre usuario específico
- `GET/POST /api/administration/residential-units/` - Listar/Crear unidades residenciales
- `GET/PUT/PATCH/DELETE /api/administration/residential-units/{id}/` - Operaciones sobre unidad específica

## Modelos

### Role
- `name`: Nombre del rol (único)

### User (Personalizado)
- `email`: Email (usado como username)
- `phone_number`: Número de teléfono
- `role`: Relación con Role
- Hereda de AbstractUser de Django

### ResidentialUnit
- `unit_number`: Número de unidad (único)
- `type`: Tipo ('Departamento' o 'Casa')
- `floor`: Piso (opcional)
- `owner`: Relación con User (opcional)

## Configuración de Base de Datos

### Para Desarrollo (SQLite - por defecto)
No requiere configuración adicional, utiliza SQLite automáticamente.

### Para Producción (PostgreSQL)
1. Instala psycopg2-binary:
```bash
pip install psycopg2-binary
```

2. Descomenta la configuración de PostgreSQL en `settings.py`

3. Configura las variables de entorno en `.env`:
```
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

## Admin de Django

Accede al admin en `http://127.0.0.1:8000/admin/` con las credenciales del superusuario creado.

## Estructura del Proyecto

```
smartcondo_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── smartcondo_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── administration/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── migrations/
```

