# 🏢 Smart Condominium Backend - API Documentation Completa
*Documentación completa para desarrollo móvil y frontend*

---

## 🚀 Información General

**Base URL:** `https://smart-condominium-backend.onrender.com`
**Framework:** Django REST Framework
**Autenticación:** JWT (JSON Web Tokens)
**Formato de respuesta:** JSON

---

## 🔐 Autenticación

### 1. Obtener Token de Acceso
```http
POST /api/token/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "password123"
}
```

**Respuesta Exitosa (200):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Refrescar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Usar Token en Requests
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | CREATED | Recurso creado exitosamente |
| 400 | BAD REQUEST | Error en los datos enviados |
| 401 | UNAUTHORIZED | Token JWT inválido o ausente |
| 403 | FORBIDDEN | Sin permisos para la operación |
| 404 | NOT FOUND | Recurso no encontrado |
| 405 | METHOD NOT ALLOWED | Método HTTP no permitido |
| 500 | INTERNAL SERVER ERROR | Error interno del servidor |

---

# 📱 API ENDPOINTS COMPLETOS

## 1. 👥 USUARIOS

### Base URL: `/api/administration/users/`

#### Listar Usuarios
```http
GET /api/administration/users/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@smartcondo.com",
        "first_name": "Admin",
        "last_name": "User",
        "phone_number": "+52-555-0123",
        "role": 1,
        "role_name": "Administrador",
        "is_active": true,
        "date_joined": "2025-09-07T01:00:00Z"
    }
]
```

#### Obtener Usuario Específico
```http
GET /api/administration/users/{id}/
Authorization: Bearer {token}
```

#### Crear Usuario
```http
POST /api/administration/users/
Authorization: Bearer {token}
Content-Type: application/json

{
    "email": "nuevo@usuario.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone_number": "+52-555-1234",
    "role": 2
}
```

#### Actualizar Usuario (PUT)
```http
PUT /api/administration/users/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "email": "usuario@actualizado.com",
    "first_name": "Juan Carlos",
    "last_name": "Pérez García",
    "phone_number": "+52-555-5678",
    "role": 2,
    "is_active": true
}
```

#### Actualización Parcial (PATCH)
```http
PATCH /api/administration/users/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "phone_number": "+52-555-9999"
}
```

#### Eliminar Usuario
```http
DELETE /api/administration/users/{id}/
Authorization: Bearer {token}
```

#### Mi Perfil
```http
GET /api/administration/users/me/
Authorization: Bearer {token}
```

---

## 2. 🏠 UNIDADES RESIDENCIALES

### Base URL: `/api/administration/residential-units/`

#### Listar Unidades
```http
GET /api/administration/residential-units/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "unit_number": "101",
        "type": "Departamento",
        "floor": 1,
        "owner": 2,
        "owner_name": "Juan Pérez",
        "owner_email": "juan@ejemplo.com"
    }
]
```

#### Crear Unidad
```http
POST /api/administration/residential-units/
Authorization: Bearer {token}
Content-Type: application/json

{
    "unit_number": "202",
    "type": "Departamento",
    "floor": 2,
    "owner": 3
}
```

#### Actualizar Unidad (PUT)
```http
PUT /api/administration/residential-units/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "unit_number": "202A",
    "type": "Casa",
    "floor": 2,
    "owner": 3
}
```

---

## 3. 📢 COMUNICADOS

### Base URL: `/api/administration/announcements/`

#### Listar Comunicados
```http
GET /api/administration/announcements/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "title": "Mantenimiento del Elevador",
        "content": "Se realizará mantenimiento preventivo...",
        "author": 1,
        "author_name": "Admin User",
        "created_at": "2025-09-24T10:00:00Z",
        "updated_at": "2025-09-24T10:00:00Z"
    }
]
```

#### Crear Comunicado
```http
POST /api/administration/announcements/
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Nuevo Reglamento",
    "content": "Por la presente se comunica que..."
}
```
*Nota: El autor se asigna automáticamente al usuario autenticado*

#### Actualizar Comunicado (PUT)
```http
PUT /api/administration/announcements/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Nuevo Reglamento - Actualizado",
    "content": "Contenido actualizado del comunicado..."
}
```

---

## 4. 💰 CUOTAS FINANCIERAS

### Base URL: `/api/administration/financial-fees/`

#### Listar Cuotas
```http
GET /api/administration/financial-fees/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "unit": 1,
        "unit_number": "101",
        "unit_owner_name": "Juan Pérez",
        "description": "Cuota mensual Septiembre 2025",
        "amount": "250.00",
        "due_date": "2025-09-30",
        "status": "Pendiente",
        "created_at": "2025-09-01T08:00:00Z"
    }
]
```

