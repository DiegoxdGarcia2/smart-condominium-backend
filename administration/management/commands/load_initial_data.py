"""
Comando personalizado para cargar datos iniciales en la base de datos.
Ejecutar con: python manage.py load_initial_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from administration.models import Role, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation, Vehicle, Pet, VisitorLog, Task, Feedback, PaymentTransaction

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
        
        # Crear áreas comunes
        self.stdout.write('\n=== CREANDO ÁREAS COMUNES ===')
        
        common_areas_data = [
            {
                'name': 'Salón de Eventos',
                'description': 'Amplio salón para celebraciones y eventos sociales con capacidad para 50 personas',
                'capacity': 50,
                'booking_price': Decimal('300.00')
            },
            {
                'name': 'Piscina',
                'description': 'Piscina comunitaria con área recreativa',
                'capacity': 30,
                'booking_price': Decimal('150.00')
            },
            {
                'name': 'Cancha de Tenis',
                'description': 'Cancha de tenis profesional iluminada',
                'capacity': 4,
                'booking_price': Decimal('100.00')
            },
            {
                'name': 'Gimnasio',
                'description': 'Gimnasio equipado con máquinas de ejercicio',
                'capacity': 15,
                'booking_price': Decimal('50.00')
            },
            {
                'name': 'Terraza BBQ',
                'description': 'Terraza con parrillas y mesas para asados familiares',
                'capacity': 20,
                'booking_price': Decimal('120.00')
            }
        ]
        
        for area_data in common_areas_data:
            area, created = CommonArea.objects.get_or_create(
                name=area_data['name'],
                defaults=area_data
            )
            if created:
                self.stdout.write(f'✓ Área común creada: {area.name} (${area.booking_price})')
            else:
                self.stdout.write(f'- Área común ya existe: {area.name}')
        
        # Crear algunas reservas de ejemplo
        self.stdout.write('\n=== CREANDO RESERVAS DE EJEMPLO ===')
        
        # Obtener usuarios y áreas para las reservas
        juan = User.objects.filter(email='juan.perez@email.com').first()
        ana = User.objects.filter(email='ana.garcia@email.com').first()
        salon = CommonArea.objects.filter(name='Salón de Eventos').first()
        piscina = CommonArea.objects.filter(name='Piscina').first()
        
        if juan and ana and salon and piscina:
            reservations_data = [
                {
                    'common_area': salon,
                    'resident': juan,
                    'start_time': timezone.now() + timedelta(days=7, hours=18),
                    'end_time': timezone.now() + timedelta(days=7, hours=23),
                    'status': 'Confirmada',
                    'total_paid': salon.booking_price
                },
                {
                    'common_area': piscina,
                    'resident': ana,
                    'start_time': timezone.now() + timedelta(days=3, hours=10),
                    'end_time': timezone.now() + timedelta(days=3, hours=14),
                    'status': 'Pendiente',
                    'total_paid': piscina.booking_price
                }
            ]
            
            for reservation_data in reservations_data:
                reservation, created = Reservation.objects.get_or_create(
                    common_area=reservation_data['common_area'],
                    resident=reservation_data['resident'],
                    start_time=reservation_data['start_time'],
                    defaults=reservation_data
                )
                if created:
                    self.stdout.write(
                        f'✓ Reserva creada: {reservation.common_area.name} - '
                        f'{reservation.resident.get_full_name()} ({reservation.status})'
                    )
                else:
                    self.stdout.write(
                        f'- Reserva ya existe: {reservation.common_area.name} - '
                        f'{reservation.resident.get_full_name()}'
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
        self.stdout.write(
            '🏊 Áreas Comunes: /api/administration/common-areas/'
        )
        self.stdout.write(
            '📅 Reservas: /api/administration/reservations/'
        )
        
        # NUEVOS DATOS DE LA FASE 4: VEHÍCULOS, MASCOTAS Y VISITANTES
        self.stdout.write('\n=== CREANDO VEHÍCULOS DE EJEMPLO ===')
        
        vehicles_data = [
            {
                'resident': juan,
                'license_plate': 'ABC-123',
                'brand': 'Toyota',
                'model': 'Corolla',
                'color': 'Blanco'
            },
            {
                'resident': juan,
                'license_plate': 'DEF-456',
                'brand': 'Honda',
                'model': 'Civic',
                'color': 'Gris'
            },
            {
                'resident': ana,
                'license_plate': 'GHI-789',
                'brand': 'Nissan',
                'model': 'Sentra',
                'color': 'Azul'
            },
            {
                'resident': ana,
                'license_plate': 'JKL-012',
                'brand': 'Mazda',
                'model': 'CX-5',
                'color': 'Rojo'
            }
        ]
        
        if juan and ana:
            for vehicle_data in vehicles_data:
                vehicle, created = Vehicle.objects.get_or_create(
                    license_plate=vehicle_data['license_plate'],
                    defaults=vehicle_data
                )
                if created:
                    self.stdout.write(
                        f'✓ Vehículo creado: {vehicle.license_plate} - '
                        f'{vehicle.brand} {vehicle.model} ({vehicle.resident.get_full_name()})'
                    )
                else:
                    self.stdout.write(f'- Vehículo ya existe: {vehicle.license_plate}')
        
        # Crear mascotas de ejemplo
        self.stdout.write('\n=== CREANDO MASCOTAS DE EJEMPLO ===')
        
        pets_data = [
            {
                'resident': juan,
                'name': 'Buddy',
                'species': 'Perro',
                'breed': 'Labrador',
                'age': 3
            },
            {
                'resident': juan,
                'name': 'Miau',
                'species': 'Gato',
                'breed': 'Persa',
                'age': 2
            },
            {
                'resident': ana,
                'name': 'Rocky',
                'species': 'Perro',
                'breed': 'Pastor Alemán',
                'age': 5
            },
            {
                'resident': ana,
                'name': 'Luna',
                'species': 'Gato',
                'breed': 'Siames',
                'age': 1
            }
        ]
        
        if juan and ana:
            for pet_data in pets_data:
                pet, created = Pet.objects.get_or_create(
                    resident=pet_data['resident'],
                    name=pet_data['name'],
                    defaults=pet_data
                )
                if created:
                    self.stdout.write(
                        f'✓ Mascota creada: {pet.name} ({pet.species} - {pet.breed}) - '
                        f'Propietario: {pet.resident.get_full_name()}'
                    )
                else:
                    self.stdout.write(f'- Mascota ya existe: {pet.name}')
        
        # Crear registros de visitantes de ejemplo
        self.stdout.write('\n=== CREANDO REGISTROS DE VISITANTES ===')
        
        visitor_logs_data = [
            {
                'visitor_name': 'María Rodríguez',
                'visitor_dni': '12345678',
                'resident': juan,
                'entry_time': timezone.now() - timedelta(hours=2),
                'exit_time': None,  # Visitante activo
                'vehicle_license_plate': 'VIS-001',
                'observations': 'Visita familiar'
            },
            {
                'visitor_name': 'Carlos Mendoza',
                'visitor_dni': '87654321',
                'resident': ana,
                'entry_time': timezone.now() - timedelta(hours=4),
                'exit_time': timezone.now() - timedelta(hours=1),  # Ya salió
                'vehicle_license_plate': 'VIS-002',
                'observations': 'Técnico de mantenimiento'
            },
            {
                'visitor_name': 'Laura Jiménez',
                'visitor_dni': '11223344',
                'resident': juan,
                'entry_time': timezone.now() - timedelta(days=1, hours=3),
                'exit_time': timezone.now() - timedelta(days=1, hours=1),
                'vehicle_license_plate': None,
                'observations': 'Visita social'
            },
            {
                'visitor_name': 'Pedro Gómez',
                'visitor_dni': '55667788',
                'resident': ana,
                'entry_time': timezone.now() - timedelta(minutes=30),
                'exit_time': None,  # Visitante activo
                'vehicle_license_plate': None,
                'observations': 'Entrega de paquete'
            }
        ]
        
        if juan and ana:
            for visitor_data in visitor_logs_data:
                visitor_log, created = VisitorLog.objects.get_or_create(
                    visitor_dni=visitor_data['visitor_dni'],
                    resident=visitor_data['resident'],
                    entry_time=visitor_data['entry_time'],
                    defaults=visitor_data
                )
                if created:
                    status = "Activo" if not visitor_data['exit_time'] else "Salió"
                    self.stdout.write(
                        f'✓ Registro creado: {visitor_log.visitor_name} visitando a '
                        f'{visitor_log.resident.get_full_name()} - {status}'
                    )
                else:
                    self.stdout.write(f'- Registro ya existe: {visitor_data["visitor_name"]}')
        
        self.stdout.write(
            '\n🎉 ¡FASE 4 COMPLETADA! Nuevos endpoints disponibles:'
        )
        self.stdout.write(
            '🚗 Vehículos: /api/administration/vehicles/'
        )
        self.stdout.write(
            '🐕 Mascotas: /api/administration/pets/'
        )
        self.stdout.write(
            '👥 Visitantes: /api/administration/visitor-logs/'
        )
        self.stdout.write(
            '\n📊 Endpoints especiales de visitantes:'
        )
        self.stdout.write(
            '  - Visitantes activos: /api/administration/visitor-logs/active_visitors/'
        )
        self.stdout.write(
            '  - Reporte diario: /api/administration/visitor-logs/daily_report/'
        )
        self.stdout.write(
            '  - Registrar salida: POST /api/administration/visitor-logs/{id}/register_exit/'
        )
        
        # Crear tareas de ejemplo
        self.stdout.write('\n--- CREANDO TAREAS DE EJEMPLO ---')
        tasks_data = [
            {
                'title': 'Revisión mensual de aires acondicionados',
                'description': 'Realizar mantenimiento preventivo de todos los sistemas de aire acondicionado del condominio',
                'status': 'Pendiente',
                'assigned_to': User.objects.get(email='carlos.seguridad@email.com'),
                'created_by': User.objects.get(email='admin@smartcondo.com')
            },
            {
                'title': 'Reparación de puerta del gimnasio',
                'description': 'La puerta del gimnasio no cierra correctamente, revisar bisagras y cerradura',
                'status': 'En Progreso',
                'assigned_to': User.objects.get(email='carlos.seguridad@email.com'),
                'created_by': User.objects.get(email='juan.perez@email.com')
            },
            {
                'title': 'Instalación de nueva cámara en lobby',
                'description': 'Instalar cámara de seguridad adicional en el área del lobby principal',
                'status': 'Completada',
                'assigned_to': User.objects.get(email='carlos.seguridad@email.com'),
                'created_by': User.objects.get(email='admin@smartcondo.com'),
                'completed_at': timezone.now() - timedelta(days=2)
            },
            {
                'title': 'Limpieza de filtros de la piscina',
                'description': 'Limpieza semanal de filtros y verificación de niveles de cloro',
                'status': 'Pendiente',
                'assigned_to': User.objects.get(email='carlos.seguridad@email.com'),
                'created_by': User.objects.get(email='admin@smartcondo.com')
            }
        ]
        
        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                self.stdout.write(f'✓ Tarea creada: {task.title}')
            else:
                self.stdout.write(f'- Tarea ya existe: {task.title}')
        
        # Crear feedback de ejemplo
        self.stdout.write('\n--- CREANDO FEEDBACK DE EJEMPLO ---')
        feedback_data = [
            {
                'subject': 'Problema con el ascensor',
                'message': 'El ascensor principal ha estado haciendo ruidos extraños y se detiene de manera irregular entre los pisos 3 y 4.',
                'resident': User.objects.get(email='juan.perez@email.com'),
                'status': 'Pendiente'
            },
            {
                'subject': 'Sugerencia para mejora del gimnasio',
                'message': 'Sería excelente si pudieran agregar más equipos cardiovasculares, especialmente caminadoras, ya que las actuales están muy ocupadas.',
                'resident': User.objects.get(email='ana.garcia@email.com'),
                'status': 'En Revisión'
            },
            {
                'subject': 'Ruido en el piso superior',
                'message': 'Los vecinos del piso de arriba están haciendo mucho ruido durante las noches, especialmente después de las 10 PM.',
                'resident': User.objects.get(email='juan.perez@email.com'),
                'status': 'Respondido'
            },
            {
                'subject': 'Agradecimiento por la limpieza',
                'message': 'Quiero felicitar al equipo de limpieza por el excelente trabajo que han estado haciendo en las áreas comunes.',
                'resident': User.objects.get(email='ana.garcia@email.com'),
                'status': 'Cerrado'
            },
            {
                'subject': 'Problema con el estacionamiento',
                'message': 'Hay vehículos que no tienen permiso ocupando los espacios de visitantes durante todo el día.',
                'resident': User.objects.get(email='juan.perez@email.com'),
                'status': 'En Revisión'
            }
        ]
        
        for feedback_info in feedback_data:
            feedback, created = Feedback.objects.get_or_create(
                subject=feedback_info['subject'],
                resident=feedback_info['resident'],
                defaults=feedback_info
            )
            if created:
                self.stdout.write(f'✓ Feedback creado: {feedback.subject}')
            else:
                self.stdout.write(f'- Feedback ya existe: {feedback.subject}')
        
        # Crear transacciones de pago de ejemplo
        self.stdout.write('\n--- CREANDO TRANSACCIONES DE PAGO DE EJEMPLO ---')
        
        # Obtener algunas cuotas financieras para asignar a las transacciones
        financial_fees = FinancialFee.objects.all()[:3]
        residents = User.objects.filter(role=resident_role)[:4]
        
        payment_data = [
            {
                'financial_fee': financial_fees[0],
                'resident': residents[0],
                'amount': financial_fees[0].amount,
                'status': 'Completado',
                'payment_method': 'Tarjeta de Crédito',
                'gateway_response': {'payment_id': 'pay_12345', 'status': 'approved'},
                'processed_at': timezone.now() - timedelta(days=5)
            },
            {
                'financial_fee': financial_fees[1] if len(financial_fees) > 1 else financial_fees[0],
                'resident': residents[1] if len(residents) > 1 else residents[0],
                'amount': financial_fees[1].amount if len(financial_fees) > 1 else financial_fees[0].amount,
                'status': 'Pendiente',
                'payment_method': '',
                'gateway_response': {}
            },
            {
                'financial_fee': financial_fees[0],
                'resident': residents[2] if len(residents) > 2 else residents[0],
                'amount': financial_fees[0].amount,
                'status': 'Fallido',
                'payment_method': 'Transferencia Bancaria',
                'gateway_response': {'error': 'insufficient_funds', 'status': 'failed'},
                'processed_at': timezone.now() - timedelta(days=1)
            },
            {
                'financial_fee': financial_fees[2] if len(financial_fees) > 2 else financial_fees[0],
                'resident': residents[3] if len(residents) > 3 else residents[0],
                'amount': financial_fees[2].amount if len(financial_fees) > 2 else financial_fees[0].amount,
                'status': 'Procesando',
                'payment_method': 'PayPal',
                'gateway_response': {'payment_id': 'pay_67890', 'status': 'processing'}
            }
        ]
        
        for payment_info in payment_data:
            # Crear transacción única por resident y financial_fee con el status específico
            transaction, created = PaymentTransaction.objects.get_or_create(
                financial_fee=payment_info['financial_fee'],
                resident=payment_info['resident'],
                status=payment_info['status'],
                defaults=payment_info
            )
            if created:
                self.stdout.write(f'✓ Transacción creada: {transaction.transaction_id} - {transaction.status}')
            else:
                self.stdout.write(f'- Transacción ya existe: {transaction.transaction_id}')
        
        # Información de nuevos endpoints de Fase 5
        self.stdout.write('\n=== NUEVOS ENDPOINTS DE FASE 5 ===')
        self.stdout.write('🔧 GESTIÓN DE TAREAS:')
        self.stdout.write('  - Listar tareas: GET /api/administration/tasks/')
        self.stdout.write('  - Crear tarea: POST /api/administration/tasks/')
        self.stdout.write('  - Mis tareas: /api/administration/tasks/my_tasks/')
        self.stdout.write('  - Actualizar estado: PATCH /api/administration/tasks/{id}/update_status/')
        
        self.stdout.write('\n💬 SISTEMA DE FEEDBACK:')
        self.stdout.write('  - Listar feedback: GET /api/administration/feedback/')
        self.stdout.write('  - Crear feedback: POST /api/administration/feedback/')
        self.stdout.write('  - Mi feedback: /api/administration/feedback/my_feedback/')
        self.stdout.write('  - Dashboard admin: /api/administration/feedback/admin_dashboard/')
        
        self.stdout.write('\n💳 GATEWAY DE PAGOS:')
        self.stdout.write('  - Listar transacciones: GET /api/administration/payments/')
        self.stdout.write('  - Iniciar pago: POST /api/administration/payments/initiate_payment/')
        self.stdout.write('  - Webhook: POST /api/administration/payments/payment_webhook/')
        self.stdout.write('  - Mis pagos: /api/administration/payments/my_payments/')
