import requests
import json

base_url = 'http://127.0.0.1:8000/api'

# Login como administrador
print("🔑 Iniciando login...")
response = requests.post(f'{base_url}/token/', json={'email': 'admin@smartcondo.com', 'password': 'password123'})
if response.status_code != 200:
    print(f'❌ Error en login: {response.status_code}')
    exit()

token = response.json()['access']
headers = {'Authorization': f'Bearer {token}'}
print("✅ Login exitoso")

# Llamar al endpoint de feedback para ver la estructura exacta
print("\n📋 Consultando endpoint de feedback...")
response = requests.get(f'{base_url}/administration/feedback/', headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Headers de respuesta: {dict(response.headers)}")

if response.status_code == 200:
    data = response.json()
    print(f"Tipo de respuesta: {type(data)}")
    print(f"Estructura de la respuesta:")
    print(json.dumps(data, indent=2)[:500])  # Mostrar solo los primeros 500 caracteres
    
    if isinstance(data, dict):
        print(f"\nClaves del objeto: {list(data.keys())}")
        if 'results' in data:
            print(f"Tipo de 'results': {type(data['results'])}")
            print(f"Número de items en 'results': {len(data['results']) if isinstance(data['results'], list) else 'No es lista'}")
else:
    print(f"Error: {response.text}")