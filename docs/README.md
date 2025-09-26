# 📖 Documentación del Backend - Smart Condominium

*Documentación completa y actualizada del backend para desarrollo móvil y frontend*

---

## 📋 Índice de Documentación

### 🚀 Documentación Principal
- **[📱 API Documentation Completa](COMPLETE_BACKEND_API_DOCUMENTATION.md)** - Documentación completa de todos los endpoints con ejemplos
- **[🔧 Ejemplos de Integración Móvil](MOBILE_INTEGRATION_EXAMPLES.md)** - Ejemplos específicos para React Native, Flutter, iOS y Android
- **[🛠️ Casos de Uso y Troubleshooting](USE_CASES_TROUBLESHOOTING.md)** - Casos de uso comunes y solución de problemas

### 📚 Documentación de Funcionalidades Específicas
- **[💳 Copilot Prompt para PaymentTab](COPILOT_PROMPT_FOR_PAYMENTTAB.txt)** - Guía para implementar la funcionalidad de pagos en frontend

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico
- **Backend**: Django 5.0.6 + Django REST Framework
- **Base de Datos**: PostgreSQL (Render managed)
- **Autenticación**: JWT con django-rest-framework-simplejwt
- **Pagos**: Stripe Checkout + Webhooks
- **Deployment**: Render.com
- **Storage**: Archivos estáticos en Render

### Estructura del Proyecto
```
smart-condominium-backend/
├── smartcondo_backend/          # Configuración principal del proyecto
│   ├── settings.py             # Configuraciones
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                # WSGI para producción
├── administration/              # App principal
│   ├── models.py              # Modelos de datos
│   ├── serializers.py         # Serializers para API
│   ├── views.py               # ViewSets y lógica de negocio
│   ├── urls.py                # URLs de la app
│   └── migrations/            # Migraciones de BD
├── docs/                       # Documentación completa
└── requirements.txt           # Dependencias Python
```

---

## 🔗 URLs del Sistema

### Producción
- **API Base**: `https://smart-condominium-backend.onrender.com`
- **Admin Panel**: `https://smart-condominium-backend.onrender.com/admin/`

### Endpoints Principales
- **Autenticación**: `/api/token/` y `/api/token/refresh/`
- **API Core**: `/api/administration/`
- **Webhook Stripe**: `/api/administration/payment-webhook/`

---

## 🔐 Autenticación

El sistema utiliza **JWT (JSON Web Tokens)** para autenticación:

```http
POST /api/token/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "password123"
}
```

**Respuesta:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Uso en requests:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📱 Endpoints Disponibles

### Core del Sistema
| Endpoint | Descripción | Métodos |
|----------|-------------|---------|
| `/api/administration/users/` | Gestión de usuarios | GET, POST, PUT, PATCH, DELETE |
| `/api/administration/users/me/` | Perfil del usuario actual | GET |
| `/api/administration/roles/` | Roles del sistema | GET, POST, PUT, DELETE |
| `/api/administration/residential-units/` | Unidades residenciales | GET, POST, PUT, DELETE |

### Comunicación y Finanzas
| Endpoint | Descripción | Métodos |
|----------|-------------|---------|
| `/api/administration/announcements/` | Comunicados | GET, POST, PUT, DELETE |
| `/api/administration/financial-fees/` | Cuotas financieras | GET, POST, PUT, DELETE |
| `/api/administration/payments/` | Transacciones de pago | GET, POST |
| `/api/administration/payments/initiate_payment/` | Iniciar pago Stripe | POST |
| `/api/administration/payments/my_payments/` | Mis pagos | GET |

### Reservas y Áreas Comunes
| Endpoint | Descripción | Métodos |
|----------|-------------|---------|
| `/api/administration/common-areas/` | Áreas comunes | GET, POST, PUT, DELETE |
| `/api/administration/reservations/` | Reservas | GET, POST, PUT, DELETE |

### Gestión de Residentes
| Endpoint | Descripción | Métodos |
|----------|-------------|---------|
| `/api/administration/vehicles/` | Vehículos | GET, POST, PUT, DELETE |
| `/api/administration/pets/` | Mascotas | GET, POST, PUT, DELETE |
| `/api/administration/visitor-logs/` | Registro de visitantes | GET, POST |
| `/api/administration/visitor-logs/{id}/register_exit/` | Registrar salida | POST |

