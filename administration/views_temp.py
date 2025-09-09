from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee
from .serializers import (
    RoleSerializer, UserSerializer, ResidentialUnitSerializer, 
    AnnouncementSerializer, FinancialFeeSerializer
)


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los roles del sistema"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los usuarios del sistema"""
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas incluyendo el rol relacionado"""
        return User.objects.select_related('role').order_by('date_joined')
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint para obtener los datos del usuario actualmente autenticado.
        
        Returns:
            Response: Datos del usuario actual serializados
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ResidentialUnitViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las unidades residenciales"""
    queryset = ResidentialUnit.objects.all()
    serializer_class = ResidentialUnitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas incluyendo el propietario relacionado"""
        return ResidentialUnit.objects.select_related('owner').order_by('unit_number')


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los comunicados del condominio"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas incluyendo el autor relacionado"""
        return Announcement.objects.select_related('author').order_by('-created_at')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como autor"""
        serializer.save(author=self.request.user)


class FinancialFeeViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las cuotas financieras del condominio"""
    queryset = FinancialFee.objects.all()
    serializer_class = FinancialFeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas incluyendo la unidad y propietario relacionados"""
        return FinancialFee.objects.select_related('unit', 'unit__owner').order_by('-due_date')
