#!/usr/bin/env python3
"""
Test específico de los endpoints de administración
"""

import requests

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def test_admin_endpoints():
    print("🔍 Probando endpoints de administración específicos...")
    
    # Las rutas están bajo /api/administration/
    endpoints = [
        "/api/administration/users/",
        "/api/administration/roles/", 
        "/api/administration/residential-units/",
        "/api/administration/announcements/",
        "/api/administration/financial-fees/",
        "/api/administration/common-areas/",
        "/api/administration/reservations/",
        "/api/administration/vehicles/",
        "/api/administration/pets/",
        "/api/administration/visitor-logs/",
        "/api/administration/tasks/",
        "/api/administration/feedback/",
        "/api/administration/payments/",
    ]
    
    working_endpoints = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 401:
                print(f"   ✅ {endpoint}: 401 (requiere autenticación)")
                working_endpoints += 1
            elif response.status_code == 200:
                print(f"   ✅ {endpoint}: 200 (accesible)")
                working_endpoints += 1
            elif response.status_code == 404:
                print(f"   ❌ {endpoint}: 404 (no encontrado)")
            else:
                print(f"   ❓ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    print(f"\n📊 {working_endpoints}/{len(endpoints)} endpoints funcionando")
    return working_endpoints > 0

def test_cors_with_origin():
    print("\n🔍 Probando CORS con Origin específico...")
    
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }
        
        response = requests.options(f"{BASE_URL}/api/", headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        cors_headers = response.headers
        for header, value in cors_headers.items():
            if 'access-control' in header.lower():
                print(f"   ✅ {header}: {value}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de endpoints de administración")
    print("=" * 50)
    
    endpoints_ok = test_admin_endpoints()
    cors_ok = test_cors_with_origin()
    
    if endpoints_ok:
        print("\n✅ Los endpoints de administración están funcionando")
    else:
        print("\n❌ Hay problemas con los endpoints")
    
    print("=" * 50)