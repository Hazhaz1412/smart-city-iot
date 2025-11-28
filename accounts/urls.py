from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    login_view,
    google_login,
    UserProfileView,
    UserDeviceViewSet,
    PublicDeviceViewSet,
)

router = DefaultRouter()
router.register(r'devices', UserDeviceViewSet, basename='user-device')
router.register(r'public-devices', PublicDeviceViewSet, basename='public-device')

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('google/', google_login, name='google-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Devices
    path('', include(router.urls)),
]
