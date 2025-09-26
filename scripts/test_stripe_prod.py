import requests
import time
import hmac
import hashlib
import json

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"
EMAIL = "admin@test.com"
PASSWORD = "admin123"
FINANCIAL_FEE_ID = 1
STRIPE_WEBHOOK_SECRET = "whsec_hLXZ2H23yX1A1o5T7SzA1b4NfublNwAU"


def pretty(resp):
    try:
        return json.dumps(resp.json(), indent=2, ensure_ascii=False)
    except Exception:
        return resp.text


print("1) Obteniendo JWT (3 reintentos, timeout 30s)...")
access = None
for attempt in range(1, 4):
    try:
        print(f"  intento {attempt}...")
        r = requests.post(f"{BASE_URL}/api/token/", json={"email": EMAIL, "password": PASSWORD}, timeout=30)
        print("  Status:", r.status_code)
        print(pretty(r))
        if r.status_code == 200:
            access = r.json().get('access')
            break
        else:
            print('  Respuesta no OK, reintentando...')
    except Exception as e:
        print('  Error en petición:', e)
    time.sleep(2)

if not access:
    print("No se pudo obtener token después de reintentos; abortando pruebas de pago.")
    raise SystemExit

headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}

print('\n2) Intentando iniciar pago (POST initiate-payment) con financial_fee_id=', FINANCIAL_FEE_ID)
try:
    r = requests.post(f"{BASE_URL}/api/administration/initiate-payment/", json={"financial_fee_id": FINANCIAL_FEE_ID}, headers=headers, timeout=20)
    print("Status:", r.status_code)
    print(pretty(r))
    if r.status_code not in (200,201):
        print("initiate-payment no devolvió sesión/transaction_id. Resultado final de la prueba.")
        raise SystemExit
    data = r.json()
    payment_url = data.get('payment_url')
    transaction_id = data.get('transaction_id')
    print('payment_url:', payment_url)
    print('transaction_id:', transaction_id)
except Exception as e:
    print('Error en initiate-payment:', e)
    raise SystemExit

# Si obtuvimos transaction_id, simulamos webhook
if not transaction_id:
    print('No hay transaction_id, no puedo simular webhook relacionado. Fin.')
    raise SystemExit

print('\n3) Construyendo payload simulando evento checkout.session.completed y firmando con STRIPE_WEBHOOK_SECRET...')
# Construir payload tal como espera el backend
event = {
    'id': 'evt_test_{}'.format(int(time.time())),
    'object': 'event',
    'type': 'checkout.session.completed',
    'data': {
        'object': {
            'id': transaction_id,
            'object': 'checkout.session',
            'payment_status': 'paid',
            'payment_intent': 'pi_test_{}'.format(int(time.time())),
            'amount_total': int(100 * 100),
            'metadata': {
                'financial_fee_id': str(FINANCIAL_FEE_ID),
                'resident_id': '1'
            }
        }
    }
}

payload = json.dumps(event)

ts = str(int(time.time()))
_signed = hmac.new(STRIPE_WEBHOOK_SECRET.encode('utf-8'), msg=f"{ts}.{payload}".encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
sig_header = f"t={ts},v1={_signed}"

print('Stripe-Signature header:', sig_header)

print('\n4) Enviando POST al webhook endpoint...')
try:
    # Añadir Authorization para que la petición de webhook incluya el token JWT
    wh_headers = {"Content-Type": "application/json", "Stripe-Signature": sig_header, "Authorization": f"Bearer {access}"}
    r = requests.post(f"{BASE_URL}/api/administration/payment-webhook/", data=payload.encode('utf-8'), headers=wh_headers, timeout=20)
    print('Status webhook:', r.status_code)
    print(pretty(r))
except Exception as e:
    print('Error enviando webhook:', e)
    raise SystemExit

print('\nPrueba completada.')
