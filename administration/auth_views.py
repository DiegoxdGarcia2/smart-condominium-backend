"""
Vistas personalizadas para autenticación JWT
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT usando email
    """
    serializer_class = CustomTokenObtainPairSerializer