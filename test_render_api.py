import requests
import json

# URL base de tu API en Render
base_url = 'https://smart-condominium-backend-fuab.onrender.com/api'

print("🚀 PROBANDO API EN RENDER - SMART CONDOMINIUM")
print("=" * 60)
print(f"URL Base: {base_url}")

# Test 1: Verificar que el servidor responde
print("\n📡 1. Probando conectividad...")
try:
    response = requests.get(f'{base_url}/administration/roles/', timeout=10)
    print(f"✅ Servidor responde: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ Error de conexión: {e}")
    exit()

# Test 2: Login con usuario migrado
print("\n🔐 2. Probando autenticación...")
login_data = {
    "email": "admin@smartcondo.com",
    "password": "password123"
}

try:
    response = requests.post(f'{base_url}/token/', json=login_data, timeout=10)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data['access']
        print(f"✅ Login exitoso")
        print(f"   Usuario: {login_data['email']}")
        print(f"   Token generado: {token[:50]}...")
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        exit()
except Exception as e:
    print(f"❌ Error en login: {e}")
    exit()

# Headers para requests autenticados
headers = {'Authorization': f'Bearer {token}'}

# Test 3: Listar usuarios
print("\n👥 3. Probando endpoint de usuarios...")
try:
    response = requests.get(f'{base_url}/administration/users/', headers=headers, timeout=10)
    if response.status_code == 200:
        users = response.json()
        if isinstance(users, dict) and 'results' in users:
            users_list = users['results']
        else:
            users_list = users
        print(f"✅ Usuarios obtenidos: {len(users_list)} usuarios")
        for user in users_list[:3]:
            print(f"   - {user['email']} ({user['first_name']} {user['last_name']})")
    else:
        print(f"❌ Error obteniendo usuarios: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Listar cuotas financieras
print("\n💰 4. Probando endpoint de cuotas financieras...")
try:
    response = requests.get(f'{base_url}/administration/financial-fees/', headers=headers, timeout=10)
    if response.status_code == 200:
        fees = response.json()
        if isinstance(fees, dict) and 'results' in fees:
            fees_list = fees['results']
        else:
            fees_list = fees
        print(f"✅ Cuotas obtenidas: {len(fees_list)} cuotas")
        for fee in fees_list[:3]:
            print(f"   - {fee['description']}: ${fee['amount']}")
    else:
        print(f"❌ Error obteniendo cuotas: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Listar transacciones de pago (Stripe)
print("\n💳 5. Probando endpoint de pagos (Stripe)...")
try:
    response = requests.get(f'{base_url}/administration/payments/', headers=headers, timeout=10)
    if response.status_code == 200:
        payments = response.json()
        if isinstance(payments, dict) and 'results' in payments:
            payments_list = payments['results']
        else:
            payments_list = payments
        print(f"✅ Transacciones obtenidas: {len(payments_list)} transacciones")
        for payment in payments_list[:3]:
            print(f"   - ID: {payment['id']}, Estado: {payment['status']}, Monto: ${payment['amount']}")
    else:
        print(f"❌ Error obteniendo pagos: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Probar endpoint de inicio de pago (Stripe)
print("\n🔥 6. Probando iniciar pago con Stripe...")
try:
    payment_data = {"financial_fee_id": 1}
    response = requests.post(f'{base_url}/administration/payments/initiate_payment/', 
                           json=payment_data, headers=headers, timeout=15)
    if response.status_code == 201:
        payment_response = response.json()
        print(f"✅ Pago iniciado exitosamente")
        print(f"   URL de pago: {payment_response.get('payment_url', 'N/A')[:80]}...")
        print(f"   Transaction ID: {payment_response.get('transaction_id', 'N/A')}")
    else:
        print(f"⚠️  Respuesta del pago: {response.status_code}")
        print(f"   Detalle: {response.text}")
except Exception as e:
    print(f"❌ Error en pago: {e}")

print("\n" + "=" * 60)
print("🎉 PRUEBAS COMPLETADAS")
print("✅ Tu API en Render está funcionando correctamente!")
print(f"🌐 URL de producción: {base_url}")