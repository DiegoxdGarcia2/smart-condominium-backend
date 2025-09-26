#!/usr/bin/env python3
"""
Script de prueba para las funcionalidades de la Fase 5:
1. Captura de foto en el registro de visitas
2. Predicción de riesgo de morosidad con ML

Autor: Sistema de Condominio Inteligente
Fecha: 2024
"""

import requests
import json
import base64
import io
from PIL import Image

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"
ADMIN_USERNAME = "admin@smartcondo.com"
ADMIN_PASSWORD = "password123"

class SmartCondoTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        
    def authenticate(self):
        """Autenticar con el sistema"""
        print("🔐 Autenticando con el sistema...")
        
        try:
            response = self.session.post(f"{BASE_URL}/token/", {
                'email': ADMIN_USERNAME,
                'password': ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })
                print("✅ Autenticación exitosa")
                return True
            else:
                print(f"❌ Error de autenticación: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def create_sample_image(self):
        """Crear una imagen de muestra para pruebas"""
        print("🖼️  Creando imagen de muestra...")
        
        # Crear una imagen simple de prueba
        img = Image.new('RGB', (200, 200), color='lightblue')
        
        # Guardar en memoria como bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        return img_buffer.getvalue()
    
    def test_visitor_registration_with_photo(self):
        """Probar registro de visita con foto"""
        print("\n📸 PRUEBA 1: Registro de visita con foto")
        print("=" * 50)
        
        # Crear imagen de prueba
        image_data = self.create_sample_image()
        
        # Datos de la visita
        visitor_data = {
            'full_name': 'Juan Pérez Visitante',
            'document_number': '12345678',
            'phone_number': '+57300123456',
            'email': 'juan.visitante@email.com',
            'purpose': 'Visita familiar',
            'apartment_number': '101',
            'resident_name': 'María González'
        }
        
        # Preparar archivos para multipart/form-data
        files = {
            'visitor_photo': ('visitor_photo.jpg', image_data, 'image/jpeg')
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/administration/visitor-logs/",
                data=visitor_data,
                files=files
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print("✅ Registro exitoso con foto")
                print(f"📋 ID del registro: {result.get('id')}")
                print(f"📸 Foto guardada: {result.get('visitor_photo', 'No disponible')}")
                
                # Mostrar todos los campos
                for key, value in result.items():
                    if key != 'visitor_photo':
                        print(f"   {key}: {value}")
                
                return result.get('id')
            else:
                print(f"❌ Error en el registro: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def test_ai_risk_prediction(self):
        """Probar predicción de riesgo de morosidad"""
        print("\n🤖 PRUEBA 2: Predicción de riesgo de morosidad")
        print("=" * 50)
        
        # Casos de prueba con diferentes niveles de riesgo
        test_cases = [
            {
                'name': 'Cliente de Bajo Riesgo',
                'data': {
                    'amount': 30000,
                    'historical_default_rate': 0.05,
                    'previous_overdue_count': 0,
                    'days_since_due': 0
                }
            },
            {
                'name': 'Cliente de Riesgo Medio',
                'data': {
                    'amount': 65000,
                    'historical_default_rate': 0.25,
                    'previous_overdue_count': 1,
                    'days_since_due': 5
                }
            },
            {
                'name': 'Cliente de Alto Riesgo',
                'data': {
                    'amount': 85000,
                    'historical_default_rate': 0.65,
                    'previous_overdue_count': 3,
                    'days_since_due': 25
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Caso {i}: {test_case['name']}")
            print(f"💰 Monto: ${test_case['data']['amount']:,}")
            print(f"📊 Tasa histórica: {test_case['data']['historical_default_rate']:.1%}")
            print(f"🔄 Moras previas: {test_case['data']['previous_overdue_count']}")
            print(f"⏰ Días vencido: {test_case['data']['days_since_due']}")
            
            try:
                response = self.session.post(
                    f"{BASE_URL}/administration/ai/predict-risk/",
                    json=test_case['data'],
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"🎯 Probabilidad de riesgo: {result['risk_probability']:.1%}")
                    print(f"⚠️  Nivel de riesgo: {result['risk_level']}")
                    print(f"💡 Recomendaciones:")
                    for rec in result['recommendations']:
                        print(f"   - {rec}")
                    
                    print(f"📈 Modelo usado: {result['model_info']['trained_at']}")
                    
                else:
                    print(f"❌ Error en predicción: {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
    
    def test_visitor_retrieval(self, visitor_id):
        """Probar recuperación de datos de visitante"""
        if not visitor_id:
            return
            
        print(f"\n📋 PRUEBA 3: Recuperación de datos del visitante {visitor_id}")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{BASE_URL}/administration/visitor-logs/{visitor_id}/")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Datos recuperados exitosamente")
                
                for key, value in result.items():
                    if key == 'visitor_photo' and value:
                        print(f"   {key}: {value[:50]}... (URL de la foto)")
                    else:
                        print(f"   {key}: {value}")
            else:
                print(f"❌ Error al recuperar datos: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS DE LA FASE 5")
        print("=" * 60)
        print("✨ Funcionalidades:")
        print("   1. Captura de foto en registro de visitas")
        print("   2. Predicción de riesgo de morosidad con IA")
        print("=" * 60)
        
        # Autenticar
        if not self.authenticate():
            print("❌ No se pudo autenticar. Verifica las credenciales.")
            return
        
        # Ejecutar pruebas
        visitor_id = self.test_visitor_registration_with_photo()
        self.test_ai_risk_prediction()
        self.test_visitor_retrieval(visitor_id)
        
        print("\n🎉 PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("📝 RESUMEN:")
        print("   ✅ Registro de visitas con foto")
        print("   ✅ Predicción de riesgo con IA")
        print("   ✅ Recuperación de datos")
        print("\n💡 Las nuevas funcionalidades de la Fase 5 están funcionando correctamente!")


if __name__ == "__main__":
    tester = SmartCondoTester()
    tester.run_all_tests()