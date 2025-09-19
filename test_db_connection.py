#!/usr/bin/env python3
"""
Script para probar la conectividad con la base de datos de Render
"""

import os
import sys
import psycopg2
from psycopg2 import sql

# Configuración de la base de datos de Render
DB_CONFIG = {
    'host': 'dpg-d36co28gjchc73c6rekg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'smartcondominio',
    'user': 'smartcondominio_user',
    'password': '3gRivgyPRtg988KIAvsfMJu7IjpRacff'
}

DATABASE_URL = "postgresql://smartcondominio_user:3gRivgyPRtg988KIAvsfMJu7IjpRacff@dpg-d36co28gjchc73c6rekg-a.oregon-postgres.render.com/smartcondominio"

def test_connection():
    """Probar conexión directa con psycopg2"""
    try:
        print("🔌 Probando conexión directa a la base de datos...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"User: {DB_CONFIG['user']}")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Probar consulta simple
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conexión exitosa!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Verificar tablas de Django
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 Tablas encontradas ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar datos de usuarios (modelo personalizado)
        cursor.execute("SELECT COUNT(*) FROM administration_user;")
        user_count = cursor.fetchone()[0]
        print(f"\n👥 Usuarios en el sistema: {user_count}")
        
        # Verificar cuotas financieras
        cursor.execute("SELECT COUNT(*) FROM administration_financialfee;")
        fee_count = cursor.fetchone()[0]
        print(f"💰 Cuotas financieras: {fee_count}")
        
        # Verificar transacciones de pago
        cursor.execute("SELECT COUNT(*) FROM administration_paymenttransaction;")
        transaction_count = cursor.fetchone()[0]
        print(f"💳 Transacciones de pago: {transaction_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_django_connection():
    """Probar conexión usando Django ORM"""
    try:
        print("\n🐍 Probando conexión con Django...")
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcondo_backend.settings')
        os.environ['DATABASE_URL'] = DATABASE_URL
        os.environ['SECRET_KEY'] = '3gRivgyPRtg988KIAvsfMJu7IjpRacff'
        os.environ['DEBUG'] = 'FALSE'
        
        import django
        django.setup()
        
        from django.db import connection
        from administration.models import User, FinancialFee, PaymentTransaction
        
        # Probar conexión
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Django ORM conectado correctamente!")
        
        # Verificar modelos
        user_count = User.objects.count()
        fee_count = FinancialFee.objects.count()
        transaction_count = PaymentTransaction.objects.count()
        
        print(f"👥 Usuarios (Django ORM): {user_count}")
        print(f"💰 Cuotas (Django ORM): {fee_count}")
        print(f"💳 Transacciones (Django ORM): {transaction_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con Django: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Database Connection to Render PostgreSQL")
    print("=" * 60)
    
    # Test 1: Conexión directa
    db_ok = test_connection()
    
    # Test 2: Conexión con Django
    if db_ok:
        django_ok = test_django_connection()
    
    print("\n" + "=" * 60)
    if db_ok:
        print("✅ La base de datos está funcionando correctamente!")
        print("📝 Ahora configura las variables de entorno en Render:")
        print("   1. DATABASE_URL =", DATABASE_URL)
        print("   2. SECRET_KEY = 3gRivgyPRtg988KIAvsfMJu7IjpRacff")
        print("   3. DEBUG = FALSE")
        print("   4. STRIPE_WEBHOOK_SECRET = whsec_hLXZ2H23yX1A1o5T7SzA1b4NfublNwAU")
    else:
        print("❌ Hay problemas con la conexión a la base de datos")