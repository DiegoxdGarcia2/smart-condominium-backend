#!/usr/bin/env python3
"""
Script simple para probar endpoints específicos del deployment
"""

import requests

BASE_URL = "https://smart-condominium-backend.onrender.com"

def test_endpoints():
    """Probar endpoints específicos"""
    print("🧪 PRUEBAS DE ENDPOINTS ESPECÍFICOS")
    print("="*50)
    
    # Endpoints según nuestra configuración de Django
    endpoints = [
        ("/", "Página principal (nueva vista)"),
        ("/api/", "API raíz (nueva vista)"),  
        ("/admin/", "Django Admin"),
        ("/api/administration/", "Administration API"),
        ("/api/administration/users/", "Users API"),
        ("/api/administration/financial-fees/", "Financial Fees API"),
        ("/api/administration/announcements/", "Announcements API"),
        ("/api/administration/initiate-payment/", "Stripe Payment"),
        ("/api/administration/payment-webhook/", "Stripe Webhook"),
        ("/api/token/", "JWT Token"),
    ]
    
    for endpoint, description in endpoints:
        try:
            url = BASE_URL + endpoint
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            print(f"{endpoint:35} -> {status:3} {response.reason}")
            
            # Si es 200 y JSON, mostrar más detalles
            if status == 200 and 'application/json' in response.headers.get('content-type', ''):
                try:
                    data = response.json()
                    if 'message' in data:
                        print(f"{'':35}    💬 {data['message']}")
                    if 'endpoints' in data:
                        print(f"{'':35}    🔗 Endpoints disponibles")
                except:
                    pass
                    
            # Casos especiales
            elif status == 401:
                print(f"{'':35}    🔒 Autenticación requerida (correcto)")
            elif status == 404:
                print(f"{'':35}    ❌ Endpoint no encontrado")
            elif status == 405:
                print(f"{'':35}    ⚠️  Método no permitido")
                
        except Exception as e:
            print(f"{endpoint:35} -> ❌ ERROR: {str(e)[:40]}")

if __name__ == "__main__":
    test_endpoints()