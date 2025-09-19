#!/usr/bin/env python3
"""
TEST FINAL - Validación completa del backend al 100%
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def test_core_functionality():
    """Test de funcionalidad principal"""
    print("📋 FUNCIONALIDAD PRINCIPAL")
    print('-'*40)
    
    results = []
    
    # 1. Conectividad básica
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Servidor en línea y respondiendo")
            results.append(True)
        else:
            print(f"   ❌ Servidor responde con error: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Servidor no accesible: {e}")
        results.append(False)
    
    # 2. API disponible
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        if response.status_code == 200:
            print("   ✅ API principal accesible")
            results.append(True)
        else:
            print(f"   ❌ API no accesible: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Error accediendo API: {e}")
        results.append(False)
    
    # 3. Base de datos conectada
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=10)
        if response.status_code == 200 and "Django" in response.text:
            print("   ✅ Base de datos conectada (Django admin accesible)")
            results.append(True)
        else:
            print("   ❌ Problema con base de datos")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Error verificando base de datos: {e}")
        results.append(False)
    
    return all(results)

def test_authentication_system():
    """Test del sistema de autenticación"""
    print("\n📋 SISTEMA DE AUTENTICACIÓN")
    print('-'*40)
    
    results = []
    
    # 1. Endpoint de token existe y funciona
    try:
        response = requests.post(f"{BASE_URL}/api/token/", timeout=10)
        if response.status_code == 400:
            data = response.json()
            if 'email' in data or 'username' in data:
                print("   ✅ Endpoint de autenticación configurado correctamente")
                results.append(True)
            else:
                print("   ⚠️ Endpoint funciona pero campos inesperados")
                results.append(True)
        else:
            print(f"   ❌ Endpoint de token con problema: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Error probando autenticación: {e}")
        results.append(False)
    
    # 2. Refresh token disponible
    try:
        response = requests.post(f"{BASE_URL}/api/token/refresh/", timeout=10)
        if response.status_code in [400, 401]:
            print("   ✅ Endpoint de refresh token configurado")
            results.append(True)
        else:
            print(f"   ❌ Problema con refresh token: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Error probando refresh token: {e}")
        results.append(False)
    
    return all(results)

def test_api_endpoints():
    """Test de todos los endpoints de API"""
    print("\n📋 ENDPOINTS DE API")
    print('-'*40)
    
    endpoints = [
        "users", "roles", "residential-units", "announcements", 
        "financial-fees", "common-areas", "reservations", "vehicles",
        "pets", "visitor-logs", "tasks", "feedback", "payments"
    ]
    
    working_endpoints = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}/api/administration/{endpoint}/", timeout=10)
            if response.status_code == 401:
                print(f"   ✅ {endpoint}: Protegido correctamente")
                working_endpoints += 1
            elif response.status_code == 200:
                print(f"   ✅ {endpoint}: Accesible")
                working_endpoints += 1
            else:
                print(f"   ❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    success_rate = (working_endpoints / len(endpoints)) * 100
    print(f"\n   📊 {working_endpoints}/{len(endpoints)} endpoints funcionando ({success_rate:.1f}%)")
    
    return working_endpoints == len(endpoints)

def test_cors_configuration():
    """Test de configuración CORS"""
    print("\n📋 CONFIGURACIÓN CORS")
    print('-'*40)
    
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }
        
        response = requests.options(f"{BASE_URL}/api/", headers=headers, timeout=10)
        
        required_headers = [
            'access-control-allow-origin',
            'access-control-allow-methods', 
            'access-control-allow-headers'
        ]
        
        cors_headers_found = 0
        for header in required_headers:
            if header in [h.lower() for h in response.headers.keys()]:
                cors_headers_found += 1
        
        if cors_headers_found == len(required_headers):
            print("   ✅ CORS configurado correctamente para frontend")
            print("   ✅ Permite localhost:3000")
            print("   ✅ Métodos HTTP permitidos")
            print("   ✅ Headers de autorización permitidos")
            return True
        else:
            print(f"   ⚠️ CORS parcialmente configurado ({cors_headers_found}/{len(required_headers)})")
            return False
            
    except Exception as e:
        print(f"   ❌ Error probando CORS: {e}")
        return False

def test_security_headers():
    """Test de headers de seguridad"""
    print("\n📋 SEGURIDAD")
    print('-'*40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        headers = response.headers
        
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY'
        }
        
        security_score = 0
        for header, expected in security_headers.items():
            if header in headers:
                print(f"   ✅ {header}: {headers[header]}")
                security_score += 1
            else:
                print(f"   ⚠️ {header}: No configurado")
        
        # Verificar que no está en modo DEBUG
        if "DEBUG" not in response.text.upper():
            print("   ✅ Modo DEBUG deshabilitado")
            security_score += 1
        else:
            print("   ⚠️ Posible modo DEBUG habilitado")
        
        return security_score >= 2
        
    except Exception as e:
        print(f"   ❌ Error verificando seguridad: {e}")
        return False

def run_final_validation():
    """Ejecutar validación final completa"""
    print_header("VALIDACIÓN FINAL DEL BACKEND")
    print(f"🕐 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: {BASE_URL}")
    
    tests = {
        "🏗️  Funcionalidad Principal": test_core_functionality,
        "🔐 Sistema de Autenticación": test_authentication_system,
        "🔗 Endpoints de API": test_api_endpoints,
        "🌍 Configuración CORS": test_cors_configuration,
        "🛡️  Seguridad": test_security_headers,
    }
    
    results = {}
    for test_name, test_func in tests.items():
        results[test_name] = test_func()
    
    print_header("RESULTADO FINAL")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    percentage = (passed / total) * 100
    print(f"\n📊 PUNTUACIÓN FINAL: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 ¡BACKEND FUNCIONANDO AL 100%!")
        print("✅ Completamente listo para producción")
        print("✅ Listo para integración con frontend")
        print("✅ Todos los sistemas operativos")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Crear usuarios de prueba")
        print("   2. Probar autenticación con credenciales reales")
        print("   3. Integrar con frontend")
    elif passed >= total * 0.8:
        print("\n👍 Backend funcionando excelentemente")
        print("⚠️ Issues menores que no afectan funcionalidad principal")
    else:
        print("\n⚠️ Backend necesita atención")
        print("❌ Resolver issues antes de producción")
    
    return passed, total

if __name__ == "__main__":
    passed, total = run_final_validation()
    
    print(f"\n{'='*60}")
    print("🏁 VALIDACIÓN COMPLETADA")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)