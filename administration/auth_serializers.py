"""
Serializadores personalizados para autenticación
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from administration.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado que maneja la autenticación con email
    """
    username_field = User.USERNAME_FIELD  # Usará 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reemplazar el campo 'username' por 'email'
        self.fields[self.username_field] = self.fields.pop('username')
    
    def validate(self, attrs):
        """
        Validación personalizada que usa email en lugar de username
        """
        # Obtener el email y password de los datos recibidos
        credential = attrs.get(self.username_field)  # email
        password = attrs.get("password")
        
        if credential and password:
            # Autenticar usando email
            user = authenticate(
                request=self.context.get('request'),
                username=credential,  # Django auth backend espera 'username' pero usará USERNAME_FIELD
                password=password
            )
            
            if not user:
                # Si falla la autenticación estándar, intentar directamente
                try:
                    user = User.objects.get(email=credential)
                    if not user.check_password(password):
                        user = None
                except User.DoesNotExist:
                    user = None
            
            if not user:
                raise serializers.ValidationError(
                    'No se puede iniciar sesión con las credenciales proporcionadas.'
                )
                
            if not user.is_active:
                raise serializers.ValidationError(
                    'La cuenta de usuario está deshabilitada.'
                )
        else:
            raise serializers.ValidationError(
                'Debe incluir "email" y "password".'
            )
        
        # Configurar para el serializador padre
        attrs['username'] = credential  # Para compatibilidad con TokenObtainPairSerializer
        
        # Llamar al método padre para generar los tokens
        data = super().validate(attrs)
        
        return data