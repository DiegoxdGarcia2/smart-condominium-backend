# Usar imagen base ligera de Python
FROM python:3.11-slim-bullseye

# Configurar variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Dar permisos de ejecución al script de inicio
RUN chmod +x run.sh

# Exponer puerto 8000
EXPOSE 8000

# Comando por defecto: ejecutar el script de inicio
CMD ["./run.sh"]