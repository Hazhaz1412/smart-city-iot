from django.contrib import admin
from .models import (
    Entity,
    WeatherStation,
    AirQualitySensor,
    TrafficSensor,
    PublicService
)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['entity_id', 'entity_type', 'synced_to_orion', 'created_at']
    list_filter = ['entity_type', 'synced_to_orion']
    search_fields = ['entity_id', 'entity_type']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WeatherStation)
class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'station_id', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'station_id', 'address']


@admin.register(AirQualitySensor)
class AirQualitySensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sensor_id', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'sensor_id', 'address']


@admin.register(TrafficSensor)
class TrafficSensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sensor_id', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'sensor_id', 'address']


@admin.register(PublicService)
class PublicServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'latitude', 'longitude', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'service_id', 'address']
