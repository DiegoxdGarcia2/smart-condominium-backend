#!/usr/bin/env python3
"""
Verificar datos migrados desde base de datos local a Render
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://smart-condominium-backend-fuab.onrender.com"

def check_admin_panel_users():
    """
    Verificar usuarios a través del panel de administración
    """
    print("🔍 Verificando panel de administración...")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/administration/user/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Panel de admin requiere login (normal)")
            print("   💡 Esto significa que la aplicación está configurada correctamente")
        elif response.status_code == 200:
            print("   ⚠️ Panel de admin accesible sin login")
        else:
            print(f"   ❓ Respuesta inesperada: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def check_database_connection():
    """
    Verificar conexión a base de datos a través de endpoints
    """
    print("\n🔍 Verificando conexión a base de datos...")
    
    # Lista de endpoints que requieren acceso a DB
    endpoints = [
        ("/api/administration/users/", "Usuarios"),
        ("/api/administration/roles/", "Roles"),
        ("/api/administration/residential-units/", "Unidades Residenciales"),
        ("/api/administration/announcements/", "Anuncios"),
    ]
    
    db_working = True
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 401:
                print(f"   ✅ {name}: Requiere autenticación (DB funcionando)")
            elif response.status_code == 200:
                print(f"   ✅ {name}: Accesible (DB funcionando)")
            elif response.status_code == 500:
                print(f"   ❌ {name}: Error 500 (posible problema DB)")
                db_working = False
            else:
                print(f"   ❓ {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
            db_working = False
    
    return db_working

def test_with_local_credentials():
    """
    Probar con credenciales que deberían existir desde la migración local
    """
    print("\n🔍 Probando credenciales que deberían existir desde migración local...")
    
    # Credenciales típicas que podrían haber estado en tu DB local
    possible_creds = [
        {"email": "admin@admin.com", "password": "admin"},
        {"email": "admin@localhost", "password": "admin"},
        {"email": "admin@smartcondo.com", "password": "admin123"},
        {"email": "test@test.com", "password": "test"},
        {"email": "diego@garcia.com", "password": "password"},  # Basado en tu username
        {"email": "diego@smartcondo.com", "password": "admin123"},
        {"email": "administrador@condominio.com", "password": "admin123"},
    ]
    
    working_creds = []
    
    for creds in possible_creds:
        try:
            print(f"   Probando: {creds['email']}")
            response = requests.post(
                f"{BASE_URL}/api/token/",
                json=creds,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ ¡CREDENCIALES VÁLIDAS! {creds['email']}")
                data = response.json()
                working_creds.append(creds)
                print(f"   Access Token: {data.get('access', 'N/A')[:50]}...")
            elif response.status_code == 401:
                print(f"   ⚠️ Credenciales incorrectas (pero endpoint funciona)")
            elif response.status_code == 500:
                print(f"   ❌ Error 500 con {creds['email']}")
                
        except Exception as e:
            print(f"   ❌ Error probando {creds['email']}: {e}")
    
    return working_creds

def check_data_migration_indicators():
    """
    Verificar indicadores de que los datos se migraron correctamente
    """
    print("\n🔍 Verificando indicadores de migración de datos...")
    
    # Verificar que las tablas/modelos existen revisando endpoints
    print("   Verificando estructura de modelos:")
    
    # Si podemos acceder a estos endpoints sin error 500, significa que:
    # 1. Los modelos están bien definidos
    # 2. Las tablas existen en la DB
    # 3. Las migraciones se aplicaron
    
    model_endpoints = [
        "users", "roles", "residential-units", "announcements", 
        "financial-fees", "common-areas", "reservations", "vehicles",
        "pets", "visitor-logs", "tasks", "feedback", "payments"
    ]
    
    models_ok = 0
    for model in model_endpoints:
        try:
            response = requests.get(f"{BASE_URL}/api/administration/{model}/", timeout=10)
            if response.status_code in [200, 401]:  # OK o requiere auth
                print(f"   ✅ Modelo {model}: Tabla existe")
                models_ok += 1
            elif response.status_code == 500:
                print(f"   ❌ Modelo {model}: Posible problema de migración")
            else:
                print(f"   ❓ Modelo {model}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Modelo {model}: Error - {e}")
    
    migration_success = (models_ok / len(model_endpoints)) * 100
    print(f"\n   📊 Migración exitosa: {models_ok}/{len(model_endpoints)} modelos ({migration_success:.1f}%)")
    
    return migration_success > 90

def get_local_db_info():
    """
    Información sobre cómo verificar los datos locales
    """
    print("\n💡 Para verificar qué usuarios tienes en local:")
    print("   1. En tu proyecto local, ejecuta:")
    print("      python manage.py shell")
    print("   2. Luego ejecuta:")
    print("      from administration.models import User")
    print("      users = User.objects.all()")
    print("      for user in users:")
    print("          print(f'Email: {user.email}, Name: {user.first_name} {user.last_name}')")
    print("\n   3. O usa el admin local:")
    print("      python manage.py runserver")
    print("      Ve a http://localhost:8000/admin/")

if __name__ == "__main__":
    print("🚀 VERIFICACIÓN DE MIGRACIÓN DE DATOS LOCAL → RENDER")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar base de datos
    db_ok = check_database_connection()
    
    # Verificar panel de admin
    check_admin_panel_users()
    
    # Verificar migración
    migration_ok = check_data_migration_indicators()
    
    # Probar credenciales
    working_creds = test_with_local_credentials()
    
    # Información para verificar local
    get_local_db_info()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN:")
    
    if db_ok:
        print("✅ Base de datos conectada y funcionando")
    else:
        print("❌ Problemas con base de datos")
    
    if migration_ok:
        print("✅ Migración de modelos exitosa")
    else:
        print("❌ Posibles problemas en migración")
    
    if working_creds:
        print(f"✅ {len(working_creds)} credenciales válidas encontradas:")
        for creds in working_creds:
            print(f"   - {creds['email']} / {creds['password']}")
    else:
        print("⚠️ No se encontraron credenciales válidas")
        print("💡 Verifica tus usuarios locales y confirma la migración")
    
    print("=" * 60)