import requests
import json

print("🔍 DEBUGGING API RENDER")
print("=" * 40)

# URL base
base_url = 'https://smart-condominium-backend-fuab.onrender.com'

# Test 1: Root endpoint
print("\n1. Probando endpoint raíz...")
try:
    response = requests.get(base_url, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Admin endpoint
print("\n2. Probando endpoint admin...")
try:
    response = requests.get(f'{base_url}/admin/', timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: API endpoint con user agent
print("\n3. Probando API con headers...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
try:
    response = requests.get(f'{base_url}/api/', headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Verificar si están las variables de entorno
print("\n4. Test endpoint específico...")
try:
    response = requests.get(f'{base_url}/api/administration/roles/', headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 40)
print("Debugging completo")