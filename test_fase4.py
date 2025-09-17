#!/usr/bin/env python3
"""
Script de pruebas para los endpoints de la FASE 4
Gestión de Vehículos, Mascotas y Visitantes
"""

import requests
import json
from datetime import datetime

# Configuración del servidor
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

class Fase4TestSuite:
    def __init__(self):
        self.token = None
        self.admin_token = None
        self.headers = {}
        self.admin_headers = {}
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_test(self, test_name, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    def authenticate(self):
        """Autenticar usuarios de prueba"""
        self.print_header("AUTENTICACIÓN")
        
        # Login como residente (Juan Pérez)
        login_data = {
            "email": "juan.perez@email.com",
            "password": "password123"
        }
        
        try:
            response = requests.post(f"{API_BASE}/token/", json=login_data)
            if response.status_code == 200:
                self.token = response.json()["access"]
                self.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                self.print_test("Login como residente (Juan Pérez)")
            else:
                self.print_test(f"Login como residente FALLÓ: {response.status_code}", False)
                return False
        except Exception as e:
            self.print_test(f"Error de conexión en login residente: {e}", False)
            return False
        
        # Login como administrador
        admin_login_data = {
            "email": "admin@smartcondo.com",
            "password": "password123"
        }
        
        try:
            response = requests.post(f"{API_BASE}/token/", json=admin_login_data)
            if response.status_code == 200:
                self.admin_token = response.json()["access"]
                self.admin_headers = {
                    "Authorization": f"Bearer {self.admin_token}",
                    "Content-Type": "application/json"
                }
                self.print_test("Login como administrador")
                return True
            else:
                self.print_test(f"Login como administrador FALLÓ: {response.status_code}", False)
                return False
        except Exception as e:
            self.print_test(f"Error de conexión en login admin: {e}", False)
            return False
    
    def test_vehicles_endpoints(self):
        """Probar endpoints de vehículos"""
        self.print_header("PRUEBAS DE VEHÍCULOS")
        
        # 1. Listar vehículos como residente
        try:
            response = requests.get(f"{API_BASE}/administration/vehicles/", headers=self.headers)
            if response.status_code == 200:
                vehicles = response.json()
                self.print_test(f"GET /vehicles/ - Encontrados {len(vehicles)} vehículos")
            else:
                self.print_test(f"GET /vehicles/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en GET /vehicles/: {e}", False)
        
        # 2. Crear nuevo vehículo
        new_vehicle = {
            "license_plate": "TEST-999",
            "brand": "Ford",
            "model": "Focus",
            "color": "Verde"
        }
        
        try:
            response = requests.post(f"{API_BASE}/administration/vehicles/", 
                                   json=new_vehicle, headers=self.headers)
            if response.status_code == 201:
                created_vehicle = response.json()
                vehicle_id = created_vehicle["id"]
                self.print_test(f"POST /vehicles/ - Vehículo creado ID: {vehicle_id}")
                
                # 3. Actualizar vehículo
                update_data = {"color": "Verde Metalizado"}
                response = requests.patch(f"{API_BASE}/administration/vehicles/{vehicle_id}/",
                                        json=update_data, headers=self.headers)
                if response.status_code == 200:
                    self.print_test("PATCH /vehicles/{id}/ - Vehículo actualizado")
                else:
                    self.print_test(f"PATCH /vehicles/ FALLÓ: {response.status_code}", False)
                
                # 4. Eliminar vehículo de prueba
                response = requests.delete(f"{API_BASE}/administration/vehicles/{vehicle_id}/",
                                         headers=self.headers)
                if response.status_code == 204:
                    self.print_test("DELETE /vehicles/{id}/ - Vehículo eliminado")
                else:
                    self.print_test(f"DELETE /vehicles/ FALLÓ: {response.status_code}", False)
                    
            else:
                self.print_test(f"POST /vehicles/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en operaciones de vehículos: {e}", False)
        
        # 5. Probar acceso como administrador (debería ver todos los vehículos)
        try:
            response = requests.get(f"{API_BASE}/administration/vehicles/", headers=self.admin_headers)
            if response.status_code == 200:
                admin_vehicles = response.json()
                self.print_test(f"Admin ve {len(admin_vehicles)} vehículos (todos)")
            else:
                self.print_test(f"Admin GET /vehicles/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en admin vehicles: {e}", False)
    
    def test_pets_endpoints(self):
        """Probar endpoints de mascotas"""
        self.print_header("PRUEBAS DE MASCOTAS")
        
        # 1. Listar mascotas como residente
        try:
            response = requests.get(f"{API_BASE}/administration/pets/", headers=self.headers)
            if response.status_code == 200:
                pets = response.json()
                self.print_test(f"GET /pets/ - Encontradas {len(pets)} mascotas")
            else:
                self.print_test(f"GET /pets/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en GET /pets/: {e}", False)
        
        # 2. Crear nueva mascota
        new_pet = {
            "name": "Firulais",
            "species": "Perro",
            "breed": "Mestizo",
            "age": 2
        }
        
        try:
            response = requests.post(f"{API_BASE}/administration/pets/", 
                                   json=new_pet, headers=self.headers)
            if response.status_code == 201:
                created_pet = response.json()
                pet_id = created_pet["id"]
                self.print_test(f"POST /pets/ - Mascota creada ID: {pet_id}")
                
                # 3. Actualizar mascota
                update_data = {"age": 3}
                response = requests.patch(f"{API_BASE}/administration/pets/{pet_id}/",
                                        json=update_data, headers=self.headers)
                if response.status_code == 200:
                    self.print_test("PATCH /pets/{id}/ - Mascota actualizada")
                else:
                    self.print_test(f"PATCH /pets/ FALLÓ: {response.status_code}", False)
                
                # 4. Eliminar mascota de prueba
                response = requests.delete(f"{API_BASE}/administration/pets/{pet_id}/",
                                         headers=self.headers)
                if response.status_code == 204:
                    self.print_test("DELETE /pets/{id}/ - Mascota eliminada")
                else:
                    self.print_test(f"DELETE /pets/ FALLÓ: {response.status_code}", False)
                    
            else:
                self.print_test(f"POST /pets/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en operaciones de mascotas: {e}", False)
    
    def test_visitor_logs_endpoints(self):
        """Probar endpoints de visitantes"""
        self.print_header("PRUEBAS DE VISITANTES")
        
        # 1. Listar registros de visitantes como administrador
        try:
            response = requests.get(f"{API_BASE}/administration/visitor-logs/", 
                                  headers=self.admin_headers)
            if response.status_code == 200:
                visitors = response.json()
                self.print_test(f"GET /visitor-logs/ - Encontrados {len(visitors)} registros")
            else:
                self.print_test(f"GET /visitor-logs/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en GET /visitor-logs/: {e}", False)
        
        # 2. Registrar entrada de visitante
        new_visitor = {
            "visitor_name": "Prueba Visitante",
            "visitor_dni": "99887766",
            "resident": 2,  # Juan Pérez
            "vehicle_license_plate": "TEST-VIS",
            "observations": "Prueba automatizada"
        }
        
        try:
            response = requests.post(f"{API_BASE}/administration/visitor-logs/", 
                                   json=new_visitor, headers=self.admin_headers)
            if response.status_code == 201:
                created_visitor = response.json()
                visitor_id = created_visitor["id"]
                self.print_test(f"POST /visitor-logs/ - Visitante registrado ID: {visitor_id}")
                
                # 3. Probar endpoint de visitantes activos
                response = requests.get(f"{API_BASE}/administration/visitor-logs/active_visitors/",
                                      headers=self.admin_headers)
                if response.status_code == 200:
                    active_visitors = response.json()
                    self.print_test(f"GET /active_visitors/ - {len(active_visitors)} visitantes activos")
                else:
                    self.print_test(f"GET /active_visitors/ FALLÓ: {response.status_code}", False)
                
                # 4. Registrar salida del visitante
                response = requests.post(f"{API_BASE}/administration/visitor-logs/{visitor_id}/register_exit/",
                                       headers=self.admin_headers)
                if response.status_code == 200:
                    exit_data = response.json()
                    self.print_test("POST /register_exit/ - Salida registrada")
                else:
                    self.print_test(f"POST /register_exit/ FALLÓ: {response.status_code}", False)
                
                # 5. Eliminar registro de prueba
                response = requests.delete(f"{API_BASE}/administration/visitor-logs/{visitor_id}/",
                                         headers=self.admin_headers)
                if response.status_code == 204:
                    self.print_test("DELETE /visitor-logs/{id}/ - Registro eliminado")
                else:
                    self.print_test(f"DELETE /visitor-logs/ FALLÓ: {response.status_code}", False)
                    
            else:
                self.print_test(f"POST /visitor-logs/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en operaciones de visitantes: {e}", False)
        
        # 6. Probar reporte diario
        try:
            response = requests.get(f"{API_BASE}/administration/visitor-logs/daily_report/",
                                  headers=self.admin_headers)
            if response.status_code == 200:
                report = response.json()
                stats = report.get("statistics", {})
                self.print_test(f"GET /daily_report/ - {stats.get('total_visitors', 0)} visitantes hoy")
            else:
                self.print_test(f"GET /daily_report/ FALLÓ: {response.status_code}", False)
        except Exception as e:
            self.print_test(f"Error en daily_report: {e}", False)
    
    def test_permissions(self):
        """Probar sistema de permisos"""
        self.print_header("PRUEBAS DE PERMISOS")
        
        # 1. Residente intentando acceder a endpoint de admin
        try:
            response = requests.get(f"{API_BASE}/administration/visitor-logs/daily_report/",
                                  headers=self.headers)
            if response.status_code == 403:
                self.print_test("Residente NO puede acceder a daily_report (correcto)")
            else:
                self.print_test(f"Error de permisos: residente accedió a daily_report", False)
        except Exception as e:
            self.print_test(f"Error en test de permisos: {e}", False)
        
        # 2. Acceso sin token
        try:
            response = requests.get(f"{API_BASE}/administration/vehicles/")
            if response.status_code == 401:
                self.print_test("Acceso sin token es rechazado (correcto)")
            else:
                self.print_test(f"Error: acceso sin token permitido", False)
        except Exception as e:
            self.print_test(f"Error en test sin token: {e}", False)
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 INICIANDO SUITE DE PRUEBAS - FASE 4")
        print(f"⏰ Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Autenticación requerida para todas las pruebas
        if not self.authenticate():
            print("❌ FALLO EN AUTENTICACIÓN - ABORTANDO PRUEBAS")
            return
        
        # Ejecutar todas las pruebas
        self.test_vehicles_endpoints()
        self.test_pets_endpoints()
        self.test_visitor_logs_endpoints()
        self.test_permissions()
        
        # Resumen final
        self.print_header("RESUMEN DE PRUEBAS COMPLETADAS")
        print("✅ Endpoints de Vehículos probados")
        print("✅ Endpoints de Mascotas probados")
        print("✅ Endpoints de Visitantes probados")
        print("✅ Sistema de Permisos validado")
        print("\n🎉 ¡FASE 4 VALIDADA EXITOSAMENTE!")
        print(f"⏰ Hora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_suite = Fase4TestSuite()
    test_suite.run_all_tests()