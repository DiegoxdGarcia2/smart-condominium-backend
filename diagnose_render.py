#!/usr/bin/env python3
"""
Script de diagnóstico detallado para el deployment de Render
"""

import requests
import time
import json
from urllib.parse import urljoin

BASE_URL = "https://smart-condominium-backend.onrender.com"

def test_connection_with_details():
    """Probar la conexión con detalles completos"""
    print("🔍 DIAGNÓSTICO DETALLADO DE CONEXIÓN")
    print("="*50)
    
    try:
        print(f"🌐 Probando: {BASE_URL}")
        
        # Incrementar timeout progresivamente
        for timeout in [10, 20, 30]:
            print(f"\n⏱️  Timeout: {timeout}s")
            try:
                response = requests.get(BASE_URL, timeout=timeout)
                print(f"✅ Conexión exitosa!")
                print(f"📊 Status Code: {response.status_code}")
                print(f"📋 Headers: {dict(response.headers)}")
                
                if response.status_code == 404:
                    print("⚠️  Error 404: La aplicación no está configurando las rutas correctamente")
                    print("📝 Content-Type:", response.headers.get('content-type', 'No definido'))
                    print("📄 Content (primeros 500 chars):")
                    print(response.text[:500])
                    
                elif response.status_code == 200:
                    print("✅ ¡Aplicación funcionando correctamente!")
                    
                return response
                
            except requests.exceptions.Timeout:
                print(f"⏱️  Timeout después de {timeout}s")
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"❌ Error de conexión: {str(e)}")
                continue
            except Exception as e:
                print(f"❌ Error inesperado: {str(e)}")
                continue
                
        print("❌ No se pudo establecer conexión con ningún timeout")
        return None
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        return None

def test_specific_endpoints():
    """Probar endpoints específicos que deberían existir"""
    print("\n🎯 PROBANDO ENDPOINTS ESPECÍFICOS")
    print("="*50)
    
    # Endpoints que definitivamente deberían existir según nuestro Django
    endpoints = [
        "/",
        "/admin/",
        "/admin/login/",
        "/api/",
    ]
    
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint)
        print(f"\n📡 Probando: {url}")
        
        try:
            response = requests.get(url, timeout=15)
            print(f"📊 Status: {response.status_code}")
            print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 404:
                print("❌ 404 - Endpoint no encontrado")
            elif response.status_code == 200:
                print("✅ 200 - Endpoint funcionando")
            elif response.status_code in [301, 302]:
                print(f"🔄 {response.status_code} - Redirección")
                print(f"🔗 Location: {response.headers.get('location', 'N/A')}")
            elif response.status_code == 403:
                print("🔒 403 - Forbidden (puede ser normal)")
            else:
                print(f"⚠️  {response.status_code} - Revisar")
                
        except requests.exceptions.Timeout:
            print("⏱️  Timeout - Servicio muy lento")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def check_render_service_status():
    """Verificar si el servicio está activo en Render"""
    print("\n🔧 VERIFICANDO ESTADO DEL SERVICIO")
    print("="*50)
    
    # Intentar obtener información del servidor
    try:
        response = requests.get(BASE_URL, timeout=20)
        
        # Analizar headers para información del servidor
        server = response.headers.get('server', 'No definido')
        print(f"🖥️  Servidor: {server}")
        
        # Verificar si hay headers de Render/CloudFlare
        cf_ray = response.headers.get('cf-ray', 'No presente')
        print(f"☁️  CloudFlare Ray: {cf_ray}")
        
        # Verificar content-type
        content_type = response.headers.get('content-type', 'No definido')
        print(f"📄 Content-Type: {content_type}")
        
        # Si obtenemos HTML, verificar si es página de error de Django
        if 'text/html' in content_type and response.status_code == 404:
            if 'Django' in response.text:
                print("🐍 Django está sirviendo la respuesta 404")
                print("✅ La aplicación Django está funcionando!")
                print("⚠️  Pero las rutas URL no están configuradas correctamente")
            else:
                print("❌ No parece ser Django sirviendo la respuesta")
                
        return response
        
    except Exception as e:
        print(f"❌ No se pudo verificar estado: {str(e)}")
        return None

def diagnose_routing_issue():
    """Diagnosticar problemas de enrutamiento"""
    print("\n🛣️  DIAGNÓSTICO DE RUTAS")
    print("="*50)
    
    # Verificar si las URLs están en nuestro urls.py
    print("📝 Verificando configuración de URLs...")
    
    # Leer archivo urls.py principal
    try:
        with open("smartcondo_backend/urls.py", "r") as f:
            urls_content = f.read()
            print("✅ URLs principales encontradas:")
            if "admin/" in urls_content:
                print("  ✅ admin/ configurado")
            if "api/" in urls_content:
                print("  ✅ api/ configurado")
            else:
                print("  ❌ api/ NO configurado")
                
    except Exception as e:
        print(f"❌ No se pudo leer urls.py: {str(e)}")

def main():
    """Función principal de diagnóstico"""
    print("🚀 DIAGNÓSTICO COMPLETO DE RENDER DEPLOYMENT")
    print(f"🕐 {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Test 1: Conexión básica
    response = test_connection_with_details()
    
    # Test 2: Endpoints específicos  
    test_specific_endpoints()
    
    # Test 3: Estado del servicio
    check_render_service_status()
    
    # Test 4: Diagnóstico de rutas
    diagnose_routing_issue()
    
    print("\n" + "="*60)
    print("🏁 RESUMEN DEL DIAGNÓSTICO")
    print("="*60)
    
    if response:
        if response.status_code == 404:
            print("🔍 PROBLEMA IDENTIFICADO:")
            print("   La aplicación Django está funcionando en Render")
            print("   PERO las rutas URL no están configuradas correctamente")
            print("")
            print("🔧 SOLUCIONES POSIBLES:")
            print("   1. Verificar que urls.py incluya todas las rutas necesarias")
            print("   2. Verificar que DEBUG=False no esté ocultando errores")
            print("   3. Verificar configuración de ALLOWED_HOSTS")
            print("   4. Revisar los logs de Render para más detalles")
        elif response.status_code == 200:
            print("✅ ¡Todo funcionando correctamente!")
        else:
            print(f"⚠️  Status {response.status_code} - Requiere investigación")
    else:
        print("❌ No se pudo conectar al servicio")
        print("🔧 Verificar que el servicio esté ejecutándose en Render")

if __name__ == "__main__":
    main()