from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create initial admin user for production'
    
    def handle(self, *args, **options):
        email = 'admin@smartcondo.com'
        password = 'SmartCondo2024!'
        username = 'admin'
        
        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Admin user with email {email} already exists')
                    )
                    return
                
                # Create superuser
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    username=username,
                    first_name='Admin',
                    last_name='System'
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created admin user: {email}')
                )
                self.stdout.write(f'Email: {email}')
                self.stdout.write(f'Username: {username}')
                self.stdout.write(f'Password: {password}')
                self.stdout.write(
                    self.style.WARNING('IMPORTANT: Change this password after first login!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )