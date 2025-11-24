from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, PlatformViewSet, SensorDeploymentViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'platforms', PlatformViewSet, basename='platform')
router.register(r'deployments', SensorDeploymentViewSet, basename='deployment')

urlpatterns = [
    path('', include(router.urls)),
]