#### Crear Cuota
```http
POST /api/administration/financial-fees/
Authorization: Bearer {token}
Content-Type: application/json

{
    "unit": 1,
    "description": "Cuota mensual Octubre 2025",
    "amount": "250.00",
    "due_date": "2025-10-31",
    "status": "Pendiente"
}
```

#### Actualizar Cuota (PUT)
```http
PUT /api/administration/financial-fees/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "unit": 1,
    "description": "Cuota mensual Octubre 2025 - Actualizada",
    "amount": "275.00",
    "due_date": "2025-10-31",
    "status": "Pendiente"
}
```

---

## 5. 🏊 ÁREAS COMUNES

### Base URL: `/api/administration/common-areas/`

#### Listar Áreas Comunes
```http
GET /api/administration/common-areas/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "name": "Piscina",
        "description": "Piscina principal del condominio",
        "capacity": 20,
        "hourly_rate": "15.00",
        "is_available": true
    }
]
```

#### Crear Área Común
```http
POST /api/administration/common-areas/
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Salón de Eventos",
    "description": "Salón para eventos familiares",
    "capacity": 50,
    "hourly_rate": "25.00",
    "is_available": true
}
```

---

## 6. 📅 RESERVAS

### Base URL: `/api/administration/reservations/`

#### Listar Reservas
```http
GET /api/administration/reservations/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "common_area": 1,
        "common_area_name": "Piscina",
        "resident": 2,
        "resident_name": "Juan Pérez",
        "resident_email": "juan@ejemplo.com",
        "start_time": "2025-09-25T14:00:00Z",
        "end_time": "2025-09-25T16:00:00Z",
        "status": "Confirmada",
        "total_paid": "30.00",
        "created_at": "2025-09-24T10:00:00Z"
    }
]
```

#### Crear Reserva
```http
POST /api/administration/reservations/
Authorization: Bearer {token}
Content-Type: application/json

{
    "common_area": 1,
    "start_time": "2025-09-26T15:00:00Z",
    "end_time": "2025-09-26T17:00:00Z",
    "total_paid": "30.00"
}
```
*Nota: El residente se asigna automáticamente al usuario autenticado*

---

## 7. 🚗 VEHÍCULOS

### Base URL: `/api/administration/vehicles/`

#### Listar Mis Vehículos
```http
GET /api/administration/vehicles/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "owner": 2,
        "owner_name": "Juan Pérez",
        "license_plate": "ABC123",
        "brand": "Toyota",
        "model": "Camry",
        "color": "Azul",
        "is_active": true,
        "created_at": "2025-09-24T08:00:00Z"
    }
]
```

#### Registrar Vehículo
```http
POST /api/administration/vehicles/
Authorization: Bearer {token}
Content-Type: application/json

{
    "license_plate": "XYZ789",
    "brand": "Honda",
    "model": "Civic",
    "color": "Blanco"
}
```

#### Actualizar Vehículo (PUT)
```http
PUT /api/administration/vehicles/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "license_plate": "XYZ789",
    "brand": "Honda",
    "model": "Civic",
    "color": "Negro",
    "is_active": true
}
```

---

## 8. 🐕 MASCOTAS

### Base URL: `/api/administration/pets/`

#### Listar Mis Mascotas
```http
GET /api/administration/pets/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "owner": 2,
        "owner_name": "Juan Pérez",
        "name": "Max",
        "species": "Perro",
        "breed": "Labrador",
        "age": 3,
        "is_active": true,
        "created_at": "2025-09-24T08:00:00Z"
    }
]
```

#### Registrar Mascota
```http
POST /api/administration/pets/
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Luna",
    "species": "Gato",
    "breed": "Persa",
    "age": 2
}
```

---

## 9. 👥 REGISTRO DE VISITANTES

### Base URL: `/api/administration/visitor-logs/`

#### Listar Registros
```http
GET /api/administration/visitor-logs/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "visitor_name": "María García",
        "visitor_id": "12345678",
        "unit_visited": 1,
        "unit_number": "101",
        "purpose": "Visita familiar",
        "entry_time": "2025-09-24T14:30:00Z",
        "exit_time": null,
        "status": "Activo",
        "created_at": "2025-09-24T14:30:00Z"
    }
]
```

#### Registrar Visitante
```http
POST /api/administration/visitor-logs/
Authorization: Bearer {token}
Content-Type: application/json

{
    "visitor_name": "Carlos López",
    "visitor_id": "87654321",
    "unit_visited": 1,
    "purpose": "Entrega de paquete"
}
```

#### Registrar Salida
```http
POST /api/administration/visitor-logs/{id}/register_exit/
Authorization: Bearer {token}
```

#### Visitantes Activos
```http
GET /api/administration/visitor-logs/active_visitors/
Authorization: Bearer {token}
```

#### Reporte Diario
```http
GET /api/administration/visitor-logs/daily_report/
Authorization: Bearer {token}
```

