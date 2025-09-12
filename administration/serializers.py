from rest_framework import serializers
from .models import Role, User, ResidentialUnit, Announcement, FinancialFee, CommonArea, Reservation


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
