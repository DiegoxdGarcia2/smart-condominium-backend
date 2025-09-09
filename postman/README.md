# 📁 Archivos de Postman para Smart Condominium API

Este directorio contiene todos los archivos necesarios para probar la API del Smart Condominium Backend usando Postman.

## 📋 Archivos Incluidos

### 🔧 **Archivos de Configuración**
- `Smart_Condominium_API.postman_collection.json` - Colección completa con todos los endpoints
- `Smart_Condominium_Development.postman_environment.json` - Variables de entorno para desarrollo

### 📖 **Documentación**
- `POSTMAN_GUIDE.md` - Guía completa paso a paso
- `README.md` - Este archivo

## 🚀 Inicio Rápido

### **1. Importar en Postman**
1. Abre Postman
2. Import → Upload Files
3. Selecciona ambos archivos `.json`
4. Activa el environment "Smart Condominium - Development"

### **2. Iniciar Servidor**
```bash
cd smart-condominium-backend
python manage.py runserver
```

### **3. Primera Prueba**
1. Ve a Authentication → "Obtener Token JWT"
2. Ejecuta la request
3. ¡El token se guardará automáticamente!

## 🎯 Endpoints Incluidos

### 🔐 **Autenticación**
- Obtener Token JWT
- Refrescar Token  
- Login Administrador

### 👥 **Roles**
- Listar, Crear, Obtener, Actualizar, Eliminar

### 👤 **Usuarios**
- Listar, Crear, Obtener, Actualizar

### 🏠 **Unidades Residenciales**
- Listar, Crear, Obtener, Asignar Propietario

### 🔒 **Pruebas de Seguridad**
- Acceso sin token
- Token inválido
- Credenciales incorrectas

## 📊 Credenciales de Prueba

| Usuario | Email | Password | Rol |
|---------|-------|----------|-----|
| Admin | `admin@smartcondo.com` | `password123` | Administrador |
| Juan | `juan.perez@email.com` | `password123` | Residente |
| Ana | `ana.garcia@email.com` | `password123` | Residente |
| Carlos | `carlos.seguridad@email.com` | `password123` | Guardia |

## ⚡ Características Automáticas

- ✅ **Auto-save de tokens JWT**
- ✅ **Variables de entorno automáticas**
- ✅ **Validaciones de respuesta**
- ✅ **Headers pre-configurados**

## 🛠️ Personalización

Para modificar la URL base o agregar nuevos endpoints:

1. **Cambiar URL:** Environment → `base_url`
2. **Nuevos endpoints:** Collection → Add Request
3. **Variables:** Environment → Add Variable

---

**¡Todo listo para probar la API! 🎉**

Lee `POSTMAN_GUIDE.md` para instrucciones detalladas.
