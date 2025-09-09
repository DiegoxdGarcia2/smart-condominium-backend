# 🔥 PRUEBAS RÁPIDAS PARA POSTMAN - Endpoint /me/

## 🎯 Servidor Activo
**URL Base:** http://127.0.0.1:8000

## 📝 Secuencia de Pruebas

### 1️⃣ PRIMERA PRUEBA: Login + /me/

#### A) Login Administrador
```
Method: POST
URL: http://127.0.0.1:8000/api/token/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "email": "admin@smartcondo.com",
    "password": "password123"
}
```
**Resultado esperado:** Status 200 + tokens

#### B) Obtener Mi Perfil (/me/)
```
Method: GET
URL: http://127.0.0.1:8000/api/administration/users/me/
Headers: 
- Authorization: Bearer [PEGAR_TOKEN_AQUÍ]
- Content-Type: application/json
```
**Resultado esperado:** Datos del admin

---

### 2️⃣ SEGUNDA PRUEBA: Residente + /me/

#### A) Login Residente
```
Method: POST
URL: http://127.0.0.1:8000/api/token/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "email": "juan.perez@email.com",
    "password": "password123"
}
```

#### B) Obtener Mi Perfil (/me/)
```
Method: GET
URL: http://127.0.0.1:8000/api/administration/users/me/
Headers: Authorization: Bearer [NUEVO_TOKEN_AQUÍ]
```
**Resultado esperado:** Datos de Juan Pérez (diferentes al admin)

---

### 3️⃣ TERCERA PRUEBA: Sin Autenticación

```
Method: GET
URL: http://127.0.0.1:8000/api/administration/users/me/
Headers: (SIN Authorization header)
```
**Resultado esperado:** Status 401 Unauthorized

---

## 🚀 Instrucciones Rápidas para Postman

### Opción A: Usar la Colección (Recomendado)
1. **Import** > Seleccionar `Smart_Condominium_API.postman_collection.json`
2. **Environment** > Crear con `base_url: http://127.0.0.1:8000`
3. **Ejecutar:** "Login Administrador" (guarda tokens automáticamente)
4. **Ejecutar:** "Obtener Mi Perfil (/me/)" 

### Opción B: Requests Manuales
1. **Crear nuevo request**
2. **Copiar URLs y datos de arriba**
3. **Copiar tokens manualmente**

## 📊 Respuestas Expected

### Login Exitoso:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### /me/ Admin:
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
    "date_joined": "2025-09-07T06:04:33Z"
}
```

### /me/ Residente:
```json
{
    "id": 2,
    "username": "juan.perez",
    "email": "juan.perez@email.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone_number": "+52-555-0002",
    "role": 2,
    "role_name": "Residente",
    "is_active": true,
    "date_joined": "2025-09-07T06:04:33Z"
}
```

### Sin Auth (Error):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## ✅ Checklist Rápido
- [ ] Servidor corriendo (✅ Ya está activo)
- [ ] Postman abierto
- [ ] Login exitoso (status 200)
- [ ] Token copiado en Authorization header
- [ ] /me/ retorna status 200 con mis datos
- [ ] Sin token retorna 401

**¡Listo para probar! El endpoint /me/ está funcionando perfectamente.**
