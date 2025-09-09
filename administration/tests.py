from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, ResidentialUnit

User = get_user_model()


class RoleModelTest(TestCase):
    """Pruebas para el modelo Role"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Administrador")
    
    def test_role_creation(self):
        """Prueba la creación de un rol"""
        self.assertEqual(self.role.name, "Administrador")
        self.assertTrue(isinstance(self.role, Role))
        self.assertEqual(str(self.role), "Administrador")
    
    def test_role_unique_name(self):
        """Prueba que el nombre del rol sea único"""
        with self.assertRaises(Exception):
            Role.objects.create(name="Administrador")


class UserModelTest(TestCase):
    """Pruebas para el modelo User personalizado"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Residente")
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone_number="+52-555-0123",
            role=self.role
        )
    
    def test_user_creation(self):
        """Prueba la creación de un usuario"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone_number, "+52-555-0123")
        self.assertEqual(self.user.role, self.role)
        self.assertTrue(self.user.check_password("testpass123"))
    
    def test_user_string_representation(self):
        """Prueba la representación en string del usuario"""
        expected = "Test User (test@example.com)"
        self.assertEqual(str(self.user), expected)
    
    def test_email_as_username_field(self):
        """Prueba que el email sea el campo de username"""
        self.assertEqual(User.USERNAME_FIELD, 'email')
    
    def test_user_unique_email(self):
        """Prueba que el email sea único"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="anotheruser",
                email="test@example.com",
                password="testpass123"
            )


class ResidentialUnitModelTest(TestCase):
    """Pruebas para el modelo ResidentialUnit"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Residente")
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="testpass123",
            role=self.role
        )
        self.unit = ResidentialUnit.objects.create(
            unit_number="A-101",
            type="Departamento",
            floor=1,
            owner=self.user
        )
    
    def test_residential_unit_creation(self):
        """Prueba la creación de una unidad residencial"""
        self.assertEqual(self.unit.unit_number, "A-101")
        self.assertEqual(self.unit.type, "Departamento")
        self.assertEqual(self.unit.floor, 1)
        self.assertEqual(self.unit.owner, self.user)
    
    def test_residential_unit_string_representation(self):
        """Prueba la representación en string de la unidad"""
        expected = "Unidad A-101 - Departamento"
        self.assertEqual(str(self.unit), expected)
    
    def test_unit_without_owner(self):
        """Prueba crear una unidad sin propietario"""
        unit = ResidentialUnit.objects.create(
            unit_number="B-202",
            type="Casa",
            floor=None
        )
        self.assertIsNone(unit.owner)
        self.assertIsNone(unit.floor)
    
    def test_unit_unique_number(self):
        """Prueba que el número de unidad sea único"""
        with self.assertRaises(Exception):
            ResidentialUnit.objects.create(
                unit_number="A-101",
                type="Casa"
            )


class AuthenticationAPITest(APITestCase):
    """Pruebas para la autenticación JWT"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Residente")
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=self.role
        )
    
    def test_obtain_token(self):
        """Prueba obtener token JWT"""
        url = '/api/token/'
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_token_invalid_credentials(self):
        """Prueba obtener token con credenciales inválidas"""
        url = '/api/token/'
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_token(self):
        """Prueba refrescar token JWT"""
        refresh = RefreshToken.for_user(self.user)
        url = '/api/token/refresh/'
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class RoleAPITest(APITestCase):
    """Pruebas para la API de roles"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Administrador")
        self.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=self.role
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_roles_list(self):
        """Prueba obtener lista de roles"""
        url = '/api/administration/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_role(self):
        """Prueba crear un nuevo rol"""
        url = '/api/administration/roles/'
        data = {'name': 'Guardia'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)
    
    def test_unauthorized_access(self):
        """Prueba acceso no autorizado"""
        self.client.force_authenticate(user=None)
        url = '/api/administration/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAPITest(APITestCase):
    """Pruebas para la API de usuarios"""
    
    def setUp(self):
        self.role_admin = Role.objects.create(name="Administrador")
        self.role_resident = Role.objects.create(name="Residente")
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=self.role_admin
        )
        self.client.force_authenticate(user=self.admin_user)
    
    def test_get_users_list(self):
        """Prueba obtener lista de usuarios"""
        url = '/api/administration/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_user(self):
        """Prueba crear un nuevo usuario"""
        url = '/api/administration/users/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+52-555-0456',
            'role': self.role_resident.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        
        # Verificar que la contraseña no se devuelva en la respuesta
        self.assertNotIn('password', response.data)
    
    def test_user_serializer_role_name(self):
        """Prueba que el serializer incluya el nombre del rol"""
        url = f'/api/administration/users/{self.admin_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_name'], 'Administrador')


class ResidentialUnitAPITest(APITestCase):
    """Pruebas para la API de unidades residenciales"""
    
    def setUp(self):
        self.role = Role.objects.create(name="Administrador")
        self.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=self.role
        )
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="testpass123",
            role=self.role
        )
        self.unit = ResidentialUnit.objects.create(
            unit_number="A-101",
            type="Departamento",
            floor=1,
            owner=self.owner
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_units_list(self):
        """Prueba obtener lista de unidades residenciales"""
        url = '/api/administration/residential-units/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_unit(self):
        """Prueba crear una nueva unidad residencial"""
        url = '/api/administration/residential-units/'
        data = {
            'unit_number': 'B-202',
            'type': 'Casa',
            'floor': 2,
            'owner': self.owner.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ResidentialUnit.objects.count(), 2)
    
    def test_unit_serializer_owner_info(self):
        """Prueba que el serializer incluya información del propietario"""
        url = f'/api/administration/residential-units/{self.unit.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('owner_name', response.data)
        self.assertIn('owner_email', response.data)


class UserMeEndpointTest(APITestCase):
    """Pruebas para el endpoint /api/administration/users/me/"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear rol
        self.role = Role.objects.create(name='Residente')
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@email.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone_number='555-0123',
            role=self.role
        )
        
    def test_me_endpoint_authenticated(self):
        """Prueba que el endpoint /me/ funciona para usuarios autenticados"""
        # Autenticar usuario
        self.client.force_authenticate(user=self.user)
        
        # Hacer petición al endpoint /me/
        url = '/api/administration/users/me/'
        response = self.client.get(url)
        
        # Verificar respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)
        self.assertEqual(response.data['role'], self.role.id)
        self.assertEqual(response.data['role_name'], self.role.name)
        
    def test_me_endpoint_unauthenticated(self):
        """Prueba que el endpoint /me/ requiere autenticación"""
        url = '/api/administration/users/me/'
        response = self.client.get(url)
        
        # Verificar que retorna 401 sin autenticación
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_me_endpoint_returns_current_user_only(self):
        """Prueba que el endpoint /me/ solo retorna datos del usuario autenticado"""
        # Crear otro usuario
        other_role = Role.objects.create(name='Admin')
        other_user = User.objects.create_user(
            username='otheruser',
            email='other.user@email.com',
            password='otherpass123',
            first_name='Other',
            last_name='User',
            role=other_role
        )
        
        # Autenticar con el primer usuario
        self.client.force_authenticate(user=self.user)
        
        # Hacer petición al endpoint /me/
        url = '/api/administration/users/me/'
        response = self.client.get(url)
        
        # Verificar que retorna datos del usuario autenticado, no del otro usuario
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], 'test.user@email.com')
        self.assertNotEqual(response.data['id'], other_user.id)
        self.assertNotEqual(response.data['email'], 'other.user@email.com')