---

## 10. ✅ TAREAS

### Base URL: `/api/administration/tasks/`

#### Listar Tareas
```http
GET /api/administration/tasks/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "title": "Reparar tubería",
        "description": "Reparar tubería del baño principal",
        "status": "En Progreso",
        "assigned_to": 3,
        "assigned_to_name": "Pedro Mantenimiento",
        "created_by": 1,
        "created_by_name": "Admin User",
        "created_at": "2025-09-24T09:00:00Z",
        "completed_at": null
    }
]
```

#### Crear Tarea
```http
POST /api/administration/tasks/
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Limpieza de jardines",
    "description": "Poda y mantenimiento de áreas verdes",
    "assigned_to": 4
}
```

#### Mis Tareas Asignadas
```http
GET /api/administration/tasks/my_tasks/
Authorization: Bearer {token}
```

---

## 11. 💬 FEEDBACK

### Base URL: `/api/administration/feedback/`

#### Listar Feedback
```http
GET /api/administration/feedback/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "subject": "Problema con el ascensor",
        "message": "El ascensor hace ruidos extraños",
        "status": "Pendiente",
        "resident": 2,
        "resident_name": "Juan Pérez",
        "created_at": "2025-09-24T11:00:00Z",
        "updated_at": "2025-09-24T11:00:00Z"
    }
]
```

#### Enviar Feedback
```http
POST /api/administration/feedback/
Authorization: Bearer {token}
Content-Type: application/json

{
    "subject": "Sugerencia para mejoras",
    "message": "Sería bueno instalar cámaras de seguridad adicionales"
}
```

#### Mi Feedback
```http
GET /api/administration/feedback/my_feedback/
Authorization: Bearer {token}
```

#### Dashboard Administrativo
```http
GET /api/administration/feedback/admin_dashboard/
Authorization: Bearer {token}
```

---

## 12. 💳 PAGOS

### Base URL: `/api/administration/payments/`

#### Listar Transacciones
```http
GET /api/administration/payments/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "financial_fee": 1,
        "fee_description": "Cuota mensual Septiembre 2025",
        "fee_amount": "250.00",
        "resident": 2,
        "resident_name": "Juan Pérez",
        "transaction_id": "cs_test_12345",
        "amount": "250.00",
        "status": "Completado",
        "payment_method": "card",
        "created_at": "2025-09-24T10:00:00Z",
        "processed_at": "2025-09-24T10:05:00Z"
    }
]
```

#### Iniciar Pago
```http
POST /api/administration/payments/initiate_payment/
Authorization: Bearer {token}
Content-Type: application/json

{
    "financial_fee_id": 1
}
```

**Respuesta:**
```json
{
    "payment_url": "https://checkout.stripe.com/c/pay/cs_test_12345#fidkdWxOYHwnPyd1blpxblF2dktxaEdOZWtyUUJoUn9nYTdVcUtJcTdOZVxAVEYnPScpJ3VpbGtuQH11anZgYUxhJz8nNlV3dzFdaGpVPTFoM1hfPDZxPTI3J3gl",
    "transaction_id": "cs_test_12345",
    "existing": false
}
```

#### Mis Pagos
```http
GET /api/administration/payments/my_payments/
Authorization: Bearer {token}
```

---

## 13. 🏢 ROLES

### Base URL: `/api/administration/roles/`

#### Listar Roles
```http
GET /api/administration/roles/
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "name": "Administrador"
    },
    {
        "id": 2,
        "name": "Residente"
    },
    {
        "id": 3,
        "name": "Personal de Mantenimiento"
    }
]
```

---

# 🛠️ Ejemplos de Uso para Desarrollo Móvil

## Configuración Base (React Native/Flutter)

### React Native con Axios
```javascript
import axios from 'axios';

const API_BASE_URL = 'https://smart-condominium-backend.onrender.com';

// Configurar interceptor para token
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Agregar token a todas las requests
api.interceptors.request.use((config) => {
    const token = getStoredToken(); // Tu función para obtener token
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;
```

### Flutter con Dio
```dart
import 'package:dio/dio.dart';

class ApiService {
    static const String baseUrl = 'https://smart-condominium-backend.onrender.com';
    late Dio _dio;

    ApiService() {
        _dio = Dio(BaseOptions(
            baseUrl: baseUrl,
            headers: {'Content-Type': 'application/json'},
        ));

        _dio.interceptors.add(InterceptorsWrapper(
            onRequest: (options, handler) {
                final token = getStoredToken(); // Tu función para obtener token
                if (token != null) {
                    options.headers['Authorization'] = 'Bearer $token';
                }
                handler.next(options);
            },
        ));
    }
}
```

## Ejemplos Prácticos de Consumo

