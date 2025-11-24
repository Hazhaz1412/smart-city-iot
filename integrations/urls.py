from django.urls import path
from .views import (
    WeatherSyncView,
    AirQualitySyncView,
    SingleLocationWeatherView,
    SingleLocationAirQualityView
)

urlpatterns = [
    path('sync/weather', WeatherSyncView.as_view(), name='sync-weather'),
    path('sync/air-quality', AirQualitySyncView.as_view(), name='sync-air-quality'),
    path('fetch/weather', SingleLocationWeatherView.as_view(), name='fetch-weather'),
    path('fetch/air-quality', SingleLocationAirQualityView.as_view(), name='fetch-air-quality'),
]
