#!/usr/bin/env python3
"""
Prueba rápida de las correcciones de la Fase 4
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def quick_test():
    print("🔧 PRUEBA RÁPIDA DE CORRECCIONES")
    
    # 1. Autenticación
    login_data = {"email": "juan.perez@email.com", "password": "password123"}
    response = requests.post(f"{API_BASE}/token/", json=login_data)
    
    if response.status_code != 200:
        print("❌ Error en autenticación")
        return
    
    token = response.json()["access"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("✅ Autenticación exitosa")
    
    # 2. Probar creación de vehículo (SIN campo resident)
    vehicle_data = {
        "license_plate": "FIXED-123",
        "brand": "Toyota",
        "model": "Camry", 
        "color": "Azul"
    }
    
    response = requests.post(f"{API_BASE}/administration/vehicles/", json=vehicle_data, headers=headers)
    if response.status_code == 201:
        print("✅ Vehículo creado exitosamente")
        vehicle_id = response.json()["id"]
        
        # Eliminar vehículo de prueba
        requests.delete(f"{API_BASE}/administration/vehicles/{vehicle_id}/", headers=headers)
    else:
        print(f"❌ Error creando vehículo: {response.status_code}")
        print(response.text)
    
    # 3. Probar creación de mascota (SIN campo resident)
    pet_data = {
        "name": "TestPet",
        "species": "Perro",
        "breed": "Mestizo",
        "age": 3
    }
    
    response = requests.post(f"{API_BASE}/administration/pets/", json=pet_data, headers=headers)
    if response.status_code == 201:
        print("✅ Mascota creada exitosamente")
        pet_id = response.json()["id"]
        
        # Eliminar mascota de prueba
        requests.delete(f"{API_BASE}/administration/pets/{pet_id}/", headers=headers)
    else:
        print(f"❌ Error creando mascota: {response.status_code}")
        print(response.text)
    
    # 4. Probar permisos de daily_report como residente
    response = requests.get(f"{API_BASE}/administration/visitor-logs/daily_report/", headers=headers)
    if response.status_code == 403:
        print("✅ Permisos correctos: residente NO puede acceder a daily_report")
    else:
        print(f"❌ Error de permisos: residente puede acceder a daily_report ({response.status_code})")
    
    print("\n🎉 Pruebas de corrección completadas!")

if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")