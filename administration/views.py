from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation
from .serializers import (
    RoleSerializer, UserSerializer, ResidentialUnitSerializer, 
    AnnouncementSerializer, FinancialFeeSerializer, CommonAreaSerializer, 
    ReservationSerializer
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
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva cuota financiera con logs de debugging"""
        print(f"POST Data received: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Actualizar una cuota financiera con logs de debugging"""
        print(f"PUT Data received: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        return super().update(request, *args, **kwargs)


class CommonAreaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las áreas comunes"""
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas y ordenar por nombre"""
        return CommonArea.objects.order_by('name')


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las reservas de áreas comunes"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimizar consultas incluyendo área común y residente relacionados"""
        return Reservation.objects.select_related('common_area', 'resident').order_by('-start_time')
    
    def create(self, request, *args, **kwargs):
        """
        Crear una nueva reserva con validación de conflictos de horario
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extraer datos validados
        common_area = serializer.validated_data['common_area']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        
        # Validar que la fecha de fin sea posterior a la de inicio
        if end_time <= start_time:
            return Response(
                {'error': 'La fecha de fin debe ser posterior a la fecha de inicio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar conflictos con reservas confirmadas existentes
        conflicting_reservations = Reservation.objects.filter(
            common_area=common_area,
            status='Confirmada',
            # Verificar solapamiento de horarios
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if conflicting_reservations.exists():
            conflicting_reservation = conflicting_reservations.first()
            return Response(
                {
                    'error': 'Conflicto de horario detectado',
                    'details': f'El área "{common_area.name}" ya está reservada desde '
                              f'{conflicting_reservation.start_time.strftime("%d/%m/%Y %H:%M")} '
                              f'hasta {conflicting_reservation.end_time.strftime("%d/%m/%Y %H:%M")} '
                              f'por {conflicting_reservation.resident.get_full_name()}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Si no hay conflictos, crear la reserva
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
