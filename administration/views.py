from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import stripe
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation, Vehicle, Pet, VisitorLog, Task, Feedback, PaymentTransaction
from .serializers import (
    RoleSerializer, UserSerializer, ResidentialUnitSerializer, 
    AnnouncementSerializer, FinancialFeeSerializer, CommonAreaSerializer, 
    ReservationSerializer, VehicleSerializer, PetSerializer, VisitorLogSerializer,
    TaskSerializer, FeedbackSerializer, PaymentTransactionSerializer
)

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


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


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar el sistema de tareas"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar tareas según el rol del usuario"""
        user = self.request.user
        
        # Administradores ven todas las tareas
        if user.is_superuser or (user.role and user.role.name == 'Administrador'):
            return Task.objects.select_related('assigned_to', 'created_by').order_by('-created_at')
        
        # Usuarios normales solo ven tareas asignadas a ellos o creadas por ellos
        return Task.objects.select_related('assigned_to', 'created_by').filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como created_by"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Obtener todas las tareas asignadas al usuario actual"""
        user = request.user
        tasks = Task.objects.select_related('created_by').filter(assigned_to=user)
        serializer = self.get_serializer(tasks, many=True)
        
        # Estadísticas de tareas del usuario
        pending = tasks.filter(status='Pendiente').count()
        in_progress = tasks.filter(status='En Progreso').count()
        completed = tasks.filter(status='Completada').count()
        
        return Response({
            'statistics': {
                'pending': pending,
                'in_progress': in_progress,
                'completed': completed,
                'total': tasks.count()
            },
            'tasks': serializer.data
        })
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Actualizar solo el estado de una tarea"""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'El campo status es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que el status es válido
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Estado inválido. Opciones válidas: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar el sistema de feedback"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar feedback según el rol del usuario"""
        user = self.request.user
        
        # Administradores ven todos los feedbacks
        if user.is_superuser or (user.role and user.role.name == 'Administrador'):
            return Feedback.objects.select_related('resident').order_by('-created_at')
        
        # Usuarios normales solo ven sus propios feedbacks
        return Feedback.objects.filter(resident=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como resident"""
        serializer.save(resident=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_feedback(self, request):
        """Obtener todos los feedbacks del usuario actual"""
        user = request.user
        feedbacks = Feedback.objects.filter(resident=user).order_by('-created_at')
        serializer = self.get_serializer(feedbacks, many=True)
        
        # Estadísticas de feedback del usuario
        pending = feedbacks.filter(status='Pendiente').count()
        in_review = feedbacks.filter(status='En Revisión').count()
        responded = feedbacks.filter(status='Respondido').count()
        closed = feedbacks.filter(status='Cerrado').count()
        
        return Response({
            'statistics': {
                'pending': pending,
                'in_review': in_review,
                'responded': responded,
                'closed': closed,
                'total': feedbacks.count()
            },
            'feedbacks': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def admin_dashboard(self, request):
        """Dashboard de administración para feedback (solo admins)"""
        user = request.user
        
        # Verificar permisos de administrador
        if not (user.is_superuser or (user.role and user.role.name == 'Administrador')):
            return Response(
                {'error': 'No tienes permisos para acceder a este endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener estadísticas generales
        all_feedbacks = Feedback.objects.all()
        pending = all_feedbacks.filter(status='Pendiente').count()
        in_review = all_feedbacks.filter(status='En Revisión').count()
        responded = all_feedbacks.filter(status='Respondido').count()
        closed = all_feedbacks.filter(status='Cerrado').count()
        
        # Feedbacks más recientes pendientes
        recent_pending = Feedback.objects.select_related('resident').filter(
            status='Pendiente'
        ).order_by('-created_at')[:5]
        
        recent_serializer = self.get_serializer(recent_pending, many=True)
        
        return Response({
            'statistics': {
                'pending': pending,
                'in_review': in_review,
                'responded': responded,
                'closed': closed,
                'total': all_feedbacks.count()
            },
            'recent_pending': recent_serializer.data
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar transacciones de pago"""
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar transacciones según el rol del usuario"""
        user = self.request.user
        
        # Administradores ven todas las transacciones
        if user.is_superuser or (user.role and user.role.name == 'Administrador'):
            return PaymentTransaction.objects.select_related(
                'resident', 'financial_fee'
            ).order_by('-created_at')
        
        # Usuarios normales solo ven sus propias transacciones
        return PaymentTransaction.objects.select_related(
            'financial_fee'
        ).filter(resident=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como resident"""
        serializer.save(resident=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        """Iniciar un nuevo proceso de pago con Stripe Checkout"""
        financial_fee_id = request.data.get('financial_fee_id')
        
        if not financial_fee_id:
            return Response(
                {'error': 'financial_fee_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            financial_fee = FinancialFee.objects.get(id=financial_fee_id)
        except FinancialFee.DoesNotExist:
            return Response(
                {'error': 'Cuota financiera no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar si ya existe una transacción pendiente para esta cuota
        existing_transaction = PaymentTransaction.objects.filter(
            financial_fee=financial_fee,
            resident=request.user,
            status__in=['Pendiente', 'Procesando']
        ).first()
        
        if existing_transaction:
            # En lugar de devolver un 400, devolver la URL/ID de la sesión existente
            gw = existing_transaction.gateway_response or {}
            # Intentar obtener la URL completa guardada en gateway_response
            payment_url = (gw.get('stripe_session_url') or 
                          getattr(existing_transaction, 'payment_url', None))
            
            # Si no tenemos la URL completa, intentar recuperarla de Stripe usando session_id
            if not payment_url:
                session_id = gw.get('stripe_session_id') or existing_transaction.transaction_id
                if session_id:
                    try:
                        # Recuperar sesión completa de Stripe para obtener la URL correcta
                        session = stripe.checkout.Session.retrieve(session_id)
                        payment_url = session.url
                        # Actualizar gateway_response para futuras referencias
                        gw['stripe_session_url'] = session.url
                        existing_transaction.gateway_response = gw
                        existing_transaction.save()
                    except stripe.error.StripeError as e:
                        logger.warning("Could not retrieve Stripe session %s: %s", session_id, str(e))
            
            if payment_url:
                logger.info(f"Existing payment transaction for fee %s user %s -> session_id=%s, url=%s", financial_fee_id, request.user.id, gw.get('stripe_session_id'), payment_url)
                return Response({
                    'payment_url': payment_url,
                    'transaction_id': existing_transaction.transaction_id,
                    'existing': True
                }, status=status.HTTP_201_CREATED)

            # Si no se puede construir una URL, retornar el error original (logear para debugging)
            logger.warning("Existing transaction found for fee %s but no session_id/payment_url present; transaction_id=%s", financial_fee_id, existing_transaction.transaction_id)
            return Response(
                {'error': 'Ya existe una transacción pendiente para esta cuota'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Convertir el monto a centavos para Stripe
            amount_in_cents = int(financial_fee.amount * 100)
            
            # Crear sesión de Stripe Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': financial_fee.description,
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{settings.FRONTEND_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{settings.FRONTEND_URL}/payment-cancel',
                metadata={
                    'financial_fee_id': str(financial_fee_id),
                    'resident_id': str(request.user.id),
                }
            )
            
            # Crear nueva transacción con el session_id de Stripe
            logger.info("Creating new Stripe session for fee %s user %s session.id=%s", financial_fee_id, request.user.id, session.id)
            transaction = PaymentTransaction.objects.create(
                financial_fee=financial_fee,
                resident=request.user,
                amount=financial_fee.amount,
                status='Pendiente',
                transaction_id=session.id,
                gateway_response={
                    'stripe_session_id': session.id,
                    'stripe_session_url': session.url  # Guardar la URL completa para reutilizar
                }
            )
            logger.info("Created PaymentTransaction id=%s for fee %s user %s", transaction.id, financial_fee_id, request.user.id)

            return Response({
                'payment_url': session.url,
                'transaction_id': transaction.transaction_id
            }, status=status.HTTP_201_CREATED)
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': f'Error de Stripe: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error interno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def payment_webhook(self, request):
        """Webhook para recibir notificaciones de Stripe"""
        import json
        
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        
        if not endpoint_secret:
            return Response(
                {'error': 'STRIPE_WEBHOOK_SECRET no configurado'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            # Verificar la firma del webhook
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return Response(
                {'error': 'Payload inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except stripe.error.SignatureVerificationError:
            return Response(
                {'error': 'Firma inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Procesar el evento
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # Extraer metadata
            financial_fee_id = session['metadata'].get('financial_fee_id')
            resident_id = session['metadata'].get('resident_id')
            
            if not financial_fee_id or not resident_id:
                return Response(
                    {'error': 'Metadata incompleta en la sesión'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Buscar la transacción por session_id
                transaction = PaymentTransaction.objects.get(
                    transaction_id=session['id']
                )
                
                # Verificar que la FinancialFee existe
                financial_fee = FinancialFee.objects.get(id=financial_fee_id)
                
                # Actualizar transacción
                transaction.status = 'Completado'
                transaction.processed_at = timezone.now()
                transaction.gateway_response = {
                    'stripe_payment_status': session['payment_status'],
                    'stripe_payment_intent': session.get('payment_intent'),
                    'amount_total': session['amount_total']
                }
                transaction.save()
                
                # Actualizar el estado de la cuota financiera a 'Pagado'
                financial_fee.status = 'Pagado'
                financial_fee.save()
                
                return Response({
                    'message': 'Pago procesado exitosamente',
                    'transaction_id': transaction.transaction_id
                })
                
            except PaymentTransaction.DoesNotExist:
                return Response(
                    {'error': 'Transacción no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except FinancialFee.DoesNotExist:
                return Response(
                    {'error': 'Cuota financiera no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif event['type'] == 'checkout.session.expired':
            session = event['data']['object']
            
            try:
                # Buscar la transacción y marcarla como fallida
                transaction = PaymentTransaction.objects.get(
                    transaction_id=session['id']
                )
                transaction.status = 'Fallido'
                transaction.processed_at = timezone.now()
                transaction.gateway_response = {
                    'stripe_status': 'session_expired',
                    'reason': 'Sesión de pago expirada'
                }
                transaction.save()
                
                return Response({
                    'message': 'Sesión expirada procesada',
                    'transaction_id': transaction.transaction_id
                })
                
            except PaymentTransaction.DoesNotExist:
                return Response(
                    {'error': 'Transacción no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Para otros tipos de eventos, simplemente devolver OK
        return Response({'message': 'Evento recibido'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """Obtener todas las transacciones del usuario actual"""
        user = request.user
        transactions = PaymentTransaction.objects.select_related(
            'financial_fee'
        ).filter(resident=user).order_by('-created_at')
        
        serializer = self.get_serializer(transactions, many=True)
        
        # Estadísticas de pagos del usuario
        pending = transactions.filter(status='Pendiente').count()
        processing = transactions.filter(status='Procesando').count()
        completed = transactions.filter(status='Completado').count()
        failed = transactions.filter(status='Fallido').count()
        
        return Response({
            'statistics': {
                'pending': pending,
                'processing': processing,
                'completed': completed,
                'failed': failed,
                'total': transactions.count()
            },
            'transactions': serializer.data
        })
