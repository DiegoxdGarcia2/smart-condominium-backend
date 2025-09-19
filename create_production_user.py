#!/usr/bin/env python3
"""
Script para crear un usuario de prueba directamente en producción
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django para producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcondo_backend.settings')

# Configurar variables de entorno de producción
os.environ['DATABASE_URL'] = 'postgresql://smartcondo_user:wSXpUcbPBo6E5PcCZPGJZwJJ3yIimnMo@dpg-cs7u3b5umphs73fegr20-a.oregon-postgres.render.com/smartcondo_db'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'tu-secret-key-de-produccion'

try:
    django.setup()
    from administration.models import User, Role
    
    print("🔧 Creando usuario de prueba en producción...")
    
    # Crear rol admin si no existe
    admin_role, created = Role.objects.get_or_create(name='Administrador')
    if created:
        print("✅ Rol Administrador creado")
    else:
        print("✅ Rol Administrador ya existe")
    
    # Crear usuario de prueba
    email = "admin@smartcondo.com"
    password = "admin123"
    
    try:
        # Verificar si el usuario ya existe
        user = User.objects.get(email=email)
        print(f"✅ Usuario {email} ya existe")
        
        # Actualizar contraseña por si acaso
        user.set_password(password)
        user.save()
        print("✅ Contraseña actualizada")
        
    except User.DoesNotExist:
        # Crear nuevo usuario
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name="Admin",
            last_name="Test",
            role=admin_role,
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Usuario {email} creado exitosamente")
    
    # Verificar autenticación
    from django.contrib.auth import authenticate
    auth_user = authenticate(email=email, password=password)
    if auth_user:
        print(f"✅ Autenticación exitosa para {email}")
        
        # Probar token JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(auth_user)
        access_token = refresh.access_token
        print(f"✅ Token JWT generado: {str(access_token)[:50]}...")
        
    else:
        print(f"❌ Falló la autenticación para {email}")
    
    print("\n🎯 Credenciales para Postman:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   URL: https://smart-condominium-backend-fuab.onrender.com/api/token/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()