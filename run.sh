#!/bin/bash

# Script de inicio para el contenedor Docker
# Aplicar migraciones de la base de datos
echo "Aplicando migraciones de la base de datos..."
python manage.py migrate

# Iniciar el servidor Gunicorn
echo "Iniciando servidor Gunicorn..."
gunicorn smartcondo_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}