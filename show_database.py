#!/usr/bin/env python3
"""
Script para consultar la base de datos SQLite actual
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcondo_backend.settings')
django.setup()

from django.db import connection
from administration.models import Role, User, ResidentialUnit

def show_database_info():
    print("="*50)
    print("📊 INFORMACIÓN DE LA BASE DE DATOS")
    print("="*50)
    
    # Mostrar el archivo de base de datos
    from django.conf import settings
    db_name = settings.DATABASES['default']['NAME']
    print(f"📁 Archivo de BD: {db_name}")
    print(f"🔧 Motor: {settings.DATABASES['default']['ENGINE']}")
    
    # Mostrar tablas
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n📋 TABLAS EN LA BASE DE DATOS ({len(tables)} total):")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]} ({count} registros)")
    
    print("\n" + "="*50)
    print("📊 DATOS ACTUALES")
    print("="*50)
    
    # Mostrar roles
    print(f"\n👥 ROLES ({Role.objects.count()} registros):")
    for role in Role.objects.all():
        user_count = User.objects.filter(role=role).count()
        print(f"  - ID: {role.id} | {role.name} ({user_count} usuarios)")
    
    # Mostrar usuarios
    print(f"\n👤 USUARIOS ({User.objects.count()} registros):")
    for user in User.objects.all()[:10]:  # Mostrar solo los primeros 10
        role_name = user.role.name if user.role else "Sin rol"
        print(f"  - ID: {user.id} | {user.email} | {role_name}")
    
    # Mostrar unidades
    print(f"\n🏠 UNIDADES RESIDENCIALES ({ResidentialUnit.objects.count()} registros):")
    for unit in ResidentialUnit.objects.all():
        owner_name = f"{unit.owner.first_name} {unit.owner.last_name}" if unit.owner else "Sin propietario"
        print(f"  - ID: {unit.id} | {unit.unit_number} | {unit.type} | {owner_name}")
    
    print("\n" + "="*50)
    print("🔍 CÓMO VER LA BASE DE DATOS:")
    print("="*50)
    print("1. DB Browser for SQLite: https://sqlitebrowser.org/")
    print(f"   Abrir archivo: {db_name}")
    print("\n2. VS Code con extensión SQLite Viewer")
    print("   Instalar: SQLite Viewer extension")
    print(f"   Abrir: {db_name}")
    print("\n3. Admin de Django:")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("   User: admin@smartcondo.com")
    print("   Pass: password123")

if __name__ == "__main__":
    show_database_info()
