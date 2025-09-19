#!/usr/bin/env python3
"""
Script para monitorear el estado del deployment de Render
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "https://smart-condominium-backend.onrender.com"

def check_deployment_progress():
    """Verificar el progreso del deployment"""
    print("🔄 MONITOREANDO DEPLOYMENT DE RENDER")
    print("="*50)
    
    max_attempts = 10
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n📊 Intento {attempt}/{max_attempts} - {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # Probar endpoint raíz
            response = requests.get(BASE_URL + "/", timeout=15)
            status = response.status_code
            
            print(f"📡 Status Code: {status}")
            
            if status == 200:
                try:
                    data = response.json()
                    print("✅ ¡API funcionando correctamente!")
                    print(f"📝 Mensaje: {data.get('message', 'N/A')}")
                    print(f"🔗 Endpoints disponibles: {data.get('endpoints', {})}")
                    return True
                except:
                    print("✅ Endpoint respondiendo pero no es JSON")
                    print(f"📄 Contenido: {response.text[:100]}...")
                    
            elif status == 404:
                print("⚠️  404 - Deployment aún no actualizado")
                
            elif status >= 500:
                print(f"❌ Error del servidor: {status}")
                print("🔧 Posible problema en el deployment")
                
            else:
                print(f"📊 Status inesperado: {status}")
            
            # Probar admin (que sabemos que funciona)
            admin_response = requests.get(BASE_URL + "/admin/", timeout=10)
            print(f"🔧 Admin status: {admin_response.status_code}")
            
            # Si el admin funciona pero la raíz no, el deployment está activo pero no actualizado
            if admin_response.status_code == 200 and status == 404:
                print("🔄 Deployment activo pero código no actualizado")
                
        except requests.exceptions.Timeout:
            print("⏱️  Timeout - Servidor lento o deployment en progreso")
            
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión - Servidor posiblemente reiniciando")
            
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
        
        if attempt < max_attempts:
            print("⏳ Esperando 30 segundos...")
            time.sleep(30)
            
        attempt += 1
    
    print("\n❌ Deployment no completado después de esperar")
    return False

def test_specific_endpoints_after_deployment():
    """Probar endpoints específicos después del deployment"""
    print("\n🎯 PROBANDO ENDPOINTS DESPUÉS DEL DEPLOYMENT")
    print("="*50)
    
    endpoints_to_test = [
        ("/", "API Status"),
        ("/api/", "API Root"),
        ("/admin/", "Django Admin"),
        ("/api/administration/", "Administration API"),
        ("/api/administration/users/", "Users API"),
        ("/api/administration/financial-fees/", "Financial Fees API"),
        ("/api/administration/initiate-payment/", "Stripe Payment Initiation"),
        ("/api/administration/payment-webhook/", "Stripe Webhook"),
    ]
    
    results = []
    
    for endpoint, description in endpoints_to_test:
        try:
            url = BASE_URL + endpoint
            print(f"\n📡 {description}: {endpoint}")
            
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"    ✅ {status} - OK")
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        data = response.json()
                        if isinstance(data, list):
                            print(f"    📊 Datos: {len(data)} elementos")
                        elif isinstance(data, dict):
                            print(f"    📊 Respuesta: {list(data.keys())}")
                except:
                    pass
                    
            elif status == 401:
                print(f"    🔒 {status} - Autenticación requerida (OK)")
                
            elif status == 403:
                print(f"    🚫 {status} - Sin permisos (OK)")
                
            elif status == 404:
                print(f"    ❌ {status} - No encontrado")
                
            elif status >= 500:
                print(f"    💥 {status} - Error del servidor")
                
            else:
                print(f"    ⚠️  {status} - Verificar")
                
            results.append((endpoint, status, description))
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results.append((endpoint, "Error", str(e)))
    
    return results

def main():
    """Función principal"""
    print(f"🚀 MONITOR DE DEPLOYMENT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    print("="*60)
    
    # Monitorear deployment
    deployment_success = check_deployment_progress()
    
    if deployment_success:
        # Si el deployment fue exitoso, probar todos los endpoints
        results = test_specific_endpoints_after_deployment()
        
        print("\n📋 RESUMEN FINAL")
        print("="*50)
        success_count = sum(1 for _, status, _ in results if status in [200, 401, 403])
        total_count = len(results)
        
        print(f"✅ Endpoints funcionando: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("🎉 ¡DEPLOYMENT 100% EXITOSO!")
        elif success_count > total_count * 0.7:
            print("🔶 Deployment mayormente exitoso, algunos endpoints requieren revisión")
        else:
            print("🔴 Deployment con problemas significativos")
    else:
        print("\n🔴 DEPLOYMENT NO COMPLETADO")
        print("Posibles causas:")
        print("1. Error en el código que impide el startup")
        print("2. Variables de entorno mal configuradas")
        print("3. Problemas con dependencias")
        print("4. Timeout en el proceso de build")
        
    print(f"\n📝 Verificar en Render Dashboard:")
    print("   - Logs del deployment")
    print("   - Variables de entorno")
    print("   - Estado del servicio")

if __name__ == "__main__":
    main()