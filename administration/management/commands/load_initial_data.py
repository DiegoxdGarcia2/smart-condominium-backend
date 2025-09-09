"""
Comando personalizado para cargar datos iniciales en la base de datos.
Ejecutar con: python manage.py load_initial_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from administration.models import Role, ResidentialUnit, Announcement, FinancialFee

User = get_user_model()


class Command(BaseCommand):
    help = 'Carga datos iniciales en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        
        # Crear roles
        roles_data = [
            'Administrador',
            'Residente',
            'Guardia',
            'Conserje'
        ]
        
        for role_name in roles_data:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(f'✓ Rol creado: {role_name}')
            else:
                self.stdout.write(f'- Rol ya existe: {role_name}')
        
        # Obtener roles para asignar
        admin_role = Role.objects.get(name='Administrador')
        resident_role = Role.objects.get(name='Residente')
        guard_role = Role.objects.get(name='Guardia')
        
        # Crear usuarios de ejemplo
        users_data = [
            {
                'username': 'admin_condo',
                'email': 'admin@smartcondo.com',
                'first_name': 'María',
                'last_name': 'Administradora',
                'phone_number': '+52-555-0001',
                'role': admin_role,
                'is_staff': True
            },
            {
                'username': 'residente1',
                'email': 'juan.perez@email.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'phone_number': '+52-555-0002',
                'role': resident_role
            },
            {
                'username': 'residente2',
                'email': 'ana.garcia@email.com',
                'first_name': 'Ana',
                'last_name': 'García',
                'phone_number': '+52-555-0003',
                'role': resident_role
            },
            {
                'username': 'guardia1',
                'email': 'carlos.seguridad@email.com',
                'first_name': 'Carlos',
                'last_name': 'Seguridad',
                'phone_number': '+52-555-0004',
                'role': guard_role
            }
        ]
        
        for user_data in users_data:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone_number=user_data['phone_number'],
                    role=user_data['role'],
                    password='password123'  # Contraseña temporal
                )
                if user_data.get('is_staff'):
                    user.is_staff = True
                    user.save()
                
                self.stdout.write(f'✓ Usuario creado: {user.email}')
            else:
                self.stdout.write(f'- Usuario ya existe: {user_data["email"]}')
        
        # Crear unidades residenciales
        units_data = [
            {
                'unit_number': 'A-101',
                'type': 'Departamento',
                'floor': 1,
                'owner_email': 'juan.perez@email.com'
            },
            {
                'unit_number': 'A-102',
                'type': 'Departamento',
                'floor': 1,
                'owner_email': None
            },
            {
                'unit_number': 'A-201',
                'type': 'Departamento',
                'floor': 2,
                'owner_email': 'ana.garcia@email.com'
            },
            {
                'unit_number': 'B-001',
                'type': 'Casa',
                'floor': None,
                'owner_email': None
            },
            {
                'unit_number': 'B-002',
                'type': 'Casa',
                'floor': None,
                'owner_email': None
            }
        ]
        
        for unit_data in units_data:
            if not ResidentialUnit.objects.filter(unit_number=unit_data['unit_number']).exists():
                owner = None
                if unit_data['owner_email']:
                    try:
                        owner = User.objects.get(email=unit_data['owner_email'])
                    except User.DoesNotExist:
                        pass
                
                unit = ResidentialUnit.objects.create(
                    unit_number=unit_data['unit_number'],
                    type=unit_data['type'],
                    floor=unit_data['floor'],
                    owner=owner
                )
                self.stdout.write(f'✓ Unidad creada: {unit.unit_number}')
            else:
                self.stdout.write(f'- Unidad ya existe: {unit_data["unit_number"]}')
        
        # Crear comunicados de ejemplo
        admin_user = User.objects.get(email='admin@smartcondo.com')
        announcements_data = [
            {
                'title': 'Bienvenidos al nuevo sistema Smart Condominium',
                'content': 'Nos complace anunciar el lanzamiento de nuestro nuevo sistema de gestión del condominio. A través de esta plataforma podrán consultar comunicados, revisar sus cuotas financieras y mantenerse informados sobre las actividades del condominio.',
                'author': admin_user
            },
            {
                'title': 'Mantenimiento de áreas comunes - Septiembre',
                'content': 'Estimados residentes, les informamos que el próximo martes 10 de septiembre se realizará el mantenimiento preventivo de las áreas comunes, incluyendo jardines, elevadores y sistema de seguridad. El trabajo se realizará de 9:00 AM a 3:00 PM.',
                'author': admin_user
            },
            {
                'title': 'Nuevas normas de uso del estacionamiento',
                'content': 'Por favor tomar nota de las nuevas normas para el uso del estacionamiento: 1) Respetar los espacios asignados, 2) No obstruir las vías de evacuación, 3) Velocidad máxima 10 km/h. Agradecemos su cooperación.',
                'author': admin_user
            }
        ]
        
        for announcement_data in announcements_data:
            if not Announcement.objects.filter(title=announcement_data['title']).exists():
                announcement = Announcement.objects.create(**announcement_data)
                self.stdout.write(f'✓ Comunicado creado: {announcement.title}')
            else:
                self.stdout.write(f'- Comunicado ya existe: {announcement_data["title"]}')
        
        # Crear cuotas financieras de ejemplo
        financial_fees_data = [
            {
                'unit': 'A-101',
                'description': 'Cuota de mantenimiento - Septiembre 2025',
                'amount': Decimal('1500.00'),
                'due_date': timezone.now().date() + timedelta(days=15),
                'status': 'Pendiente'
            },
            {
                'unit': 'A-101',
                'description': 'Cuota de mantenimiento - Agosto 2025',
                'amount': Decimal('1500.00'),
                'due_date': timezone.now().date() - timedelta(days=15),
                'status': 'Pagado'
            },
            {
                'unit': 'A-201',
                'description': 'Cuota de mantenimiento - Septiembre 2025',
                'amount': Decimal('1500.00'),
                'due_date': timezone.now().date() + timedelta(days=15),
                'status': 'Pendiente'
            },
            {
                'unit': 'A-201',
                'description': 'Reparación de plomería - Agosto 2025',
                'amount': Decimal('850.00'),
                'due_date': timezone.now().date() - timedelta(days=5),
                'status': 'Vencido'
            },
            {
                'unit': 'A-102',
                'description': 'Cuota de mantenimiento - Septiembre 2025',
                'amount': Decimal('1500.00'),
                'due_date': timezone.now().date() + timedelta(days=15),
                'status': 'Pendiente'
            }
        ]
        
        for fee_data in financial_fees_data:
            try:
                unit = ResidentialUnit.objects.get(unit_number=fee_data['unit'])
                
                # Verificar si ya existe esta cuota específica
                existing_fee = FinancialFee.objects.filter(
                    unit=unit,
                    description=fee_data['description']
                ).first()
                
                if not existing_fee:
                    fee = FinancialFee.objects.create(
                        unit=unit,
                        description=fee_data['description'],
                        amount=fee_data['amount'],
                        due_date=fee_data['due_date'],
                        status=fee_data['status']
                    )
                    self.stdout.write(f'✓ Cuota creada: {fee.description} - {unit.unit_number}')
                else:
                    self.stdout.write(f'- Cuota ya existe: {fee_data["description"]} - {fee_data["unit"]}')
            except ResidentialUnit.DoesNotExist:
                self.stdout.write(f'⚠ Unidad no encontrada: {fee_data["unit"]}')
        
        self.stdout.write(
            self.style.SUCCESS('\n¡Datos iniciales cargados exitosamente!')
        )
        self.stdout.write(
            'Credenciales de prueba:'
        )
        self.stdout.write(
            '- Admin: admin@smartcondo.com / password123'
        )
        self.stdout.write(
            '- Residente 1: juan.perez@email.com / password123'
        )
        self.stdout.write(
            '- Residente 2: ana.garcia@email.com / password123'
        )
        self.stdout.write(
            '- Guardia: carlos.seguridad@email.com / password123'
        )
        self.stdout.write(
            '\nNuevas funcionalidades disponibles:'
        )
        self.stdout.write(
            '📢 Comunicados: /api/administration/announcements/'
        )
        self.stdout.write(
            '💰 Cuotas Financieras: /api/administration/financial-fees/'
        )
