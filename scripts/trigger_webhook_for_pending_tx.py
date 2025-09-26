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


print("1) Obtener JWT...")
r = requests.post(f"{BASE_URL}/api/token/", json={"email": EMAIL, "password": PASSWORD}, timeout=15)
print(r.status_code)
print(pretty(r))
if r.status_code != 200:
    raise SystemExit('No token')
access = r.json().get('access')
headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}

print('\n2) Listar transacciones del usuario...')
r = requests.get(f"{BASE_URL}/api/administration/payments/", headers=headers, timeout=15)
print(r.status_code)
print(pretty(r))
if r.status_code != 200:
    raise SystemExit('No payments list')

payments = r.json()
# payments puede ser lista o dict con results
candidates = []
if isinstance(payments, dict):
    # DRF paginado
    items = payments.get('results') or payments.get('data') or payments.get('transactions') or []
else:
    items = payments

for p in items:
    try:
        if p.get('financial_fee') == FINANCIAL_FEE_ID and p.get('status') in ['Pendiente', 'Procesando']:
            candidates.append(p)
    except Exception:
        continue

if not candidates:
    print('No hay transacciones pendientes para la cuota', FINANCIAL_FEE_ID)
    raise SystemExit

tx = candidates[0]
transaction_id = tx.get('transaction_id')
print('\nUsando transaction_id:', transaction_id)

print('\nConstruyendo payload y firmando...')
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
                'resident_id': str(tx.get('resident'))
            }
        }
    }
}

payload = json.dumps(event)

ts = str(int(time.time()))
_signed = hmac.new(STRIPE_WEBHOOK_SECRET.encode('utf-8'), msg=f"{ts}.{payload}".encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
sig_header = f"t={ts},v1={_signed}"

print('Stripe-Signature:', sig_header)

print('\nEnviando webhook...')
wh_headers = {"Content-Type": "application/json", "Stripe-Signature": sig_header, "Authorization": f"Bearer {access}"}
r = requests.post(f"{BASE_URL}/api/administration/payment-webhook/", data=payload.encode('utf-8'), headers=wh_headers, timeout=15)
print(r.status_code)
print(pretty(r))

print('\nFin')
