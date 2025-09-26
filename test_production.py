#!/usr/bin/env python3
import requests
import json
import time

def test_production_auth():
    """Probar la autenticación JWT en producción"""
    
    # URL de producción en Render
    base_url = "https://smart-condominium-backend-fuab.onrender.com"
    auth_url = f"{base_url}/api/token/"
    
    # Datos de prueba
    test_data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    
    print("🌍 PROBANDO AUTENTICACIÓN EN PRODUCCIÓN")
    print("=" * 60)
    print(f"🔗 URL: {auth_url}")
    print(f"📧 Email: {test_data['email']}")
    print("🔒 Password: [HIDDEN]")
    print("-" * 60)
    
    try:
        print("⏳ Haciendo petición...")
        response = requests.post(
            auth_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30  # Timeout de 30 segundos para Render
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
        print("-" * 60)
        
        if response.status_code == 200:
            token_data = response.json()
            print("🎉 ¡AUTENTICACIÓN EN PRODUCCIÓN EXITOSA!")
            print(f"🔑 Access Token: {token_data.get('access', 'N/A')[:50]}...")
            print(f"🔄 Refresh Token: {token_data.get('refresh', 'N/A')[:50]}...")
            
            # Probar el token en un endpoint protegido
            test_protected_endpoint(base_url, token_data.get('access'))
            
            return True
        else:
            print("❌ ERROR EN AUTENTICACIÓN DE PRODUCCIÓN")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT - El servidor tardó más de 30 segundos en responder")
        print("💡 Esto puede ser normal en cold starts de Render")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 ERROR DE CONEXIÓN")
        print("💡 Verifica que el servicio esté corriendo en Render")
        return False
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return False

def test_protected_endpoint(base_url, access_token):
    """Probar un endpoint protegido con el token"""
    
    print("\n🔒 PROBANDO ENDPOINT PROTEGIDO")
    print("-" * 40)
    
    users_url = f"{base_url}/api/administration/users/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(users_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ Endpoint protegido funciona correctamente")
            print(f"📄 Response: {response.json()}")
        elif response.status_code == 401:
            print("🔒 Token rechazado (401) - Verificar configuración JWT")
        else:
            print(f"⚠️  Status Code: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error probando endpoint protegido: {e}")

def wait_for_deployment():
    """Esperar a que el deployment esté listo"""
    
    base_url = "https://smart-condominium-backend-fuab.onrender.com"
    status_url = f"{base_url}/"
    
    print("⏳ Esperando que el deployment esté listo...")
    print(f"🔗 Verificando: {status_url}")
    
    for attempt in range(5):
        try:
            response = requests.get(status_url, timeout=10)
            if response.status_code == 200:
                print("✅ Servidor disponible!")
                return True
        except:
            pass
        
        print(f"🔄 Intento {attempt + 1}/5 - Esperando...")
        time.sleep(10)
    
    print("⚠️  El servidor no respondió después de varios intentos")
    return False

if __name__ == "__main__":
    print("🚀 TESTING PRODUCCIÓN EN RENDER")
    print("=" * 60)
    
    # Esperar deployment
    if wait_for_deployment():
        # Probar autenticación
        success = test_production_auth()
        
        print("\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        if success:
            print("🎉 ¡ÉXITO TOTAL!")
            print("✅ Autenticación JWT funciona en producción")
            print("✅ El proyecto está listo para usar")
            print("\n🔗 URLs importantes:")
            print("   • API Status: https://smart-condominium-backend-fuab.onrender.com/")
            print("   • Admin: https://smart-condominium-backend-fuab.onrender.com/admin/")
            print("   • Auth: https://smart-condominium-backend-fuab.onrender.com/api/token/")
        else:
            print("❌ Aún hay problemas en producción")
            print("🔧 Revisar logs de Render para más detalles")
    else:
        print("❌ No se pudo conectar al servidor")
        print("💡 Verifica el estado del deployment en Render")