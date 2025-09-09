-- Script para crear la base de datos SmartCondominiumDB en PostgreSQL
-- Ejecutar este script en pgAdmin o desde psql como superusuario

-- Crear la base de datos
CREATE DATABASE "SmartCondominiumDB"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Crear usuario específico (opcional, puedes usar postgres directamente)
-- CREATE USER smartcondo_user WITH PASSWORD 'admin123';
-- GRANT ALL PRIVILEGES ON DATABASE "SmartCondominiumDB" TO smartcondo_user;

-- Comentarios:
-- 1. La base de datos se llama SmartCondominiumDB
-- 2. Usuario: postgres
-- 3. Contraseña: admin123 (como en tu configuración)
-- 4. Puerto: 5432 (por defecto)
-- 5. Host: localhost
