from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class Role(models.Model):
    """Modelo para los roles de usuario en el sistema"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del rol")
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        
    def __str__(self):
        return self.name


class User(AbstractUser):
    """Modelo de usuario personalizado que usa email como campo de login"""
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Número de teléfono")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rol")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class ResidentialUnit(models.Model):
    """Modelo para las unidades residenciales del condominio"""
    
    UNIT_TYPE_CHOICES = [
        ('Departamento', 'Departamento'),
        ('Casa', 'Casa'),
    ]
    
    unit_number = models.CharField(max_length=20, unique=True, verbose_name="Número de unidad")
    type = models.CharField(
        max_length=20, 
        choices=UNIT_TYPE_CHOICES, 
        verbose_name="Tipo de unidad"
    )
    floor = models.IntegerField(null=True, blank=True, verbose_name="Piso")
    owner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Propietario"
    )
    
    class Meta:
        verbose_name = "Unidad Residencial"
        verbose_name_plural = "Unidades Residenciales"
        ordering = ['unit_number']
        
    def __str__(self):
        return f"Unidad {self.unit_number} - {self.type}"


class Announcement(models.Model):
    """Modelo para los comunicados del condominio"""
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Autor"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Comunicado"
        verbose_name_plural = "Comunicados"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.author.get_full_name()}"


class FinancialFee(models.Model):
    """Modelo para las cuotas financieras del condominio"""
    
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Vencido', 'Vencido'),
    ]
    
    unit = models.ForeignKey(
        ResidentialUnit, 
        on_delete=models.CASCADE, 
        verbose_name="Unidad"
    )
    description = models.CharField(max_length=200, verbose_name="Descripción")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Monto"
    )
    due_date = models.DateField(verbose_name="Fecha de vencimiento")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pendiente',
        verbose_name="Estado"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Cuota Financiera"
        verbose_name_plural = "Cuotas Financieras"
        ordering = ['-due_date']
        
    def __str__(self):
        return f"{self.description} - {self.unit.unit_number} - ${self.amount}"


class CommonArea(models.Model):
    """Modelo para las áreas comunes del condominio"""
    name = models.CharField(max_length=100, verbose_name="Nombre del área")
    description = models.TextField(blank=True, verbose_name="Descripción")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad de personas")
    booking_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio por reserva"
    )
    
    class Meta:
        verbose_name = "Área Común"
        verbose_name_plural = "Áreas Comunes"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} (Cap: {self.capacity})"


class Reservation(models.Model):
    """Modelo para las reservas de áreas comunes"""
    
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    common_area = models.ForeignKey(
        CommonArea,
        on_delete=models.CASCADE,
        verbose_name="Área común"
    )
    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Residente"
    )
    start_time = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    end_time = models.DateTimeField(verbose_name="Fecha y hora de fin")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendiente',
        verbose_name="Estado"
    )
    total_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto pagado"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.common_area.name} - {self.resident.get_full_name()} ({self.start_time.strftime('%d/%m/%Y %H:%M')})"


class Vehicle(models.Model):
    """Modelo para los vehículos de los residentes"""
    resident = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Propietario",
        related_name="vehicles"
    )
    license_plate = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Placa del vehículo"
    )
    brand = models.CharField(max_length=50, verbose_name="Marca")
    model = models.CharField(max_length=50, verbose_name="Modelo")
    color = models.CharField(max_length=30, verbose_name="Color")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['license_plate']
        
    def __str__(self):
        return f"{self.license_plate} - {self.brand} {self.model} ({self.resident.get_full_name()})"


class Pet(models.Model):
    """Modelo para las mascotas de los residentes"""
    
    SPECIES_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Pez', 'Pez'),
        ('Otro', 'Otro'),
    ]
    
    resident = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Propietario",
        related_name="pets"
    )
    name = models.CharField(max_length=50, verbose_name="Nombre de la mascota")
    species = models.CharField(
        max_length=20, 
        choices=SPECIES_CHOICES,
        verbose_name="Especie"
    )
    breed = models.CharField(max_length=50, verbose_name="Raza")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad (años)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.species}) - {self.resident.get_full_name()}"


class VisitorLog(models.Model):
    """Modelo para el registro de visitantes del condominio"""
    
    STATUS_CHOICES = [
        ('Activo', 'Activo'),  # Visitante dentro del condominio
        ('Salió', 'Salió'),   # Visitante que ya salió
    ]
    
    visitor_name = models.CharField(max_length=100, verbose_name="Nombre del visitante")
    visitor_dni = models.CharField(max_length=20, verbose_name="DNI/Identificación")
    resident = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Residente visitado",
        related_name="visitor_logs"
    )
    entry_time = models.DateTimeField(auto_now_add=True, verbose_name="Hora de entrada")
    exit_time = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Hora de salida"
    )
    vehicle_license_plate = models.CharField(
        max_length=10, 
        null=True, 
        blank=True, 
        verbose_name="Placa del vehículo"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Activo',
        verbose_name="Estado"
    )
    observations = models.TextField(
        blank=True, 
        verbose_name="Observaciones"
    )
    
    class Meta:
        verbose_name = "Registro de Visitante"
        verbose_name_plural = "Registros de Visitantes"
        ordering = ['-entry_time']
        
    def __str__(self):
        status = "Activo" if not self.exit_time else "Salió"
        return f"{self.visitor_name} visitando a {self.resident.get_full_name()} - {status}"
    
    def save(self, *args, **kwargs):
        # Auto actualizar el status basado en exit_time
        if self.exit_time:
            self.status = 'Salió'
        else:
            self.status = 'Activo'
        super().save(*args, **kwargs)
