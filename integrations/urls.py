from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WeatherSyncView,
    AirQualitySyncView,
    SingleLocationWeatherView,
    SingleLocationAirQualityView,
    ExternalAPIProviderViewSet,
    UserAPIKeyViewSet,
    SystemAPIKeyViewSet,
    LatestWeatherView,
    LatestAirQualityView,
)

router = DefaultRouter()
router.register(r'api-providers', ExternalAPIProviderViewSet, basename='api-provider')
router.register(r'my-api-keys', UserAPIKeyViewSet, basename='user-api-key')
router.register(r'system-api-keys', SystemAPIKeyViewSet, basename='system-api-key')

urlpatterns = [
    path('sync/weather/', WeatherSyncView.as_view(), name='sync-weather'),
    path('sync/air-quality/', AirQualitySyncView.as_view(), name='sync-air-quality'),
    path('fetch/weather/', SingleLocationWeatherView.as_view(), name='fetch-weather'),
    path('fetch/air-quality/', SingleLocationAirQualityView.as_view(), name='fetch-air-quality'),
    path('weather/', LatestWeatherView.as_view(), name='latest-weather'),
    path('air-quality/', LatestAirQualityView.as_view(), name='latest-air-quality'),
    path('', include(router.urls)),
]
