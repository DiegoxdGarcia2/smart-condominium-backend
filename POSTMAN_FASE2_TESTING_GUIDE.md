# 🧪 GUÍA DE PRUEBAS - FASE 2: Gestión Financiera y Comunicación

## 📋 Colección Postman Especializada

**Archivo:** `Smart_Condominium_Fase2_API.postman_collection.json`

Esta colección está diseñada específicamente para probar las **nuevas funcionalidades de la Fase 2**:
- 📢 **Sistema de Comunicados (Announcements)**
- 💰 **Sistema de Cuotas Financieras (Financial Fees)**

## 🚀 Configuración Rápida

### 1. Importar la Colección
1. **Abrir Postman**
2. **Import** > Seleccionar `Smart_Condominium_Fase2_API.postman_collection.json`
3. La colección se configurará automáticamente con:
   - **Base URL:** `http://127.0.0.1:8000`
   - **Variables de entorno** incluidas

### 2. Verificar Servidor
```bash
# Asegúrate de que el servidor esté corriendo
python manage.py runserver 8000
```

## 📂 Estructura de la Colección

### 🔐 **1. Autenticación**
- **Login Administrador** → `admin@smartcondo.com`
- **Login Residente Juan** → `juan.perez@email.com`
- ✅ **Auto-guarda tokens** en variables de entorno

### 📢 **2. Comunicados (Announcements)**
- **Listar Todos** → `GET /announcements/`
- **Crear Nuevo** → `POST /announcements/`
- **Obtener Específico** → `GET /announcements/{id}/`
- **Actualizar** → `PUT /announcements/{id}/`
- **Crear Emergencia** → `POST /announcements/` (ejemplo urgente)

### 💰 **3. Cuotas Financieras (Financial Fees)**
- **Listar Todas** → `GET /financial-fees/`
- **Crear Extraordinaria** → `POST /financial-fees/`
- **Obtener Específica** → `GET /financial-fees/{id}/`
- **Marcar como Pagada** → `PATCH /financial-fees/{id}/`
- **Crear Mantenimiento** → `POST /financial-fees/`
- **Crear Vencida** → `POST /financial-fees/` (ejemplo vencido)

### 🧪 **4. Pruebas de Integración**
- **Mi Perfil** → `GET /users/me/`
- **Listar Unidades** → `GET /residential-units/`
- **Sin Autenticación** → Test que debe fallar con 401

## 🎯 Secuencia de Pruebas Recomendada

### **Paso 1: Autenticación**
```
1. Ejecutar "Login Administrador"
   ✅ Verifica que se guarden los tokens automáticamente
```

### **Paso 2: Probar Comunicados**
```
2. "Listar Todos los Comunicados"
   ✅ Debe mostrar los 3 comunicados de ejemplo

3. "Crear Nuevo Comunicado"  
   ✅ Crea reunión de administración
   ✅ Guarda ID automáticamente

4. "Actualizar Comunicado"
   ✅ Modifica el comunicado creado

5. "Crear Comunicado de Emergencia"
   ✅ Crea aviso urgente de corte de agua
```

### **Paso 3: Probar Cuotas Financieras**
```
6. "Listar Todas las Cuotas"
   ✅ Debe mostrar las 5 cuotas de ejemplo

7. "Crear Nueva Cuota Extraordinaria"
   ✅ Crea cuota de reparación elevador
   ✅ Guarda ID automáticamente

8. "Marcar Cuota como Pagada"
   ✅ Cambia estado a "Pagado"

9. "Crear Cuota de Mantenimiento"
   ✅ Crea cuota regular de octubre

10. "Crear Cuota Vencida"
    ✅ Crea multa con estado vencido
```

### **Paso 4: Validaciones**
```
11. "Mi Perfil" 
    ✅ Confirma usuario autenticado

12. "Prueba Sin Autenticación"
    ✅ Debe fallar con 401 Unauthorized
```

## 📊 Respuestas Esperadas

### **Login Exitoso:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### **Comunicado Creado:**
```json
{
    "id": 4,
    "title": "Reunión de Administración - Octubre 2025",
    "content": "Estimados residentes, les convocamos...",
    "author": 1,
    "author_name": "María Administradora",
    "author_email": "admin@smartcondo.com",
    "created_at": "2025-09-08T23:30:00Z"
}
```

### **Cuota Financiera Creada:**
```json
{
    "id": 6,
    "unit": 1,
    "unit_number": "A-101",
    "unit_owner": "Juan Pérez",
    "description": "Cuota extraordinaria - Reparación elevador",
    "amount": "2500.00",
    "due_date": "2025-10-15",
    "status": "Pendiente",
    "created_at": "2025-09-08T23:30:00Z"
}
```

## 🔧 Funcionalidades Probadas

### ✅ **Sistema de Comunicados**
- [x] Crear comunicados con autor automático
- [x] Listar ordenados por fecha
- [x] Actualizar contenido
- [x] Información del autor incluida
- [x] Fecha de creación automática

### ✅ **Sistema Financiero**
- [x] Crear cuotas por unidad
- [x] Estados: Pendiente, Pagado, Vencido
- [x] Montos decimales precisos
- [x] Fechas de vencimiento
- [x] Información de unidad y propietario

### ✅ **Seguridad**
- [x] Autenticación JWT requerida
- [x] Tokens guardados automáticamente
- [x] Error 401 sin autenticación
- [x] Permisos por endpoint

## 🎯 Scripts de Test Automáticos

La colección incluye **scripts de validación automática**:

```javascript
// Ejemplo: Login exitoso
if (pm.response.code === 200) {
    const responseJson = pm.response.json();
    pm.environment.set('access_token', responseJson.access);
    pm.test('Login exitoso - Tokens guardados', function () {
        pm.expect(responseJson.access).to.exist;
    });
}
```

## 📱 Credenciales Incluidas

```
👑 Admin:     admin@smartcondo.com     / password123
🏠 Residente: juan.perez@email.com     / password123
```

## ✅ Checklist de Pruebas

- [ ] Servidor Django corriendo (puerto 8000)
- [ ] Colección importada en Postman
- [ ] Login administrador exitoso
- [ ] Comunicados: Listar, Crear, Actualizar ✅
- [ ] Cuotas: Listar, Crear, Cambiar estado ✅
- [ ] Prueba sin autenticación (401) ✅
- [ ] Endpoint /me/ funcionando ✅

**¡Lista para probar todas las funcionalidades de la Fase 2! 🚀**