### Sistema de Gestión
| Endpoint | Descripción | Métodos |
|----------|-------------|---------|
| `/api/administration/tasks/` | Tareas de mantenimiento | GET, POST, PUT, DELETE |
| `/api/administration/tasks/my_tasks/` | Mis tareas asignadas | GET |
| `/api/administration/feedback/` | Sistema de feedback | GET, POST, PUT, DELETE |
| `/api/administration/feedback/my_feedback/` | Mi feedback | GET |

---

## 🎯 Quick Start para Desarrolladores

### 1. Configuración Básica
```javascript
// React Native / JavaScript
const API_BASE_URL = 'https://smart-condominium-backend.onrender.com';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para JWT
apiClient.interceptors.request.use((config) => {
    const token = getStoredToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
```

### 2. Login Básico
```javascript
async function login(email, password) {
    const response = await fetch(`${API_BASE_URL}/api/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    return data;
}
```

### 3. Obtener Datos del Usuario
```javascript
async function getProfile() {
    const response = await apiClient.get('/api/administration/users/me/');
    return response.data;
}
```

---

## 🧪 Datos de Prueba

### Usuario de Prueba
```
Email: admin@smartcondo.com
Password: admin123
```

### Endpoints de Testing
- **Status**: `GET /` - Estado general de la API
- **Health**: `GET /api/` - Health check

---

## 📋 Modelos Principales

### User (Usuario)
- `id`, `email`, `first_name`, `last_name`, `phone_number`, `role`, `is_active`, `date_joined`

### ResidentialUnit (Unidad Residencial)  
- `id`, `unit_number`, `type`, `floor`, `owner`

### FinancialFee (Cuota Financiera)
- `id`, `unit`, `description`, `amount`, `due_date`, `status`, `created_at`

### PaymentTransaction (Transacción de Pago)
- `id`, `financial_fee`, `resident`, `transaction_id`, `amount`, `status`, `gateway_response`, `created_at`, `processed_at`

### Reservation (Reserva)
- `id`, `common_area`, `resident`, `start_time`, `end_time`, `status`, `total_paid`, `created_at`

### Vehicle (Vehículo)
- `id`, `owner`, `license_plate`, `brand`, `model`, `color`, `is_active`, `created_at`

### VisitorLog (Registro de Visitante)
- `id`, `visitor_name`, `visitor_id`, `unit_visited`, `purpose`, `entry_time`, `exit_time`, `status`

---

## 🛡️ Seguridad

### Autenticación y Autorización
- **JWT Tokens** con expiración automática
- **Refresh tokens** para renovación segura
- **Permisos por rol** (Admin, Residente, Personal)
- **Validación de datos** en todos los endpoints

### Stripe Integration
- **Webhook signatures** verificadas con `STRIPE_WEBHOOK_SECRET`
- **Payment URLs** generadas por Stripe (no construcción manual)
- **Metadata** segura para asociar pagos con usuarios

### Best Practices
- **HTTPS** obligatorio en producción
- **CORS** configurado apropiadamente
- **Rate limiting** implementado
- **Validación de entrada** exhaustiva

---

## 🔧 Configuración de Desarrollo

### Variables de Entorno Requeridas
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=http://localhost:3000
```

### Instalación Local
```bash
# Clonar repositorio
git clone https://github.com/DiegoxdGarcia2/smart-condominium-backend.git

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

## 📞 Soporte y Contacto

### Issues y Bugs
- **GitHub Issues**: [Reportar problemas](https://github.com/DiegoxdGarcia2/smart-condominium-backend/issues)
- **Documentación**: Referirse a los archivos en `/docs/`

### Desarrollo
- **Branch principal**: `master`
- **Deploy automático**: Conectado a Render.com
- **Logs**: Disponibles en Render Dashboard

---

## 📝 Changelog

### v1.0.0 (Septiembre 2025)
- ✅ Sistema completo de autenticación JWT
- ✅ CRUD completo para todos los módulos
- ✅ Integración con Stripe Checkout
- ✅ Sistema de webhooks para pagos
- ✅ API RESTful completa
- ✅ Documentación exhaustiva para desarrollo móvil
- ✅ Deploy en producción (Render.com)

---

*Smart Condominium Backend - Desarrollado con ❤️ para la gestión moderna de condominios*
*Última actualización: 24 de Septiembre de 2025*