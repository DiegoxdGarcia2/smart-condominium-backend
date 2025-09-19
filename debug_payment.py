import requests
import json

base_url = 'http://127.0.0.1:8000/api'

# Login
print("🔑 Iniciando login...")
response = requests.post(f'{base_url}/token/', json={'email': 'admin@smartcondo.com', 'password': 'password123'})
if response.status_code != 200:
    print(f'❌ Error en login: {response.status_code}')
    print(f'❌ Respuesta: {response.text}')
    exit()

token = response.json()['access']
headers = {'Authorization': f'Bearer {token}'}
print("✅ Login exitoso")

# Listar pagos existentes
print("\n📋 Listando pagos existentes...")
response = requests.get(f'{base_url}/administration/payments/', headers=headers)
if response.status_code == 200:
    payments_data = response.json()
    print(f"Tipo de respuesta: {type(payments_data)}")
    
    if isinstance(payments_data, dict) and 'results' in payments_data:
        payments = payments_data['results']
    elif isinstance(payments_data, list):
        payments = payments_data
    else:
        payments = []
        
    print(f"Número de pagos existentes: {len(payments)}")
    for payment in payments[:3]:  # Solo mostrar los primeros 3
        print(f"- ID: {payment['id']}, Fee: {payment['financial_fee']}, Amount: {payment['amount']}")
else:
    print(f"Error al listar pagos: {response.status_code}")
    print(f"Respuesta: {response.text}")

# Intentar crear pago
print("\n💳 Intentando crear nuevo pago...")
payment_data = {
    'financial_fee_id': 2,  # Cambiar a fee ID 2 para evitar duplicados
    'description': 'Test payment - debug'
}

response = requests.post(f'{base_url}/administration/payments/initiate_payment/', 
                        json=payment_data, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

if response.status_code == 400:
    try:
        error_data = response.json()
        print(f"Error JSON: {json.dumps(error_data, indent=2)}")
    except:
        print("No se pudo parsear como JSON")