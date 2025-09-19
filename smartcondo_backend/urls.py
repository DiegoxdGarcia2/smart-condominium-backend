"""
URL configuration for smartcondo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def api_status(request):
    """Vista simple para mostrar el estado de la API"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Smart Condominium Backend API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'auth': '/api/token/',
            'administration': '/api/administration/'
        }
    })

urlpatterns = [
    # Root endpoint - API status
    path('', api_status, name='api_status'),
    path('api/', api_status, name='api_root'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/administration/', include('administration.urls')),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
