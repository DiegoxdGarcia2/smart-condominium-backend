#!/usr/bin/env python3
"""
Script para verificar usuarios en base de datos local
Ejecutar en el proyecto local para ver qué usuarios deberían estar en producción
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcondo_backend.settings')

try:
    django.setup()
    from administration.models import User, Role
    
    print("🔍 USUARIOS EN BASE DE DATOS LOCAL")
    print("=" * 50)
    
    # Verificar si hay usuarios
    users = User.objects.all()
    print(f"📊 Total de usuarios: {users.count()}")
    
    if users.count() > 0:
        print("\n👥 Lista de usuarios:")
        for i, user in enumerate(users, 1):
            print(f"   {i}. Email: {user.email}")
            print(f"      Nombre: {user.first_name} {user.last_name}")
            print(f"      Staff: {user.is_staff}")
            print(f"      Superuser: {user.is_superuser}")
            print(f"      Activo: {user.is_active}")
            if user.role:
                print(f"      Rol: {user.role.name}")
            print(f"      Fecha: {user.date_joined}")
            print()
        
        print("🔑 CREDENCIALES PARA PROBAR EN POSTMAN:")
        print("   (Usa cualquiera de estos emails con la contraseña que hayas usado)")
        for user in users:
            if user.is_superuser or user.is_staff:
                print(f"   ✅ {user.email} (Admin/Staff)")
            else:
                print(f"   - {user.email}")
    else:
        print("⚠️ No hay usuarios en la base de datos local")
        print("💡 Necesitas crear un superusuario:")
        print("   python manage.py createsuperuser")
    
    # Verificar roles
    roles = Role.objects.all()
    print(f"\n📋 Roles disponibles: {roles.count()}")
    for role in roles:
        print(f"   - {role.name}")
    
    print("\n" + "=" * 50)
    print("📋 INSTRUCCIONES:")
    print("1. Si ves usuarios aquí, deberían estar en producción")
    print("2. Usa los emails mostrados en Postman")
    print("3. Si no recuerdas las contraseñas, puedes:")
    print("   - Cambiarlas en el admin local")
    print("   - O crear un nuevo superusuario")
    print("=" * 50)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Asegúrate de ejecutar este script en el directorio del proyecto local")
    print("💡 Y que tengas la base de datos local funcionando")