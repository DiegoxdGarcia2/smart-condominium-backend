from rest_framework import serializers
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation, Vehicle, Pet, VisitorLog, Task, Feedback, PaymentTransaction


class RoleSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Role"""
    
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User personalizado"""
    password = serializers.CharField(write_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'role_name', 'password', 
            'is_active', 'date_joined'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        """Crear un nuevo usuario con contraseña hasheada"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Actualizar usuario, manejando la contraseña si se proporciona"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class ResidentialUnitSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ResidentialUnit"""
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    
    class Meta:
        model = ResidentialUnit
        fields = [
            'id', 'unit_number', 'type', 'floor', 'owner', 
            'owner_name', 'owner_email'
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Announcement"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'author', 'author_name', 
            'author_email', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        """Crear un nuevo comunicado asignando automáticamente el autor"""
        # Si no se especifica autor, usar el usuario actual de la request
        request = self.context.get('request')
        if request and not validated_data.get('author'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class FinancialFeeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo FinancialFee"""
    unit_number = serializers.CharField(source='unit.unit_number', read_only=True)
    unit_owner = serializers.CharField(source='unit.owner.get_full_name', read_only=True)
    
    class Meta:
        model = FinancialFee
        fields = [
            'id', 'unit', 'unit_number', 'unit_owner', 'description', 
            'amount', 'due_date', 'status', 'created_at'
        ]
        read_only_fields = ['created_at']


class CommonAreaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo CommonArea"""
    
    class Meta:
        model = CommonArea
        fields = ['id', 'name', 'description', 'capacity', 'booking_price']


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Reservation"""
    common_area_name = serializers.CharField(source='common_area.name', read_only=True)
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    resident_email = serializers.CharField(source='resident.email', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'common_area', 'common_area_name', 'resident', 
            'resident_name', 'resident_email', 'start_time', 'end_time', 
            'status', 'total_paid', 'created_at'
        ]
        read_only_fields = ['created_at']


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Vehicle"""
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    resident_email = serializers.CharField(source='resident.email', read_only=True)
    unit_number = serializers.CharField(source='resident.residentialunit_set.first.unit_number', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'resident', 'resident_name', 'resident_email', 'unit_number',
            'license_plate', 'brand', 'model', 'color', 'created_at'
        ]
        read_only_fields = ['created_at', 'resident']
    
    def validate_license_plate(self, value):
        """Validar formato de placa"""
        if len(value) < 6:
            raise serializers.ValidationError("La placa debe tener al menos 6 caracteres.")
        return value.upper()


class PetSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Pet"""
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    resident_email = serializers.CharField(source='resident.email', read_only=True)
    unit_number = serializers.CharField(source='resident.residentialunit_set.first.unit_number', read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            'id', 'resident', 'resident_name', 'resident_email', 'unit_number',
            'name', 'species', 'breed', 'age', 'created_at'
        ]
        read_only_fields = ['created_at', 'resident']
    
    def validate_age(self, value):
        """Validar que la edad sea razonable"""
        if value is not None and (value < 0 or value > 30):
            raise serializers.ValidationError("La edad debe estar entre 0 y 30 años.")
        return value


class VisitorLogSerializer(serializers.ModelSerializer):
    """Serializer para el modelo VisitorLog"""
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    resident_email = serializers.CharField(source='resident.email', read_only=True)
    unit_number = serializers.CharField(source='resident.residentialunit_set.first.unit_number', read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = VisitorLog
        fields = [
            'id', 'visitor_name', 'visitor_dni', 'resident', 'resident_name', 
            'resident_email', 'unit_number', 'entry_time', 'exit_time', 
            'vehicle_license_plate', 'status', 'observations', 'duration_minutes'
        ]
        read_only_fields = ['entry_time', 'status']
    
    def get_duration_minutes(self, obj):
        """Calcular duración de la visita en minutos"""
        if obj.exit_time and obj.entry_time:
            delta = obj.exit_time - obj.entry_time
            return round(delta.total_seconds() / 60)
        return None
    
    def validate_visitor_dni(self, value):
        """Validar formato básico del DNI"""
        if len(value) < 7:
            raise serializers.ValidationError("El DNI debe tener al menos 7 caracteres.")
        return value
    
    def validate(self, data):
        """Validar que exit_time sea posterior a entry_time si se proporciona"""
        exit_time = data.get('exit_time')
        if exit_time and hasattr(self, 'instance') and self.instance:
            entry_time = self.instance.entry_time
            if exit_time <= entry_time:
                raise serializers.ValidationError(
                    "La hora de salida debe ser posterior a la hora de entrada."
                )
        return data


class TaskSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Task"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_name',
            'created_by', 'created_by_name', 'created_at', 'completed_at'
        ]
        read_only_fields = ['created_at', 'completed_at', 'created_by']
    
    def validate_assigned_to(self, value):
        """Validar que el usuario asignado existe y está activo"""
        if not value.is_active:
            raise serializers.ValidationError("No se puede asignar una tarea a un usuario inactivo.")
        return value


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Feedback"""
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    resident = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'subject', 'message', 'resident', 'resident_name', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'resident']
    
    def validate_subject(self, value):
        """Validar que el asunto no esté vacío después de quitar espacios"""
        if not value.strip():
            raise serializers.ValidationError("El asunto no puede estar vacío.")
        return value
    
    def validate_message(self, value):
        """Validar que el mensaje tenga contenido útil"""
        if not value.strip():
            raise serializers.ValidationError("El mensaje no puede estar vacío.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return value


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo PaymentTransaction"""
    resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
    fee_description = serializers.CharField(source='financial_fee.description', read_only=True)
    fee_amount = serializers.DecimalField(source='financial_fee.amount', max_digits=10, decimal_places=2, read_only=True)
    resident = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'financial_fee', 'fee_description', 'fee_amount', 'resident', 'resident_name',
            'transaction_id', 'amount', 'status', 'payment_method', 'gateway_response',
            'created_at', 'processed_at'
        ]
        read_only_fields = [
            'transaction_id', 'gateway_response', 'created_at', 'processed_at', 'resident'
        ]
    
    def validate_amount(self, value):
        """Validar que el monto sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value
    
    def validate_financial_fee(self, value):
        """Validar que la cuota financiera esté activa"""
        if not hasattr(value, 'is_active') or not value.is_active:
            raise serializers.ValidationError("No se puede procesar pago para una cuota inactiva.")
        return value
    
    def validate(self, data):
        """Validar coherencia entre financial_fee y amount"""
        financial_fee = data.get('financial_fee')
        amount = data.get('amount')
        
        if financial_fee and amount:
            if amount != financial_fee.amount:
                raise serializers.ValidationError({
                    'amount': f"El monto debe coincidir con el valor de la cuota: ${financial_fee.amount}"
                })
        return data
