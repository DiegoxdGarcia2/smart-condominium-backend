#!/usr/bin/env python3
"""
Test simple de endpoints sin autenticación
"""

import requests
import json

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def test_basic_endpoints():
    print("🔍 Probando endpoints básicos...")
    
    endpoints = [
        ("/", "Endpoint raíz"),
        ("/api/", "API principal"),
        ("/admin/", "Panel de administración"),
    ]
    
    for endpoint, desc in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            status_emoji = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status_emoji} {desc} ({endpoint}): {response.status_code}")
        except Exception as e:
            print(f"   ❌ {desc} ({endpoint}): Error - {e}")

def test_token_endpoint_structure():
    print("\n🔍 Probando estructura del endpoint de token...")
    
    # Test 1: Sin datos (debe dar 400 con mensaje claro)
    try:
        response = requests.post(f"{BASE_URL}/api/token/", timeout=10)
        print(f"   POST sin datos: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Correctamente requiere datos")
        else:
            print(f"   ⚠️ Status inesperado, respuesta: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Método GET (debe dar 405)
    try:
        response = requests.get(f"{BASE_URL}/api/token/", timeout=10)
        print(f"   GET method: {response.status_code}")
        if response.status_code == 405:
            print("   ✅ Correctamente rechaza GET")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Test básico de funcionamiento")
    print("=" * 40)
    
    test_basic_endpoints()
    test_token_endpoint_structure()
    
    print("\n✅ Test completado")
    print("Si estos endpoints funcionan, el backend está bien desplegado")
    print("El siguiente paso sería crear un usuario y probar autenticación")