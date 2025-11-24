from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EntityViewSet,
    WeatherStationViewSet,
    AirQualitySensorViewSet,
    TrafficSensorViewSet,
    PublicServiceViewSet
)

router = DefaultRouter()
router.register(r'entities', EntityViewSet, basename='entity')
router.register(r'weather-stations', WeatherStationViewSet, basename='weather-station')
router.register(r'air-quality-sensors', AirQualitySensorViewSet, basename='air-quality-sensor')
router.register(r'traffic-sensors', TrafficSensorViewSet, basename='traffic-sensor')
router.register(r'public-services', PublicServiceViewSet, basename='public-service')

urlpatterns = [
    path('', include(router.urls)),
]
