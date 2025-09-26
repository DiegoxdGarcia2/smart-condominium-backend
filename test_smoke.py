import requests, sys
base='https://smart-condominium-backend-fuab.onrender.com'
results=[]
print('Iniciando smoke tests rápidos...')
# 1. Root
try:
    r=requests.get(base+'/', timeout=10)
    results.append(('GET /', r.status_code, r.text[:200]))
except Exception as e:
    results.append(('GET /', 'ERROR', str(e)))
# 2. API root
try:
    r=requests.get(base+'/api/', timeout=10)
    results.append(('GET /api/', r.status_code, r.text[:200]))
except Exception as e:
    results.append(('GET /api/', 'ERROR', str(e)))
# 3. Token obtain
token=None
refresh=None
try:
    r=requests.post(base+'/api/token/', json={'email':'admin@test.com','password':'admin123'}, timeout=15)
    results.append(('POST /api/token/', r.status_code, r.text[:200]))
    if r.status_code==200:
        j=r.json()
        token=j.get('access')
        refresh=j.get('refresh')
except Exception as e:
    results.append(('POST /api/token/', 'ERROR', str(e)))
# 4. Token refresh (if we have refresh)
if refresh:
    try:
        rr=requests.post(base+'/api/token/refresh/', json={'refresh': refresh}, timeout=15)
        results.append(('POST /api/token/refresh/', rr.status_code, rr.text[:200]))
    except Exception as e:
        results.append(('POST /api/token/refresh/', 'ERROR', str(e)))
# 5. Protected users list
if token:
    try:
        h={'Authorization':f'Bearer {token}'}
        rr=requests.get(base+'/api/administration/users/', headers=h, timeout=15)
        results.append(('GET /api/administration/users/', rr.status_code, str(rr.json())[:400]))
    except Exception as e:
        results.append(('GET /api/administration/users/', 'ERROR', str(e)))
# 6. Additional endpoints
paths=['/api/administration/announcements/','/api/administration/commonareas/','/api/administration/paymenttransactions/']
for p in paths:
    try:
        if token:
            rr=requests.get(base+p, headers={'Authorization':f'Bearer {token}'}, timeout=15)
        else:
            rr=requests.get(base+p, timeout=15)
        results.append((f'GET {p}', rr.status_code, str(rr.text)[:300]))
    except Exception as e:
        results.append((f'GET {p}', 'ERROR', str(e)))

print('\nResultados:')
ok=True
for r in results:
    name, code, info = r
    print(f'{name:40} -> {code}')
    if not (isinstance(code,int) and 200<=code<300):
        print('   ', info)
        ok=False
print('\nResumen:', 'OK' if ok else 'FALLÓ')
if not ok:
    sys.exit(2)
else:
    sys.exit(0)
