#!/usr/bin/env python3
"""
Crear un usuario básico usando el endpoint del admin de Django
"""

import requests
import json

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def create_user_via_admin():
    """
    Verificar si podemos crear un usuario mediante el panel de admin
    """
    print("🔧 Intentando crear usuario mediante Django admin...")
    
    # Verificar que el admin esté accesible
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=10)
        if response.status_code == 200:
            print("✅ Panel de admin accesible")
            
            # El admin está accesible, pero necesitamos credenciales
            print("💡 Para crear un usuario manualmente:")
            print(f"   1. Ve a: {BASE_URL}/admin/")
            print("   2. Inicia sesión con credenciales de superusuario")
            print("   3. Ve a Administration > Users")
            print("   4. Crea un nuevo usuario con:")
            print("      - Email: admin@smartcondo.com")
            print("      - Password: admin123")
            print("      - First name: Admin")
            print("      - Last name: Test")
            
        else:
            print(f"❌ Admin no accesible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accediendo admin: {e}")

def test_with_common_credentials():
    """
    Probar con credenciales comunes que podrían existir
    """
    print("\n🔍 Probando credenciales comunes...")
    
    common_creds = [
        {"email": "admin@admin.com", "password": "admin"},
        {"email": "admin@smartcondo.com", "password": "admin123"},
        {"email": "test@test.com", "password": "test123"},
        {"email": "user@example.com", "password": "password"},
    ]
    
    for creds in common_creds:
        try:
            response = requests.post(
                f"{BASE_URL}/api/token/",
                json=creds,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"   {creds['email']}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                data = response.json()
                print(f"   Access Token: {data.get('access', 'N/A')[:50]}...")
                return creds
            elif response.status_code == 401:
                print(f"   ⚠️ Credenciales incorrectas (pero endpoint funciona)")
            elif response.status_code == 500:
                print(f"   ❌ Error 500 (problema del servidor)")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def verify_database_has_users():
    """
    Verificar indirectamente si hay usuarios en la base de datos
    """
    print("\n🔍 Verificando si hay usuarios en la base de datos...")
    
    try:
        # Los endpoints protegidos nos dan pistas sobre la DB
        response = requests.get(f"{BASE_URL}/api/administration/users/", timeout=10)
        
        if response.status_code == 401:
            print("✅ Endpoint de usuarios existe y requiere autenticación")
            print("✅ Esto indica que la base de datos está funcionando")
        elif response.status_code == 200:
            print("⚠️ Endpoint de usuarios no protegido")
        else:
            print(f"❓ Respuesta inesperada: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 CREACIÓN Y VERIFICACIÓN DE USUARIO")
    print("=" * 50)
    
    create_user_via_admin()
    working_creds = test_with_common_credentials()
    verify_database_has_users()
    
    if working_creds:
        print(f"\n🎉 ¡CREDENCIALES VÁLIDAS PARA POSTMAN!")
        print(f"   Email: {working_creds['email']}")
        print(f"   Password: {working_creds['password']}")
        print(f"   URL: {BASE_URL}/api/token/")
    else:
        print("\n📋 INSTRUCCIONES PARA POSTMAN:")
        print("1. Crear un superusuario manualmente en el admin")
        print("2. O esperar a que se resuelva el error 500")
        print("3. Usar estas credenciales de prueba en Postman:")
        print("   Email: admin@smartcondo.com")
        print("   Password: admin123")
    
    print("=" * 50)