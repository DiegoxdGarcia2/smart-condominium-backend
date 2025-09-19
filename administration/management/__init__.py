"""
Management command para crear un usuario de prueba
"""
from django.core.management.base import BaseCommand
from administration.models import User, Role


class Command(BaseCommand):
    help = 'Crear usuario de prueba para testing'
    
    def handle(self, *args, **options):
        # Crear rol admin si no existe
        admin_role, created = Role.objects.get_or_create(name='Administrador')
        if created:
            self.stdout.write('✅ Rol Administrador creado')
        
        # Crear usuario de prueba
        email = "admin@smartcondo.com"
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'⚠️ Usuario {email} ya existe')
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                password="admin123",
                first_name="Admin",
                last_name="Test",
                role=admin_role,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'✅ Usuario {email} creado')
        
        self.stdout.write(f'🔑 Credenciales: {email} / admin123')
