#!/usr/bin/env python3
"""
Script de pruebas manuales para la API del Smart Condominium Backend
Ejecutar con: python test_api.py
"""

import requests
import json
import sys

# Configuración base
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_result(test_name, success, response=None, error=None):
    """Imprime el resultado de una prueba"""
    status = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if success else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
    print(f"{status} {test_name}")
    
    if response and hasattr(response, 'status_code'):
        print(f"    Status: {response.status_code}")
        if hasattr(response, 'json'):
            try:
                data = response.json()
                if isinstance(data, dict) and len(data) < 10:
                    print(f"    Response: {json.dumps(data, indent=2)}")
                else:
                    print(f"    Response: {type(data)} with {len(data) if hasattr(data, '__len__') else 'unknown'} items")
            except:
                print(f"    Response: {response.text[:100]}...")
    
    if error:
        print(f"    Error: {error}")
    print()

def test_server_connection():
    """Prueba que el servidor esté ejecutándose"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return True, response
    except requests.exceptions.ConnectionError:
        return False, None
    except Exception as e:
        return False, str(e)

def test_token_authentication():
    """Prueba la autenticación JWT"""
    # Datos de usuario de prueba
    credentials = {
        "email": "juan.perez@email.com",
        "password": "password123"
    }
    
    try:
        # Obtener token
        response = requests.post(f"{API_BASE}/token/", json=credentials)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            refresh_token = token_data.get('refresh')
            
            if access_token and refresh_token:
                return True, response, {"access": access_token, "refresh": refresh_token}
            else:
                return False, response, None
        else:
            return False, response, None
            
    except Exception as e:
        return False, None, str(e)

def test_refresh_token(refresh_token):
    """Prueba el refresh de token"""
    try:
        response = requests.post(f"{API_BASE}/token/refresh/", json={"refresh": refresh_token})
        return response.status_code == 200, response
    except Exception as e:
        return False, str(e)

def test_authenticated_endpoint(endpoint, token, method="GET", data=None):
    """Prueba un endpoint autenticado"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{API_BASE}{endpoint}", headers=headers, json=data)
        else:
            return False, "Método no soportado"
        
        return response.status_code in [200, 201], response
    except Exception as e:
        return False, str(e)

def test_unauthorized_access():
    """Prueba acceso sin autenticación"""
    try:
        response = requests.get(f"{API_BASE}/administration/users/")
        return response.status_code == 401, response
    except Exception as e:
        return False, str(e)

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print(f"{Colors.BOLD}{Colors.BLUE}=== PRUEBAS DE API - SMART CONDOMINIUM BACKEND ==={Colors.ENDC}\n")
    
    # Prueba 1: Conexión al servidor
    print(f"{Colors.YELLOW}1. Probando conexión al servidor...{Colors.ENDC}")
    success, response = test_server_connection()
    print_result("Conexión al servidor", success, response, None if success else "Servidor no disponible")
    
    if not success:
        print(f"{Colors.RED}❌ El servidor no está ejecutándose. Ejecuta: python manage.py runserver{Colors.ENDC}")
        return False
    
    # Prueba 2: Autenticación JWT
    print(f"{Colors.YELLOW}2. Probando autenticación JWT...{Colors.ENDC}")
    auth_success, auth_response, tokens = test_token_authentication()
    print_result("Obtener token JWT", auth_success, auth_response)
    
    if not auth_success:
        print(f"{Colors.RED}❌ No se pudo obtener token. Verifica que los datos iniciales estén cargados.{Colors.ENDC}")
        return False
    
    access_token = tokens["access"]
    refresh_token = tokens["refresh"]
    
    # Prueba 3: Refresh token
    print(f"{Colors.YELLOW}3. Probando refresh de token...{Colors.ENDC}")
    refresh_success, refresh_response = test_refresh_token(refresh_token)
    print_result("Refresh token", refresh_success, refresh_response)
    
    # Prueba 4: Acceso no autorizado
    print(f"{Colors.YELLOW}4. Probando acceso no autorizado...{Colors.ENDC}")
    unauth_success, unauth_response = test_unauthorized_access()
    print_result("Acceso no autorizado (debe fallar)", unauth_success, unauth_response)
    
    # Prueba 5: Endpoints autenticados
    print(f"{Colors.YELLOW}5. Probando endpoints autenticados...{Colors.ENDC}")
    
    endpoints_to_test = [
        ("/administration/roles/", "GET", "Listar roles"),
        ("/administration/users/", "GET", "Listar usuarios"),
        ("/administration/residential-units/", "GET", "Listar unidades residenciales"),
    ]
    
    for endpoint, method, description in endpoints_to_test:
        success, response = test_authenticated_endpoint(endpoint, access_token, method)
        print_result(description, success, response)
    
    # Prueba 6: Crear datos via API
    print(f"{Colors.YELLOW}6. Probando creación de datos...{Colors.ENDC}")
    
    # Crear un nuevo rol
    new_role_data = {"name": "Portero"}
    success, response = test_authenticated_endpoint("/administration/roles/", access_token, "POST", new_role_data)
    print_result("Crear nuevo rol", success, response)
    
    # Crear nueva unidad residencial
    new_unit_data = {
        "unit_number": "TEST-001",
        "type": "Departamento",
        "floor": 5
    }
    success, response = test_authenticated_endpoint("/administration/residential-units/", access_token, "POST", new_unit_data)
    print_result("Crear nueva unidad residencial", success, response)
    
    print(f"{Colors.BOLD}{Colors.GREEN}=== PRUEBAS COMPLETADAS ==={Colors.ENDC}")
    return True

def main():
    """Función principal"""
    try:
        success = run_all_tests()
        if success:
            print(f"\n{Colors.GREEN}✅ Todas las pruebas principales pasaron exitosamente!{Colors.ENDC}")
            print(f"\n{Colors.BLUE}💡 Puedes probar manualmente en:{Colors.ENDC}")
            print(f"   - Admin: {BASE_URL}/admin/")
            print(f"   - API Browse: {BASE_URL}/api/administration/")
        else:
            print(f"\n{Colors.RED}❌ Algunas pruebas fallaron. Revisa la configuración.{Colors.ENDC}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Pruebas canceladas por el usuario.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
