# 🧪 GUÍA PASO A PASO: Probar Endpoint /me/ en Postman

## 📋 Prerrequisitos
- ✅ Servidor Django corriendo en: **http://127.0.0.1:8000/**
- ✅ Postman instalado
- ✅ Colección Smart_Condominium_API.postman_collection.json importada

## 🚀 Pasos para Probar el Endpoint /me/

### Paso 1: Configurar Variables de Entorno en Postman
1. **Abrir Postman**
2. **Crear/Editar Environment:**
   - Click en "Environments" (icono de engranaje)
   - Crear nuevo environment o editar existente
   - Añadir variables:
     ```
     base_url: http://127.0.0.1:8000
     access_token: (se llenará automáticamente)
     refresh_token: (se llenará automáticamente)
     ```

### Paso 2: Importar la Colección
1. **Import Collection:**
   - File > Import
   - Seleccionar: `Smart_Condominium_API.postman_collection.json`
   - Click "Import"

### Paso 3: Autenticarse (Obtener Token)
1. **Ir a carpeta "Autenticación"**
2. **Ejecutar "Login Administrador":**
   ```
   POST {{base_url}}/api/token/
   ```
   - Body (JSON):
   ```json
   {
       "email": "admin@smartcondo.com",
       "password": "password123"
   }
   ```
   - Click "Send"
   - ✅ **Verificar:** Status 200 y tokens guardados automáticamente

### Paso 4: Probar el Endpoint /me/
1. **Ir a carpeta "Usuarios"**
2. **Seleccionar "Obtener Mi Perfil (/me)"**
3. **Verificar configuración:**
   ```
   Method: GET
   URL: {{base_url}}/api/administration/users/me/
   Headers:
   - Authorization: Bearer {{access_token}}
   ```
4. **Click "Send"**

### 📊 Resultado Esperado

#### ✅ Respuesta Exitosa (Status 200)
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@smartcondo.com",
    "first_name": "Administrador",
    "last_name": "Sistema",
    "phone_number": "+52-555-0001",
    "role": 1,
    "role_name": "Administrador",
    "is_active": true,
    "date_joined": "2025-09-07T06:04:33.123456Z"
}
```

## 🔄 Pruebas Adicionales

### Probar con Diferentes Usuarios
1. **Login como Residente:**
   ```json
   {
       "email": "juan.perez@email.com",
       "password": "password123"
   }
   ```
   - Ejecutar `/me/` y verificar que retorna datos de Juan Pérez

2. **Login como Guardia:**
   ```json
   {
       "email": "carlos.seguridad@email.com",
       "password": "password123"
   }
   ```
   - Ejecutar `/me/` y verificar que retorna datos del guardia

### Probar Sin Autenticación
1. **Eliminar token:**
   - En Headers, borrar o comentar `Authorization`
2. **Ejecutar `/me/`**
3. **Resultado esperado:**
   ```json
   Status: 401 Unauthorized
   {
       "detail": "Authentication credentials were not provided."
   }
   ```

## 🛠️ Troubleshooting

### Error 401 - No autorizado
- ✅ Verificar que el token está en Headers
- ✅ Verificar que el token no ha expirado
- ✅ Re-ejecutar login para obtener nuevo token

### Error 404 - Not Found
- ✅ Verificar URL: `/api/administration/users/me/`
- ✅ Verificar que base_url es correcta
- ✅ Verificar que el servidor está corriendo

### Error 500 - Server Error
- ✅ Verificar logs del servidor Django
- ✅ Verificar que PostgreSQL está funcionando

## 📱 Credenciales de Prueba Disponibles

```
Admin:       admin@smartcondo.com        / password123
Residente 1: juan.perez@email.com        / password123  
Residente 2: ana.garcia@email.com        / password123
Guardia:     carlos.seguridad@email.com  / password123
```

## ✅ Checklist de Verificación

- [ ] Servidor Django corriendo en puerto 8000
- [ ] Environment configurado en Postman
- [ ] Colección importada correctamente
- [ ] Login exitoso (tokens obtenidos)
- [ ] Endpoint /me/ responde con status 200
- [ ] Datos del usuario correctos en respuesta
- [ ] Prueba sin token retorna 401
- [ ] Pruebas con diferentes usuarios funcionan

**¡El endpoint /me/ está listo para usar!**
