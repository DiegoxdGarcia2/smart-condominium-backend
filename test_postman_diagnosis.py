#!/usr/bin/env python3
"""
Diagnóstico específico para replicar el error 500 de Postman
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def test_postman_scenarios():
    """Replicar diferentes escenarios de Postman"""
    print("🔍 DIAGNÓSTICO DE ERROR 500 - Replicando Postman")
    print("=" * 60)
    
    # Test 1: GET al endpoint raíz (como en Postman)
    print("\n1️⃣ GET a la raíz del servidor:")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"   URL: {BASE_URL}")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        if response.status_code != 200:
            print(f"   Respuesta: {response.text[:500]}")
        else:
            print("   ✅ GET raíz funciona correctamente")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: GET con diferentes headers (como Postman)
    print("\n2️⃣ GET con headers de Postman:")
    try:
        headers = {
            'User-Agent': 'PostmanRuntime/7.32.3',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Respuesta: {response.text[:500]}")
        else:
            print("   ✅ GET con headers Postman funciona")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: POST al endpoint de token (común en Postman)
    print("\n3️⃣ POST al endpoint de token:")
    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.32.3'
        }
        data = {
            "email": "test@example.com",
            "password": "testpass"
        }
        response = requests.post(f"{BASE_URL}/api/token/", 
                                json=data, 
                                headers=headers, 
                                timeout=10)
        print(f"   URL: {BASE_URL}/api/token/")
        print(f"   Status: {response.status_code}")
        print(f"   Data enviada: {data}")
        if response.status_code == 500:
            print(f"   ❌ ERROR 500 - Respuesta: {response.text[:500]}")
        elif response.status_code == 401:
            print("   ✅ 401 - Credenciales incorrectas (normal)")
        elif response.status_code == 400:
            print("   ✅ 400 - Validación de campos (normal)")
            try:
                print(f"   Detalle: {response.json()}")
            except:
                pass
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Diferentes endpoints comunes
    print("\n4️⃣ Probando endpoints comunes:")
    endpoints = [
        "/api/",
        "/admin/",
        "/api/administration/",
        "/api/administration/users/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            status_emoji = "✅" if response.status_code < 500 else "❌"
            print(f"   {status_emoji} {endpoint}: {response.status_code}")
            if response.status_code == 500:
                print(f"      Error 500 detectado en: {endpoint}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")

def test_authentication_flow():
    """Test completo del flujo de autenticación"""
    print("\n5️⃣ Flujo completo de autenticación:")
    
    # Paso 1: Verificar estructura del endpoint
    try:
        response = requests.post(f"{BASE_URL}/api/token/", timeout=10)
        print(f"   POST sin datos: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Campos requeridos: {list(data.keys())}")
        elif response.status_code == 500:
            print("   ❌ ERROR 500 en POST sin datos")
            print(f"   Respuesta: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Paso 2: Con datos pero credenciales incorrectas
    try:
        test_data = [
            {"username": "admin", "password": "admin123"},
            {"email": "admin@test.com", "password": "admin123"},
            {"email": "", "password": ""},
        ]
        
        for i, data in enumerate(test_data, 1):
            response = requests.post(f"{BASE_URL}/api/token/", 
                                    json=data, 
                                    headers={'Content-Type': 'application/json'},
                                    timeout=10)
            print(f"   Test {i} - {data}: {response.status_code}")
            if response.status_code == 500:
                print(f"      ❌ ERROR 500 con datos: {data}")
    except Exception as e:
        print(f"   ❌ Error en flujo: {e}")

def check_server_logs():
    """Simular verificación de logs del servidor"""
    print("\n6️⃣ Información del servidor:")
    
    try:
        # Hacer varias peticiones para identificar el patrón
        responses = []
        for i in range(3):
            response = requests.get(f"{BASE_URL}/api/", timeout=10)
            responses.append(response.status_code)
        
        print(f"   Múltiples peticiones GET /api/: {responses}")
        
        # Verificar consistencia
        if all(r == 200 for r in responses):
            print("   ✅ Servidor estable")
        else:
            print("   ⚠️ Respuestas inconsistentes")
    except Exception as e:
        print(f"   ❌ Error verificando estabilidad: {e}")

if __name__ == "__main__":
    print(f"🚀 DIAGNÓSTICO ESPECÍFICO PARA ERROR 500")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Replicando comportamiento de Postman")
    
    test_postman_scenarios()
    test_authentication_flow() 
    check_server_logs()
    
    print("\n" + "=" * 60)
    print("📋 RECOMENDACIONES:")
    print("1. Verifica la URL exacta que usas en Postman")
    print("2. Asegúrate de usar el método HTTP correcto")
    print("3. Revisa los headers que envías")
    print("4. Si es POST, verifica el Content-Type y el body")
    print("=" * 60)