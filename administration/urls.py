from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UserViewSet, ResidentialUnitViewSet, 
    AnnouncementViewSet, FinancialFeeViewSet
)

# Crear el router y registrar nuestros viewsets
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'residential-units', ResidentialUnitViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'financial-fees', FinancialFeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
