"""
Backend de autenticación personalizado para Smart Condominium
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    """
    Backend de autenticación que permite login con email
    """
    
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        """
        Autentica usuarios usando email en lugar de username
        """
        # Si se proporciona email, usarlo; si no, usar username como email
        login_email = email or username
        
        if login_email is None or password is None:
            return None
            
        try:
            # Buscar usuario por email
            user = User.objects.get(email=login_email)
        except User.DoesNotExist:
            # Si no se encuentra por email, intentar por username (por compatibilidad)
            try:
                user = User.objects.get(username=login_email)
            except User.DoesNotExist:
                return None
        
        # Verificar contraseña
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Obtener usuario por ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None