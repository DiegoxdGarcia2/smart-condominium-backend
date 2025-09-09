# 🐘 Configuración de PostgreSQL para Smart Condominium

## 📋 Requisitos Previos

1. **PostgreSQL instalado** (https://www.postgresql.org/download/)
2. **pgAdmin instalado** (incluido con PostgreSQL)

## 🔧 Pasos de Configuración

### **Paso 1: Crear la Base de Datos**

#### **Opción A: Usando pgAdmin (Interfaz Gráfica)**
1. Abre pgAdmin
2. Conecta al servidor PostgreSQL local
3. Clic derecho en "Databases" → "Create" → "Database"
4. Nombre: `SmartCondominiumDB`
5. Owner: `postgres`
6. Clic en "Save"

#### **Opción B: Usando SQL Query**
1. Abre pgAdmin → Query Tool
2. Ejecuta el script: `database/create_database.sql`

#### **Opción C: Desde línea de comandos**
```bash
psql -U postgres -c "CREATE DATABASE \"SmartCondominiumDB\";"
```

### **Paso 2: Verificar Configuración**

#### **Configuración Actual del Proyecto:**
- **Base de Datos:** SmartCondominiumDB
- **Usuario:** postgres
- **Contraseña:** admin123
- **Host:** localhost
- **Puerto:** 5432

#### **Archivo .env creado:**
```env
DB_NAME=SmartCondominiumDB
DB_USER=postgres
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
```

### **Paso 3: Ejecutar Migraciones**

```bash
# Verificar conexión
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Cargar datos iniciales
python manage.py load_initial_data

# Crear superusuario
python manage.py createsuperuser
```

### **Paso 4: Verificar en pgAdmin**

1. Refrescar en pgAdmin
2. Navegar a: SmartCondominiumDB → Schemas → public → Tables
3. Deberías ver las tablas:
   - administration_role
   - administration_user
   - administration_residentialunit
   - django_migrations
   - auth_permission
   - etc.

## 🔍 Verificación de Datos

### **Consultas SQL para verificar:**

```sql
-- Ver roles
SELECT * FROM administration_role;

-- Ver usuarios
SELECT id, email, first_name, last_name FROM administration_user;

-- Ver unidades residenciales
SELECT * FROM administration_residentialunit;
```

## 🛠️ Troubleshooting

### **Error: "connection to server on socket"**
- Verificar que PostgreSQL esté ejecutándose
- Verificar puerto 5432 disponible

### **Error: "authentication failed"**
- Verificar usuario/contraseña en .env
- Verificar configuración pg_hba.conf

### **Error: "database does not exist"**
- Crear la base de datos SmartCondominiumDB
- Verificar nombre exacto (case-sensitive)

## 📊 Conectar pgAdmin

1. **Abrir pgAdmin**
2. **Servidor ya configurado** (durante instalación)
3. **Expandir:** Servers → PostgreSQL → Databases → SmartCondominiumDB
4. **Ver tablas:** Schemas → public → Tables

## ✅ Verificación Final

Ejecutar para verificar que todo funciona:
```bash
python show_database.py
```

¡La migración a PostgreSQL está completa! 🎉
