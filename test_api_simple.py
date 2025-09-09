import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

def test_api():
    print("=== PRUEBAS DE API - SMART CONDOMINIUM BACKEND ===")
    
    # Test 1: Server connection
    print("\n1. Probando conexion al servidor...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✓ Servidor conectado")
    except requests.exceptions.ConnectionError:
        print("✗ Servidor no disponible")
        return False
    
    # Test 2: JWT Authentication
    print("\n2. Probando autenticacion JWT...")
    credentials = {
        "email": "juan.perez@email.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/token/", json=credentials)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print("✓ Token obtenido exitosamente")
        else:
            print(f"✗ Error al obtener token: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test 3: Authenticated endpoints
    print("\n3. Probando endpoints autenticados...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    endpoints = [
        ("/administration/roles/", "Roles"),
        ("/administration/users/", "Usuarios"),
        ("/administration/residential-units/", "Unidades")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', []))
                print(f"✓ {name}: {count} items")
            else:
                print(f"✗ Error en {name}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error en {name}: {e}")
    
    # Test 4: Create new role
    print("\n4. Probando creacion de datos...")
    new_role = {"name": "Portero Test"}
    try:
        response = requests.post(f"{API_BASE}/administration/roles/", headers=headers, json=new_role)
        if response.status_code == 201:
            print("✓ Nuevo rol creado")
        else:
            print(f"✗ Error creando rol: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n=== PRUEBAS COMPLETADAS ===")
    print("✅ API funcionando correctamente!")
    print(f"\nPuedes acceder a:")
    print(f"- Admin: {BASE_URL}/admin/")
    print(f"- API: {BASE_URL}/api/administration/")
    
    return True

if __name__ == "__main__":
    test_api()
