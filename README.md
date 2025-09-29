# Smart Condominium Backend

🏢 **Sistema de gestión integral para condominios desarrollado con Django REST Framework**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15.1-orange.svg)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://postgresql.org)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Storage-blue.svg)](https://cloudinary.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange.svg)](https://scikit-learn.org)

## 📋 Descripción

Smart Condominium Backend es una API REST robusta diseñada para la gestión completa de condominios. El sistema permite administrar residentes, unidades, comunicados, finanzas, vehículos, mascotas, reservas y más, de manera eficiente y segura. Incluye funcionalidades avanzadas como IA para predicción de riesgos de morosidad y almacenamiento en la nube para imágenes.

### 🚀 Fases Implementadas

- **✅ Fase 1:** Gestión de Usuarios, Roles y Unidades Residenciales
- **✅ Fase 2:** Sistema de Comunicación y Gestión Financiera
- **✅ Fase 3:** Gestión de Espacios Comunes y Reservas
- **✅ Fase 4:** Gestión de Vehículos y Mascotas
- **✅ Fase 5:** Registro de Visitantes con Fotos (Cloudinary) + IA para Predicción de Riesgos

## ✨ Características Principales

- **🔐 Autenticación JWT**: Sistema de autenticación basado en JSON Web Tokens
- **🏠 API RESTful Completa**: Gestión integral de condominios
- **💬 Sistema de Comunicación**: Anuncios, feedback y comunicados
- **💰 Gestión Financiera Avanzada**: Cuotas, pagos, estados financieros
- **🚗 Gestión de Vehículos y Mascotas**: Control de acceso y registro
- **📅 Sistema de Reservas**: Espacios comunes y eventos
- **📸 Almacenamiento en Nube**: Cloudinary para fotos de visitantes
- **🤖 Inteligencia Artificial**: Predicción de riesgos de morosidad con ML
- **👨‍💼 Admin Interface**: Interface administrativa personalizada
- **🔍 Endpoint /me/**: Datos del usuario autenticado
- **📊 Modelos Personalizados**: Usuario con roles y unidades residenciales

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.0.6 + Django REST Framework 3.15.1
- **Autenticación**: djangorestframework-simplejwt 5.3.0
- **Base de Datos**: PostgreSQL (prod) / SQLite (dev)
- **Almacenamiento**: Cloudinary (imágenes)
- **Machine Learning**: Scikit-learn 1.7.2 + Joblib 1.3.2 + Pandas 2.3.2
- **Configuración**: python-decouple 3.8
- **Pagos**: Stripe API
- **Despliegue**: Render / Docker

## 📁 Estructura del Proyecto

```
smartcondo_backend/
├── 📂 Documentación/          # Docs, README, guías
├── 📂 Tests/                  # Scripts de testing, Postman
├── 📂 Otros/                  # Scripts misceláneos, configs
├── 📂 Machine Learning/       # Modelos entrenados (.joblib)
├── manage.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── smartcondo_backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── administration/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── management/commands/
        └── train_risk_model.py
```

## ✨ Características Principales

- **🔐 Autenticación JWT**: Sistema de autenticación basado en JSON Web Tokens
- **🏠 API RESTful Completa**: Gestión integral de condominios
- **💬 Sistema de Comunicación**: Anuncios, feedback y comunicados
- **💰 Gestión Financiera Avanzada**: Cuotas, pagos, estados financieros
- **🚗 Gestión de Vehículos y Mascotas**: Control de acceso y registro
- **📅 Sistema de Reservas**: Espacios comunes y eventos
- **📸 Almacenamiento en Nube**: Cloudinary para fotos de visitantes
- **🤖 Inteligencia Artificial**: Predicción de riesgos de morosidad con ML
- **👨‍💼 Admin Interface**: Interface administrativa personalizada
- **🔍 Endpoint /me/**: Datos del usuario autenticado
- **📊 Modelos Personalizados**: Usuario con roles y unidades residenciales

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.0.6 + Django REST Framework 3.15.1
- **Autenticación**: djangorestframework-simplejwt 5.3.0
- **Base de Datos**: PostgreSQL (prod) / SQLite (dev)
- **Almacenamiento**: Cloudinary (imágenes)
- **Machine Learning**: Scikit-learn 1.7.2 + Joblib 1.3.2 + Pandas 2.3.2
- **Configuración**: python-decouple 3.8
- **Pagos**: Stripe API
- **Despliegue**: Render / Docker

## 🚀 Instalación y Configuración

### 1. Clona el repositorio
```bash
git clone https://github.com/DiegoxdGarcia2/smart-condominium-backend.git
cd smart-condominium-backend
```

### 2. Crea un entorno virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno
```bash
cp Otros/.env.example .env
```
Edita `.env` con tus configuraciones. Para Cloudinary, agrega:
```
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

### 5. Ejecuta las migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crea un superusuario
```bash
python manage.py createsuperuser
```

### 7. Entrena el modelo de IA (opcional)
```bash
python manage.py train_risk_model
```

### 8. Ejecuta el servidor
```bash
python manage.py runserver
```

## 🤖 Funcionalidades de IA

### Predicción de Riesgos de Morosidad
- **Comando**: `python manage.py train_risk_model`
- **Endpoint**: `POST /api/administration/ai/predict_payment_risk/`
- **Modelo**: Random Forest con Scikit-learn
- **Características**: Monto, tasa histórica de morosidad, pagos atrasados, días vencidos

### Almacenamiento de Imágenes
- **Servicio**: Cloudinary
- **Campo**: `visitor_photo` en `VisitorLog`
- **URL completa**: Devuelta en `visitor_photo_url`

## 📡 Endpoints Principales

### Autenticación
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token

### Administración
- `GET/POST /api/administration/users/` - Usuarios
- `GET/POST /api/administration/residential-units/` - Unidades
- `GET/POST /api/administration/financial-fees/` - Cuotas
- `GET/POST /api/administration/visitor-logs/` - Visitantes
- `POST /api/administration/ai/predict_payment_risk/` - IA Riesgos

### Pagos
- `POST /api/administration/initiate-payment/` - Iniciar pago
- `POST /api/administration/payment-webhook/` - Webhook Stripe

## 📁 Estructura del Proyecto

```
smartcondo_backend/
├── 📂 Documentación/          # Docs, README, guías
├── 📂 Tests/                  # Scripts de testing, Postman
├── 📂 Otros/                  # Scripts misceláneos, configs
├── 📂 Machine Learning/       # Modelos entrenados (.joblib)
├── manage.py
├── requirements.txt
├── Dockerfile
├── smartcondo_backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── administration/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── management/commands/
        └── train_risk_model.py
```
