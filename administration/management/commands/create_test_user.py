from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a test user for authentication testing'
    
    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='User email', default='test@test.com')
        parser.add_argument('--password', type=str, help='User password', default='test123')
        parser.add_argument('--username', type=str, help='Username (optional)', default='testuser')
    
    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        username = options['username']
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists')
            )
            return
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
            first_name='Test',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user: {email}')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')