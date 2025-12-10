from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ObservationViewSet,
    WeatherObservationViewSet,
    AirQualityObservationViewSet,
    TrafficObservationViewSet
)

router = DefaultRouter()
router.register(r'observations', ObservationViewSet, basename='observation')
router.register(r'weather', WeatherObservationViewSet, basename='weather')
router.register(r'air-quality', AirQualityObservationViewSet, basename='air-quality')
router.register(r'traffic-observations', TrafficObservationViewSet, basename='traffic-observation')

urlpatterns = [
    path('', include(router.urls)),
]
