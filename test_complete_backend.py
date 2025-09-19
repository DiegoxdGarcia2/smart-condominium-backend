#!/usr/bin/env python3
"""
Prueba completa del backend Smart Condominium
Valida todos los endpoints y funcionalidades principales
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def print_section(title):
    print(f"\n📋 {title}")
    print('-'*40)

def test_basic_connectivity():
    """Prueba conectividad básica"""
    print_section("Conectividad Básica")
    
    endpoints = [
        ("/", "Página de inicio"),
        ("/api/", "API raíz"),
        ("/admin/", "Panel de administración"),
    ]
    
    all_ok = True
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {description} ({endpoint}): OK")
            else:
                print(f"   ❌ {description} ({endpoint}): {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"   ❌ {description} ({endpoint}): Error - {e}")
            all_ok = False
    
    return all_ok

def test_authentication_endpoints():
    """Prueba endpoints de autenticación"""
    print_section("Endpoints de Autenticación")
    
    # Test 1: Token endpoint structure
    try:
        # POST sin datos (debe dar 400)
        response = requests.post(f"{BASE_URL}/api/token/", timeout=10)
        if response.status_code == 400:
            print("   ✅ POST /api/token/ sin datos: 400 (correcto)")
            try:
                data = response.json()
                if 'email' in data or 'username' in data:
                    print("   ✅ Respuesta incluye campos requeridos")
            except:
                pass
        else:
            print(f"   ❌ POST /api/token/ sin datos: {response.status_code} (esperado 400)")
        
        # GET (debe dar 405)
        response = requests.get(f"{BASE_URL}/api/token/", timeout=10)
        if response.status_code == 405:
            print("   ✅ GET /api/token/: 405 (correcto)")
        else:
            print(f"   ❌ GET /api/token/: {response.status_code} (esperado 405)")
            
    except Exception as e:
        print(f"   ❌ Error probando token endpoints: {e}")
        return False
    
    # Test 2: Token refresh endpoint
    try:
        response = requests.post(f"{BASE_URL}/api/token/refresh/", timeout=10)
        if response.status_code in [400, 401]:
            print("   ✅ POST /api/token/refresh/ sin datos: correcto")
        else:
            print(f"   ⚠️ POST /api/token/refresh/: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error probando refresh endpoint: {e}")
    
    return True

def test_api_endpoints_without_auth():
    """Prueba endpoints de API sin autenticación (deben requerir auth)"""
    print_section("Endpoints de API (sin autenticación)")
    
    api_endpoints = [
        "/api/users/",
        "/api/roles/",
        "/api/residential-units/",
        "/api/announcements/",
        "/api/financial-fees/",
        "/api/common-areas/",
        "/api/reservations/",
        "/api/vehicles/",
        "/api/pets/",
        "/api/visitor-logs/",
        "/api/tasks/",
        "/api/feedback/",
        "/api/payment-transactions/",
    ]
    
    protected_endpoints = 0
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 401:
                print(f"   ✅ {endpoint}: 401 (requiere autenticación)")
                protected_endpoints += 1
            elif response.status_code == 200:
                print(f"   ⚠️ {endpoint}: 200 (sin autenticación requerida)")
            else:
                print(f"   ❓ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    print(f"\n   📊 {protected_endpoints}/{len(api_endpoints)} endpoints protegidos")
    return protected_endpoints > 0

def test_cors_headers():
    """Prueba configuración CORS"""
    print_section("Configuración CORS")
    
    try:
        # Hacer una petición OPTIONS para verificar CORS
        response = requests.options(f"{BASE_URL}/api/", timeout=10)
        headers = response.headers
        
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
        ]
        
        cors_ok = True
        for header in cors_headers:
            if header in headers:
                print(f"   ✅ {header}: {headers[header]}")
            else:
                print(f"   ❌ {header}: No encontrado")
                cors_ok = False
        
        return cors_ok
        
    except Exception as e:
        print(f"   ❌ Error probando CORS: {e}")
        return False

def test_database_connectivity():
    """Prueba conectividad con base de datos"""
    print_section("Conectividad de Base de Datos")
    
    try:
        # El admin panel es una buena forma de verificar DB
        response = requests.get(f"{BASE_URL}/admin/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Panel de administración accesible")
            
            # Verificar que la respuesta contiene contenido Django admin
            if "Django administration" in response.text or "Django" in response.text:
                print("   ✅ Base de datos conectada (Django admin carga)")
                return True
            else:
                print("   ⚠️ Admin panel responde pero contenido inesperado")
                return False
        else:
            print(f"   ❌ Admin panel: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error probando base de datos: {e}")
        return False

def test_production_settings():
    """Verificar configuraciones de producción"""
    print_section("Configuraciones de Producción")
    
    # Verificar que no está en modo DEBUG
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        
        # En modo DEBUG, Django suele mostrar más información en errores
        # También podemos verificar headers de seguridad
        headers = response.headers
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
        ]
        
        for header in security_headers:
            if header in headers:
                print(f"   ✅ {header}: {headers[header]}")
            else:
                print(f"   ⚠️ {header}: No encontrado")
        
        # Verificar que no hay información de debug en respuesta
        if "DEBUG" not in response.text.upper():
            print("   ✅ No hay información de DEBUG expuesta")
        else:
            print("   ⚠️ Posible información de DEBUG expuesta")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando configuración: {e}")
        return False

def run_comprehensive_test():
    """Ejecutar todas las pruebas"""
    print_header("PRUEBA COMPLETA DEL BACKEND")
    print(f"🕐 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: {BASE_URL}")
    
    results = {
        "conectividad": test_basic_connectivity(),
        "autenticacion": test_authentication_endpoints(),
        "endpoints_api": test_api_endpoints_without_auth(),
        "cors": test_cors_headers(),
        "base_datos": test_database_connectivity(),
        "produccion": test_production_settings(),
    }
    
    print_header("RESUMEN DE RESULTADOS")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name.replace('_', ' ').title()}")
        if result:
            passed += 1
    
    print(f"\n📊 PUNTUACIÓN TOTAL: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ¡BACKEND FUNCIONANDO AL 100%!")
        print("✅ Listo para integración con frontend")
    elif passed >= total * 0.8:
        print("\n👍 Backend funcionando bien con issues menores")
        print("⚠️ Revisar tests fallidos antes de producción")
    else:
        print("\n⚠️ Backend necesita atención")
        print("❌ Resolver issues críticos antes de continuar")
    
    return passed, total

if __name__ == "__main__":
    passed, total = run_comprehensive_test()
    
    print(f"\n{'='*60}")
    print("🏁 PRUEBA COMPLETADA")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)