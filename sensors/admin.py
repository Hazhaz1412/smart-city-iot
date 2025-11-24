from django.contrib import admin
from .models import Sensor, Platform, SensorDeployment


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sensor_type', 'is_active', 'created_at']
    list_filter = ['sensor_type', 'is_active']
    search_fields = ['name', 'sensor_id', 'serial_number']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'platform_id']


@admin.register(SensorDeployment)
class SensorDeploymentAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'platform', 'deployed_at', 'is_active']
    list_filter = ['is_active', 'deployed_at']
    search_fields = ['sensor__name', 'platform__name']
