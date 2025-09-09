# 🚀 Guía de Pruebas con Postman - Smart Condominium API

## 📋 Requisitos Previos

1. **Postman instalado** (Descarga desde: https://www.postman.com/downloads/)
2. **Servidor Django ejecutándose**:
   ```bash
   python manage.py runserver
   ```
3. **Datos iniciales cargados**:
   ```bash
   python manage.py load_initial_data
   ```

---

## 🔧 Configuración Inicial en Postman

### **Paso 1: Importar la Colección**
1. Abre Postman
2. Haz clic en **"Import"** (botón superior izquierdo)
3. Selecciona **"Upload Files"**
4. Navega a la carpeta `postman/` del proyecto
5. Selecciona `Smart_Condominium_API.postman_collection.json`
6. Haz clic en **"Import"**

### **Paso 2: Importar el Environment**
1. En Postman, haz clic en **"Import"** nuevamente
2. Selecciona `Smart_Condominium_Development.postman_environment.json`
3. Haz clic en **"Import"**

### **Paso 3: Activar el Environment**
1. En la esquina superior derecha, selecciona el dropdown de entornos
2. Elige **"Smart Condominium - Development"**
3. Verifica que aparezca seleccionado

---

## 🧪 Secuencia de Pruebas Recomendada

### **🔐 1. Autenticación (OBLIGATORIO PRIMERO)**

#### **1.1 Obtener Token JWT**
- **Carpeta:** Authentication → Obtener Token JWT
- **Método:** POST
- **URL:** `{{base_url}}/api/token/`
- **Body:**
  ```json
  {
      "email": "juan.perez@email.com",
      "password": "password123"
  }
  ```
- **Resultado esperado:** Status 200, tokens guardados automáticamente
- **⚠️ IMPORTANTE:** Este paso es obligatorio para todas las demás pruebas

#### **1.2 Login como Administrador (Opcional)**
- **Carpeta:** Authentication → Login Administrador
- **Credenciales:**
  ```json
  {
      "email": "admin@smartcondo.com",
      "password": "password123"
  }
  ```

### **👥 2. Gestión de Roles**

#### **2.1 Listar Roles**
- **Carpeta:** Roles → Listar Roles
- **Método:** GET
- **Resultado esperado:** Lista de roles existentes

#### **2.2 Crear Nuevo Rol**
- **Carpeta:** Roles → Crear Rol
- **Método:** POST
- **Body:**
  ```json
  {
      "name": "Portero"
  }
  ```

#### **2.3 Obtener Rol por ID**
- **Carpeta:** Roles → Obtener Rol por ID
- **Método:** GET
- **URL:** `{{base_url}}/api/administration/roles/1/`

#### **2.4 Actualizar Rol**
- **Carpeta:** Roles → Actualizar Rol
- **Método:** PUT
- **Nota:** Cambiar el ID en la URL por el del rol creado

#### **2.5 Eliminar Rol**
- **Carpeta:** Roles → Eliminar Rol
- **Método:** DELETE
- **Nota:** Solo funciona si el rol no tiene usuarios asignados

### **👤 3. Gestión de Usuarios**

#### **3.1 Listar Usuarios**
- **Carpeta:** Usuarios → Listar Usuarios
- **Método:** GET
- **Resultado esperado:** Lista con los usuarios iniciales

#### **3.2 Crear Nuevo Usuario**
- **Carpeta:** Usuarios → Crear Usuario
- **Método:** POST
- **Body:**
  ```json
  {
      "username": "nuevo_usuario",
      "email": "nuevo@ejemplo.com",
      "password": "password123",
      "first_name": "Nuevo",
      "last_name": "Usuario",
      "phone_number": "+52-555-9999",
      "role": 2
  }
  ```
- **Nota:** El campo `role` debe ser el ID de un rol existente

#### **3.3 Obtener Usuario por ID**
- **Carpeta:** Usuarios → Obtener Usuario por ID
- **Método:** GET

#### **3.4 Actualizar Usuario (PATCH)**
- **Carpeta:** Usuarios → Actualizar Usuario
- **Método:** PATCH
- **Body:** Solo los campos a actualizar
  ```json
  {
      "first_name": "Nombre Actualizado",
      "phone_number": "+52-555-8888"
  }
  ```

### **🏠 4. Gestión de Unidades Residenciales**

#### **4.1 Listar Unidades**
- **Carpeta:** Unidades Residenciales → Listar Unidades
- **Método:** GET

#### **4.2 Crear Nueva Unidad**
- **Carpeta:** Unidades Residenciales → Crear Unidad
- **Método:** POST
- **Body:**
  ```json
  {
      "unit_number": "C-301",
      "type": "Departamento",
      "floor": 3,
      "owner": null
  }
  ```

#### **4.3 Asignar Propietario a Unidad**
- **Carpeta:** Unidades Residenciales → Asignar Propietario a Unidad
- **Método:** PATCH
- **Body:**
  ```json
  {
      "owner": 2
  }
  ```
- **Nota:** El `owner` debe ser el ID de un usuario existente

#### **4.4 Obtener Unidad por ID**
- **Carpeta:** Unidades Residenciales → Obtener Unidad por ID
- **Método:** GET

### **🔒 5. Pruebas de Seguridad**

#### **5.1 Acceso Sin Token**
- **Carpeta:** Pruebas de Seguridad → Acceso Sin Token
- **Resultado esperado:** Status 401 Unauthorized

#### **5.2 Token Inválido**
- **Carpeta:** Pruebas de Seguridad → Token Inválido
- **Resultado esperado:** Status 401 Unauthorized

#### **5.3 Credenciales Incorrectas**
- **Carpeta:** Pruebas de Seguridad → Credenciales Incorrectas
- **Resultado esperado:** Status 401 Unauthorized

---

## 📊 Usuarios de Prueba Disponibles

| Email | Password | Rol | Descripción |
|-------|----------|-----|-------------|
| `admin@smartcondo.com` | `password123` | Administrador | Superusuario |
| `juan.perez@email.com` | `password123` | Residente | Usuario normal |
| `ana.garcia@email.com` | `password123` | Residente | Usuario normal |
| `carlos.seguridad@email.com` | `password123` | Guardia | Personal de seguridad |

---

## 🎯 Casos de Prueba Específicos

### **Test Case 1: Flujo Completo de Usuario**
1. Autenticarse como admin
2. Crear un nuevo rol "Conserje"
3. Crear un usuario con ese rol
4. Crear una unidad residencial
5. Asignar el usuario como propietario

### **Test Case 2: Validación de Restricciones**
1. Intentar crear un rol con nombre duplicado
2. Intentar crear un usuario con email duplicado
3. Intentar crear una unidad con número duplicado

### **Test Case 3: Pruebas de Autorización**
1. Hacer login como usuario normal
2. Intentar crear/modificar usuarios (debería funcionar según permisos)
3. Verificar que se respetan las restricciones de seguridad

---

## 🔍 Verificaciones Importantes

### **Códigos de Estado HTTP Esperados:**
- ✅ **200**: GET exitoso
- ✅ **201**: POST exitoso (creación)
- ✅ **204**: DELETE exitoso
- ❌ **400**: Bad Request (datos inválidos)
- ❌ **401**: Unauthorized (sin token o token inválido)
- ❌ **404**: Not Found (recurso no existe)

### **Estructura de Respuestas:**
- **Lista:** `{"count": X, "results": [...]}`
- **Detalle:** `{"id": X, "field1": "value", ...}`
- **Error:** `{"detail": "Error message"}`

---

## 🛠️ Troubleshooting

### **Problema: "Request failed with status code 401"**
**Solución:** 
- Verifica que obtuviste el token JWT primero
- Revisa que el environment esté seleccionado
- Confirma que las credenciales son correctas

### **Problema: "Connection refused"**
**Solución:**
- Verifica que el servidor Django esté ejecutándose
- Confirma que la URL base sea `http://127.0.0.1:8000`

### **Problema: "Token expired"**
**Solución:**
- Ejecuta "Refrescar Token" o vuelve a hacer login

---

## 📝 Variables Automáticas

La colección incluye scripts que automáticamente:
- ✅ Guardan los tokens JWT en variables de entorno
- ✅ Los utilizan en requests subsecuentes
- ✅ Ejecutan validaciones básicas

**¡Listo para probar! 🚀**
