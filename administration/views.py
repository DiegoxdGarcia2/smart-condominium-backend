from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation, Vehicle, Pet, VisitorLog
from .serializers import (
    RoleSerializer, UserSerializer, ResidentialUnitSerializer, 
    AnnouncementSerializer, FinancialFeeSerializer, CommonAreaSerializer, 
    ReservationSerializer, VehicleSerializer, PetSerializer, VisitorLogSerializer
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


class VehicleViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los vehículos de los residentes"""
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar vehículos según el rol del usuario:
        - Residentes: solo ven sus propios vehículos
        - Administradores: ven todos los vehículos
        """
        user = self.request.user
        
        # Si es superuser o administrador, ver todos los vehículos
        if user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia']):
            return Vehicle.objects.select_related('resident').order_by('license_plate')
        
        # Si es residente, solo ver sus propios vehículos
        return Vehicle.objects.filter(resident=user).select_related('resident')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como propietario del vehículo"""
        # Siempre usar el usuario actual como propietario
        serializer.save(resident=self.request.user)


class PetViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las mascotas de los residentes"""
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar mascotas según el rol del usuario:
        - Residentes: solo ven sus propias mascotas
        - Administradores: ven todas las mascotas
        """
        user = self.request.user
        
        # Si es superuser o administrador, ver todas las mascotas
        if user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia']):
            return Pet.objects.select_related('resident').order_by('name')
        
        # Si es residente, solo ver sus propias mascotas
        return Pet.objects.filter(resident=user).select_related('resident')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como propietario de la mascota"""
        # Siempre usar el usuario actual como propietario
        serializer.save(resident=self.request.user)


class VisitorLogViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los registros de visitantes"""
    queryset = VisitorLog.objects.all()
    serializer_class = VisitorLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar registros de visitantes según el rol del usuario:
        - Residentes: solo ven visitantes que los han visitado
        - Administradores/Guardias: ven todos los registros
        """
        user = self.request.user
        
        # Si es superuser, administrador o guardia, ver todos los registros
        if user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia']):
            return VisitorLog.objects.select_related('resident').order_by('-entry_time')
        
        # Si es residente, solo ver sus propios visitantes
        return VisitorLog.objects.filter(resident=user).select_related('resident')
    
    @action(detail=True, methods=['post'])
    def register_exit(self, request, pk=None):
        """
        Endpoint personalizado para registrar la salida de un visitante
        """
        visitor_log = self.get_object()
        
        # Verificar que el visitante esté actualmente en el condominio
        if visitor_log.exit_time:
            return Response(
                {'error': 'Este visitante ya registró su salida'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Registrar la hora de salida
        from django.utils import timezone
        visitor_log.exit_time = timezone.now()
        visitor_log.status = 'Salió'
        visitor_log.save()
        
        serializer = self.get_serializer(visitor_log)
        return Response(
            {
                'message': 'Salida registrada exitosamente',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def active_visitors(self, request):
        """
        Endpoint para obtener solo los visitantes que están actualmente en el condominio
        Solo accesible para administradores y guardias
        """
        # Verificar permisos - solo admin y guardias
        user = request.user
        if not (user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia'])):
            return Response(
                {'error': 'No tiene permisos para acceder a esta información'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener visitantes activos (usar queryset completo para admin)
        if user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia']):
            active_visitors = VisitorLog.objects.select_related('resident').filter(
                exit_time__isnull=True, status='Activo'
            )
        else:
            active_visitors = self.get_queryset().filter(exit_time__isnull=True, status='Activo')
        
        serializer = self.get_serializer(active_visitors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def daily_report(self, request):
        """
        Endpoint para obtener un reporte diario de visitantes
        Solo accesible para administradores y guardias
        """
        from django.utils import timezone
        from datetime import datetime, time
        
        # Verificar permisos - solo admin y guardias
        user = request.user
        if not (user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia'])):
            return Response(
                {'error': 'No tiene permisos para acceder a este reporte'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener fecha de hoy
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, time.min))
        end_of_day = timezone.make_aware(datetime.combine(today, time.max))
        
        # Filtrar visitantes del día (usar queryset completo para admin)
        if user.is_superuser or (user.role and user.role.name in ['Administrador', 'Guardia']):
            daily_visitors = VisitorLog.objects.select_related('resident').filter(
                entry_time__range=(start_of_day, end_of_day)
            )
        else:
            daily_visitors = self.get_queryset().filter(
                entry_time__range=(start_of_day, end_of_day)
            )
        
        serializer = self.get_serializer(daily_visitors, many=True)
        
        # Estadísticas del día
        total_visitors = daily_visitors.count()
        active_visitors = daily_visitors.filter(exit_time__isnull=True).count()
        visitors_left = daily_visitors.filter(exit_time__isnull=False).count()
        
        return Response({
            'date': today.strftime('%d/%m/%Y'),
            'statistics': {
                'total_visitors': total_visitors,
                'active_visitors': active_visitors,
                'visitors_left': visitors_left
            },
            'visitors': serializer.data
        })