### 1. Login y Obtener Token
```javascript
// JavaScript/React Native
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            // Guardar tokens
            await AsyncStorage.setItem('accessToken', data.access);
            await AsyncStorage.setItem('refreshToken', data.refresh);
            return data;
        } else {
            throw new Error('Credenciales inválidas');
        }
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
}
```

### 2. Obtener Mi Perfil
```javascript
async function getMyProfile() {
    try {
        const response = await api.get('/api/administration/users/me/');
        return response.data;
    } catch (error) {
        if (error.response?.status === 401) {
            // Token expirado, redirect al login
            redirectToLogin();
        }
        throw error;
    }
}
```

### 3. Crear una Reserva
```javascript
async function createReservation(reservationData) {
    try {
        const response = await api.post('/api/administration/reservations/', {
            common_area: reservationData.commonAreaId,
            start_time: reservationData.startTime,
            end_time: reservationData.endTime,
            total_paid: reservationData.totalPaid,
        });
        
        if (response.status === 201) {
            return response.data;
        }
    } catch (error) {
        if (error.response?.status === 400) {
            // Error de validación
            console.error('Datos inválidos:', error.response.data);
        }
        throw error;
    }
}
```

### 4. Actualizar Mi Información (PUT)
```javascript
async function updateMyProfile(userData) {
    try {
        const response = await api.put(`/api/administration/users/${userId}/`, {
            first_name: userData.firstName,
            last_name: userData.lastName,
            phone_number: userData.phoneNumber,
            email: userData.email,
        });
        
        return response.data;
    } catch (error) {
        console.error('Error actualizando perfil:', error);
        throw error;
    }
}
```

### 5. Registrar Vehículo
```javascript
async function registerVehicle(vehicleData) {
    try {
        const response = await api.post('/api/administration/vehicles/', {
            license_plate: vehicleData.licensePlate,
            brand: vehicleData.brand,
            model: vehicleData.model,
            color: vehicleData.color,
        });
        
        return response.data;
    } catch (error) {
        if (error.response?.status === 400) {
            // Placa ya existe o datos inválidos
            alert('Error: ' + JSON.stringify(error.response.data));
        }
        throw error;
    }
}
```

### 6. Procesar Pago con Stripe
```javascript
async function initiatePayment(financialFeeId) {
    try {
        const response = await api.post('/api/administration/payments/initiate_payment/', {
            financial_fee_id: financialFeeId,
        });
        
        const { payment_url, transaction_id } = response.data;
        
        // Abrir WebView o navegador con payment_url
        Linking.openURL(payment_url);
        
        return { paymentUrl: payment_url, transactionId: transaction_id };
    } catch (error) {
        console.error('Error iniciando pago:', error);
        throw error;
    }
}
```

---

# 🔧 Manejo de Errores

## Estructura de Errores
```json
{
    "error": "Descripción del error",
    "detail": "Detalle específico"
}
```

## Errores de Validación (400)
```json
{
    "field_name": ["Este campo es requerido."],
    "another_field": ["Ingrese un valor válido."]
}
```

## Ejemplo de Manejo de Errores
```javascript
async function handleApiCall(apiFunction) {
    try {
        const result = await apiFunction();
        return result;
    } catch (error) {
        switch (error.response?.status) {
            case 400:
                // Error de validación
                showValidationErrors(error.response.data);
                break;
            case 401:
                // Token inválido
                redirectToLogin();
                break;
            case 403:
                // Sin permisos
                showError('No tienes permisos para realizar esta acción');
                break;
            case 404:
                // No encontrado
                showError('Recurso no encontrado');
                break;
            case 500:
                // Error del servidor
                showError('Error interno del servidor. Intenta más tarde.');
                break;
            default:
                showError('Error desconocido');
        }
        throw error;
    }
}
```

---

# 📱 Tips para Desarrollo Móvil

## 1. Gestión de Tokens
- Guardar tokens en almacenamiento seguro
- Implementar refresh automático de tokens
- Manejar expiración de tokens gracefully

## 2. Optimización de Requests
- Usar paginación cuando esté disponible
- Implementar cache local para datos que no cambian frecuentemente
- Usar pull-to-refresh en listas

## 3. Manejo de Estados Offline
- Implementar queue de requests para cuando se recupere conectividad
- Guardar datos críticos localmente
- Mostrar estados apropiados de carga/error

## 4. UI/UX
- Mostrar loaders durante requests
- Implementar retry automático para requests fallidas
- Validar datos en cliente antes de enviar al servidor

---

# 🧪 Testing

## Endpoints de Testing
- Status de la API: `GET /`
- Health check: `GET /api/`

## Usuario de Prueba
```
Email: admin@smartcondo.com
Password: admin123
```

---

*Documentación generada para Smart Condominium Backend v1.0*
*Última actualización: 24 de Septiembre de 2025*