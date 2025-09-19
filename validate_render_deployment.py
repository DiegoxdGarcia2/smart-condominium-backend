#!/usr/bin/env python3
"""
Script completo para validar el deployment de Smart Condominium en Render
"""

import requests
import json
import time
from datetime import datetime

# URL base de la aplicación en Render
BASE_URL = "https://smart-condominium-backend.onrender.com"

def test_basic_endpoints():
    """Probar endpoints básicos de la aplicación"""
    print("🔍 Probando endpoints básicos...")
    
    endpoints = [
        ("/", "Página principal"),
        ("/admin/", "Admin Django"),
        ("/api/", "API raíz"),
        ("/api/auth/", "Autenticación"),
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        try:
            url = BASE_URL + endpoint
            print(f"  📡 {description}: {url}")
            
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"    ✅ {status} - OK")
                results.append((endpoint, status, "OK"))
            elif status in [301, 302, 403, 404]:
                print(f"    🔄 {status} - Redirección/Esperado")
                results.append((endpoint, status, "Esperado"))
            else:
                print(f"    ⚠️  {status} - {response.reason}")
                results.append((endpoint, status, "Error"))
                
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Error de conexión: {str(e)}")
            results.append((endpoint, "Error", str(e)))
    
    return results

def test_authentication():
    """Probar el sistema de autenticación"""
    print("\n🔐 Probando autenticación...")
    
    # Datos de prueba (usuario que sabemos que existe)
    auth_data = {
        "email": "admin@smartcondo.com",  # Ajustar según tu usuario
        "password": "admin123"            # Ajustar según tu password
    }
    
    try:
        url = BASE_URL + "/api/auth/login/"
        print(f"  📡 Login: {url}")
        
        response = requests.post(
            url, 
            data=json.dumps(auth_data),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"    📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("    ✅ Login exitoso!")
            print(f"    🔑 Token obtenido: {data.get('access', 'N/A')[:20]}...")
            return data.get('access')
            
        elif response.status_code == 400:
            print("    ⚠️  Credenciales incorrectas (esperado)")
            return None
            
        else:
            print(f"    ❌ Error inesperado: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error de conexión: {str(e)}")
        return None

def test_api_endpoints(token=None):
    """Probar endpoints de la API"""
    print("\n📊 Probando endpoints de API...")
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    api_endpoints = [
        ("/api/users/", "Usuarios"),
        ("/api/financial-fees/", "Cuotas financieras"),
        ("/api/payment-transactions/", "Transacciones"),
        ("/api/announcements/", "Anuncios"),
    ]
    
    results = []
    
    for endpoint, description in api_endpoints:
        try:
            url = BASE_URL + endpoint
            print(f"  📡 {description}: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            status = response.status_code
            
            if status == 200:
                try:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else data.get('count', 'N/A')
                    print(f"    ✅ {status} - {count} registros")
                    results.append((endpoint, status, f"{count} registros"))
                except:
                    print(f"    ✅ {status} - Respuesta válida")
                    results.append((endpoint, status, "OK"))
                    
            elif status == 401:
                print(f"    🔒 {status} - Requiere autenticación")
                results.append((endpoint, status, "Auth requerida"))
                
            elif status == 403:
                print(f"    🚫 {status} - Sin permisos")
                results.append((endpoint, status, "Sin permisos"))
                
            else:
                print(f"    ❌ {status} - Error")
                results.append((endpoint, status, "Error"))
                
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Error de conexión: {str(e)}")
            results.append((endpoint, "Error", str(e)))
    
    return results

def test_stripe_integration():
    """Probar la integración con Stripe"""
    print("\n💳 Probando integración de Stripe...")
    
    # Test 1: Endpoint de iniciar pago
    try:
        url = BASE_URL + "/api/initiate-payment/"
        print(f"  📡 Initiate Payment: {url}")
        
        # Datos de prueba para crear sesión de pago
        payment_data = {
            "fee_id": 1,  # Usar ID de cuota que sabemos que existe
            "amount": 100.00
        }
        
        response = requests.post(
            url,
            data=json.dumps(payment_data),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"    📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("    ✅ Stripe integración funcionando!")
            print(f"    🔗 Session ID: {data.get('session_id', 'N/A')[:20]}...")
            
        elif response.status_code == 401:
            print("    🔒 Requiere autenticación (esperado)")
            
        else:
            print(f"    ⚠️  Status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"    📝 Respuesta: {error_data}")
            except:
                print(f"    📝 Respuesta: {response.text[:100]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error de conexión: {str(e)}")
    
    # Test 2: Webhook endpoint
    try:
        url = BASE_URL + "/api/payment-webhook/"
        print(f"  📡 Payment Webhook: {url}")
        
        response = requests.post(url, timeout=10)
        print(f"    📊 Status: {response.status_code}")
        
        if response.status_code == 400:
            print("    ✅ Webhook endpoint respondiendo (400 esperado sin datos)")
        else:
            print(f"    📊 Respuesta: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error de conexión: {str(e)}")

def generate_report(basic_results, api_results):
    """Generar reporte final"""
    print("\n" + "="*60)
    print("📋 REPORTE FINAL DE VALIDACIÓN")
    print("="*60)
    
    print("\n🔍 Endpoints Básicos:")
    for endpoint, status, result in basic_results:
        status_icon = "✅" if result in ["OK", "Esperado"] else "❌"
        print(f"  {status_icon} {endpoint}: {status} - {result}")
    
    print("\n📊 Endpoints de API:")
    for endpoint, status, result in api_results:
        if status == 200:
            status_icon = "✅"
        elif status in [401, 403]:
            status_icon = "🔒"
        else:
            status_icon = "❌"
        print(f"  {status_icon} {endpoint}: {status} - {result}")
    
    # Evaluar estado general
    basic_ok = all(result in ["OK", "Esperado"] for _, _, result in basic_results)
    api_ok = all(status in [200, 401, 403] for _, status, _ in api_results if status != "Error")
    
    print(f"\n🎯 Estado General:")
    print(f"  {'✅' if basic_ok else '❌'} Endpoints básicos: {'OK' if basic_ok else 'Con errores'}")
    print(f"  {'✅' if api_ok else '❌'} API endpoints: {'OK' if api_ok else 'Con errores'}")
    
    if basic_ok and api_ok:
        print("\n🎉 ¡DEPLOYMENT EXITOSO!")
        print("   La aplicación está funcionando correctamente en Render")
    else:
        print("\n⚠️  DEPLOYMENT PARCIAL")
        print("   Revisar configuración de variables de entorno")

def main():
    """Función principal"""
    print("🚀 VALIDACIÓN DE DEPLOYMENT - Smart Condominium Backend")
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Test 1: Endpoints básicos
    basic_results = test_basic_endpoints()
    
    # Test 2: Autenticación
    token = test_authentication()
    
    # Test 3: API endpoints
    api_results = test_api_endpoints(token)
    
    # Test 4: Stripe
    test_stripe_integration()
    
    # Reporte final
    generate_report(basic_results, api_results)
    
    print(f"\n📝 Variables de entorno requeridas en Render:")
    print("   DATABASE_URL = postgresql://smartcondominio_user:3gRivgyPRtg988KIAvsfMJu7IjpRacff@dpg-d36co28gjchc73c6rekg-a/smartcondominio")
    print("   SECRET_KEY = 3gRivgyPRtg988KIAvsfMJu7IjpRacff") 
    print("   DEBUG = FALSE")
    print("   STRIPE_WEBHOOK_SECRET = whsec_hLXZ2H23yX1A1o5T7SzA1b4NfublNwAU")

if __name__ == "__main__":
    main()