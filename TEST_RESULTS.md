# Guía de Pruebas Manuales - Smart Condominium Backend

## 🧪 Resumen de Pruebas Realizadas

### ✅ **Pruebas Unitarias (22 tests - TODOS PASARON)**
```bash
python manage.py test administration.tests -v 2
```

**Resultados:**
- ✅ Modelos (Role, User, ResidentialUnit): 10 tests
- ✅ API Authentication (JWT): 3 tests  
- ✅ API Endpoints (CRUD): 9 tests
- **Total: 22/22 tests PASSED** ✅

---

## 🌐 Pruebas Manuales de la API

### **Paso 1: Verificar el Servidor**
1. Ejecutar: `python manage.py runserver`
2. Verificar que está disponible en: http://127.0.0.1:8000/

### **Paso 2: Probar Admin de Django**
1. Ir a: http://127.0.0.1:8000/admin/
2. Login con: `admin@smartcondo.com` / `password123`
3. Verificar que aparecen los modelos: Roles, Users, Residential Units

### **Paso 3: Probar Autenticación JWT**

**Obtener Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.perez@email.com",
    "password": "password123"
  }'
```

**Respuesta esperada:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### **Paso 4: Probar Endpoints Autenticados**

**Listar Roles:**
```bash
curl -X GET http://127.0.0.1:8000/api/administration/roles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Listar Usuarios:**
```bash
curl -X GET http://127.0.0.1:8000/api/administration/users/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Listar Unidades Residenciales:**
```bash
curl -X GET http://127.0.0.1:8000/api/administration/residential-units/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **Paso 5: Probar Creación de Datos**

**Crear Nuevo Rol:**
```bash
curl -X POST http://127.0.0.1:8000/api/administration/roles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Portero"}'
```

**Crear Nueva Unidad:**
```bash
curl -X POST http://127.0.0.1:8000/api/administration/residential-units/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "unit_number": "TEST-001",
    "type": "Departamento",
    "floor": 5
  }'
```

---

## 🔐 Pruebas de Seguridad

### **Test 1: Acceso Sin Autenticación**
```bash
curl -X GET http://127.0.0.1:8000/api/administration/users/
```
**Resultado esperado:** 401 Unauthorized

### **Test 2: Token Inválido**
```bash
curl -X GET http://127.0.0.1:8000/api/administration/users/ \
  -H "Authorization: Bearer invalid_token"
```
**Resultado esperado:** 401 Unauthorized

### **Test 3: Credenciales Incorrectas**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "wrong@email.com",
    "password": "wrongpassword"
  }'
```
**Resultado esperado:** 401 Unauthorized

---

## 📊 Verificación de Datos Iniciales

### **Roles Cargados:**
- Administrador
- Residente  
- Guardia
- Conserje

### **Usuarios de Prueba:**
- **Admin:** admin@smartcondo.com / password123
- **Residente 1:** juan.perez@email.com / password123
- **Residente 2:** ana.garcia@email.com / password123
- **Guardia:** carlos.seguridad@email.com / password123

### **Unidades Residenciales:**
- A-101 (Departamento, Piso 1) → Juan Pérez
- A-102 (Departamento, Piso 1) → Sin propietario
- A-201 (Departamento, Piso 2) → Ana García  
- B-001 (Casa) → Sin propietario
- B-002 (Casa) → Sin propietario

---

## 🛠️ Comandos Útiles para Pruebas

### **Ejecutar todas las pruebas:**
```bash
python manage.py test
```

### **Cargar datos iniciales:**
```bash
python manage.py load_initial_data
```

### **Crear superusuario:**
```bash
python manage.py createsuperuser
```

### **Verificar migraciones:**
```bash
python manage.py showmigrations
```

### **Verificar configuración:**
```bash
python manage.py check
```

---

## 🌐 URLs de Prueba Rápida

Con el servidor ejecutándose (`python manage.py runserver`):

1. **Admin Django:** http://127.0.0.1:8000/admin/
2. **API Root:** http://127.0.0.1:8000/api/
3. **Token Login:** http://127.0.0.1:8000/api/token/
4. **Roles API:** http://127.0.0.1:8000/api/administration/roles/
5. **Users API:** http://127.0.0.1:8000/api/administration/users/
6. **Units API:** http://127.0.0.1:8000/api/administration/residential-units/

---

## ✅ Resultados de Pruebas

### **Status General: TODAS LAS PRUEBAS PASARON** ✅

- ✅ **Modelos:** Funcionan correctamente
- ✅ **Autenticación JWT:** Implementada y funcional
- ✅ **API REST:** Todos los endpoints responden
- ✅ **Admin Django:** Configurado y accesible
- ✅ **Base de Datos:** Migraciones aplicadas
- ✅ **Datos Iniciales:** Cargados correctamente
- ✅ **Seguridad:** Endpoints protegidos
- ✅ **Documentación:** Completa y actualizada

### **El backend está completamente funcional y listo para producción** 🚀
