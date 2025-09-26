import requests, sys
base='https://smart-condominium-backend-fuab.onrender.com'
endpoints = [
    '/',
    '/api/',
    '/api/token/',
    '/api/token/refresh/',
    '/api/administration/roles/',
    '/api/administration/users/',
    '/api/administration/residential-units/',
    '/api/administration/announcements/',
    '/api/administration/financial-fees/',
    '/api/administration/common-areas/',
    '/api/administration/reservations/',
    '/api/administration/vehicles/',
    '/api/administration/pets/',
    '/api/administration/visitor-logs/',
    '/api/administration/tasks/',
    '/api/administration/feedback/',
    '/api/administration/payments/',
    '/api/administration/initiate-payment/',
    '/api/administration/payment-webhook/',
]

print('Starting full API smoke test...')
results = []
# Get token
try:
    r = requests.post(base + '/api/token/', json={'email':'admin@test.com','password':'admin123'}, timeout=20)
    if r.status_code == 200:
        token = r.json().get('access')
        refresh = r.json().get('refresh')
        print('Obtained token')
    else:
        token = None
        refresh = None
        print('Failed to obtain token:', r.status_code, r.text)
except Exception as e:
    print('Token request error:', e)
    token = None
    refresh = None

for ep in endpoints:
    url = base + ep
    try:
        headers = {}
        # Use token for administration endpoints
        if ep.startswith('/api/administration/') and token:
            headers['Authorization'] = 'Bearer ' + token
        # If endpoint is webhook, try GET first (should be 405 or 200)
        if ep.endswith('payment-webhook/') or ep.endswith('initiate-payment/'):
            # try GET then POST with empty body
            r = requests.get(url, headers=headers, timeout=15)
            results.append((ep, 'GET', r.status_code, r.text[:200]))
            rpost = requests.post(url, headers=headers, json={}, timeout=15)
            results.append((ep, 'POST', rpost.status_code, rpost.text[:200]))
        else:
            r = requests.get(url, headers=headers, timeout=15)
            results.append((ep, 'GET', r.status_code, r.text[:200]))
    except Exception as e:
        results.append((ep, 'ERROR', str(e), ''))

# Print concise results
ok = True
for r in results:
    ep, method, code, info = r
    print(f'{method:4} {ep:35} -> {code}')
    if not (isinstance(code,int) and 200 <= code < 300):
        ok = False
        print('    ', info)

print('\nSummary:', 'OK' if ok else 'SOME FAILURES')
if not ok:
    sys.exit(2)
else:
    sys.exit(0)
