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
