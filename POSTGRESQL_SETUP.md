# Instrucciones para Cambiar a PostgreSQL

## Problema Actual
Windows requiere compiladores C++ para instalar psycopg2-binary desde código fuente.

## Soluciones:

### Opción A: Usar Wheel Precompilado
```bash
pip install --only-binary=psycopg2-binary psycopg2-binary
```

### Opción B: Usar psycopg (versión 3)
```bash
pip uninstall psycopg2-binary
pip install psycopg[binary]
```

### Opción C: Instalar Visual Studio Build Tools
1. Descargar: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Instalar "C++ build tools"
3. Luego: pip install psycopg2-binary

## Configuración de settings.py

Descomenta y configura:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='smartcondo_db'),
        'USER': config('DB_USER', default='smartcondo_user'),
        'PASSWORD': config('DB_PASSWORD', default='tu_password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## Archivo .env

```
DB_NAME=smartcondo_db
DB_USER=smartcondo_user
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432
```

## Migrar Datos

```bash
# Hacer backup de SQLite (opcional)
python manage.py dumpdata > backup.json

# Cambiar configuración a PostgreSQL
# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar datos iniciales
python manage.py load_initial_data

# O restaurar backup (opcional)
python manage.py loaddata backup.json
```
