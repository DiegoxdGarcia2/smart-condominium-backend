from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UserViewSet, ResidentialUnitViewSet, 
    AnnouncementViewSet, FinancialFeeViewSet, CommonAreaViewSet, 
    ReservationViewSet, VehicleViewSet, PetViewSet, VisitorLogViewSet,
    TaskViewSet, FeedbackViewSet, PaymentViewSet
)

# Crear el router y registrar nuestros viewsets
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'residential-units', ResidentialUnitViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'financial-fees', FinancialFeeViewSet)
router.register(r'common-areas', CommonAreaViewSet)
router.register(r'reservations', ReservationViewSet)
# Nuevos endpoints de la Fase 4
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'visitor-logs', VisitorLogViewSet)
# Nuevos endpoints de la Fase 5
router.register(r'tasks', TaskViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
