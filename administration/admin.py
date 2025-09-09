from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, ResidentialUnit


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Role"""
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuración del admin para el modelo User personalizado"""
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']
    
    # Campos a mostrar en el formulario de edición
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('phone_number', 'role')
        }),
    )
    
    # Campos a mostrar en el formulario de creación
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'role')
        }),
    )


@admin.register(ResidentialUnit)
class ResidentialUnitAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo ResidentialUnit"""
    list_display = ['unit_number', 'type', 'floor', 'owner']
    list_filter = ['type', 'floor']
    search_fields = ['unit_number', 'owner__first_name', 'owner__last_name', 'owner__email']
    ordering = ['unit_number']
    
    # Filtros laterales
    autocomplete_fields = ['owner']
