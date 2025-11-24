from django.contrib import admin
from .models import (
    Observation,
    WeatherObservation,
    AirQualityObservation,
    TrafficObservation
)


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ['observation_id', 'sensor', 'observed_property', 'result_value', 'result_time']
    list_filter = ['observed_property', 'result_time']
    search_fields = ['observation_id', 'sensor__name']


@admin.register(WeatherObservation)
class WeatherObservationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'temperature', 'humidity', 'observed_at']
    list_filter = ['observed_at', 'source']
    search_fields = ['location_name', 'observation_id']


@admin.register(AirQualityObservation)
class AirQualityObservationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'aqi', 'pm25', 'observed_at']
    list_filter = ['observed_at', 'source']
    search_fields = ['location_name', 'observation_id']


@admin.register(TrafficObservation)
class TrafficObservationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'intensity', 'average_speed', 'congestion_level', 'observed_at']
    list_filter = ['congestion_level', 'observed_at', 'source']
    search_fields = ['location_name', 'observation_id']
