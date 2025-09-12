#!/usr/bin/env python
"""
Script para probar los endpoints de Financial Fees y diagnosticar errores
"""
import requests
import json
from datetime import datetime, timedelta

# Configuración
API_BASE = "http://localhost:8000/api"

# Credenciales de prueba
credentials = {
    "email": "juan.perez@email.com",
    "password": "password123"
}

def get_auth_token():
    """Obtener token de autenticación"""
    response = requests.post(f"{API_BASE}/token/", json=credentials)
    if response.status_code == 200:
        return response.json()['access']
    else:
        print(f"Error al obtener token: {response.status_code}")
        print(response.text)
        return None

def test_financial_fees():
    """Probar los endpoints de cuotas financieras"""
    token = get_auth_token()
    if not token:
        return
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("=== PROBANDO ENDPOINTS DE FINANCIAL FEES ===\n")
    
    # 1. Obtener lista de unidades residenciales
    print("1. Obteniendo unidades residenciales...")
    response = requests.get(f"{API_BASE}/administration/residential-units/", headers=headers)
    if response.status_code == 200:
        units = response.json()['results']
        print(f"✓ {len(units)} unidades encontradas")
        for unit in units:
            print(f"   - ID: {unit['id']}, Number: {unit['unit_number']}, Owner: {unit['owner_name']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return
    
    # 2. Obtener lista actual de cuotas
    print("\n2. Obteniendo cuotas financieras existentes...")
    response = requests.get(f"{API_BASE}/administration/financial-fees/", headers=headers)
    if response.status_code == 200:
        fees = response.json()['results']
        print(f"✓ {len(fees)} cuotas encontradas")
        for fee in fees[:3]:  # Solo mostrar las primeras 3
            print(f"   - ID: {fee['id']}, Unit: {fee['unit_number']}, Amount: ${fee['amount']}, Status: {fee['status']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return
    
    # 3. Probar POST (crear nueva cuota)
    print("\n3. Probando POST - Crear nueva cuota...")
    
    # Probar con diferentes formatos de datos
    test_data_variations = [
        {
            "name": "Formato básico correcto",
            "data": {
                "unit": 1,
                "description": "Cuota de prueba POST",
                "amount": "100.00",
                "due_date": "2025-12-31",
                "status": "Pendiente"
            }
        },
        {
            "name": "Sin status (debería usar default)",
            "data": {
                "unit": 1,
                "description": "Cuota sin status",
                "amount": "150.50",
                "due_date": "2025-12-31"
            }
        },
        {
            "name": "Amount como número",
            "data": {
                "unit": 1,
                "description": "Cuota amount numérico",
                "amount": 200.75,
                "due_date": "2025-12-31",
                "status": "Pendiente"
            }
        }
    ]
    
    for test_case in test_data_variations:
        print(f"\n   Probando: {test_case['name']}")
        print(f"   Datos: {json.dumps(test_case['data'], indent=2)}")
        
        response = requests.post(
            f"{API_BASE}/administration/financial-fees/", 
            json=test_case['data'],
            headers=headers
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 201:
            print("   ✓ Creación exitosa")
            result = response.json()
            print(f"   ID creado: {result['id']}")
        else:
            print("   ✗ Error en creación")
            print(f"   Response: {response.text}")
        print("   " + "-"*50)
    
    # 4. Probar PUT (actualizar cuota existente)
    print("\n4. Probando PUT - Actualizar cuota existente...")
    
    if fees:
        fee_id = fees[0]['id']
        print(f"   Actualizando cuota ID: {fee_id}")
        
        update_data = {
            "unit": fees[0]['unit'],
            "description": "Cuota actualizada via PUT",
            "amount": "999.99",
            "due_date": "2025-12-31",
            "status": "Pagado"
        }
        
        print(f"   Datos: {json.dumps(update_data, indent=2)}")
        
        response = requests.put(
            f"{API_BASE}/administration/financial-fees/{fee_id}/",
            json=update_data,
            headers=headers
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Actualización exitosa")
            result = response.json()
            print(f"   Nueva descripción: {result['description']}")
            print(f"   Nuevo monto: ${result['amount']}")
            print(f"   Nuevo status: {result['status']}")
        else:
            print("   ✗ Error en actualización")
            print(f"   Response: {response.text}")

if __name__ == "__main__":
    test_financial_fees()
