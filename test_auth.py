#!/usr/bin/env python3
import requests
import json

def test_authentication():
    """Probar la autenticación JWT con el usuario creado"""
    
    # URL del endpoint de autenticación
    url = "http://127.0.0.1:8000/api/token/"
    
    # Datos de prueba
    test_data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    
    print("🔑 Probando autenticación JWT...")
    print(f"URL: {url}")
    print(f"Datos: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        # Hacer la petición POST
        response = requests.post(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ ¡Autenticación exitosa!")
            print(f"Access Token: {token_data.get('access', 'N/A')[:50]}...")
            print(f"Refresh Token: {token_data.get('refresh', 'N/A')[:50]}...")
            return True
        else:
            print("❌ Error en autenticación")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("¿Está corriendo el servidor en http://127.0.0.1:8000?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_with_username():
    """Probar también con username en lugar de email"""
    
    url = "http://127.0.0.1:8000/api/token/"
    
    test_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("\n🔑 Probando autenticación con username...")
    print(f"Datos: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ ¡Autenticación con username exitosa!")
            print(f"Access Token: {token_data.get('access', 'N/A')[:50]}...")
            return True
        else:
            print("❌ Error en autenticación con username")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTING JWT AUTHENTICATION")
    print("=" * 60)
    
    # Probar con email
    email_success = test_authentication()
    
    # Probar con username
    username_success = test_with_username()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Autenticación con email: {'✅ EXITOSA' if email_success else '❌ FALLÓ'}")
    print(f"Autenticación con username: {'✅ EXITOSA' if username_success else '❌ FALLÓ'}")
    
    if email_success or username_success:
        print("\n🎉 ¡Al menos una forma de autenticación funciona!")
        print("🚀 Listo para deploy en Render")
    else:
        print("\n⚠️  Ninguna forma de autenticación funciona")
        print("🔧 Necesita más diagnóstico")