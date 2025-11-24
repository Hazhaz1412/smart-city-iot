"""
Models for storing NGSI-LD entities
"""
from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class Entity(models.Model):
    """Base model for NGSI-LD entities"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_id = models.CharField(max_length=500, unique=True, db_index=True)
    entity_type = models.CharField(max_length=200, db_index=True)
    data = models.JSONField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Geolocation for spatial queries
    latitude = models.FloatField(null=True, blank=True, db_index=True)
    longitude = models.FloatField(null=True, blank=True, db_index=True)
    
    # Sync status with Orion-LD
    synced_to_orion = models.BooleanField(default=False)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type', 'created_at']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.entity_type}: {self.entity_id}"


class WeatherStation(models.Model):
    """Weather Station entity"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference to NGSI-LD entity
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='weather_stations'
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AirQualitySensor(models.Model):
    """Air Quality Sensor entity"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference to NGSI-LD entity
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='air_quality_sensors'
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TrafficSensor(models.Model):
    """Traffic Sensor entity"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference to NGSI-LD entity
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='traffic_sensors'
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PublicService(models.Model):
    """Public Service entity (parks, parking lots, etc.)"""
    
    SERVICE_TYPES = [
        ('park', 'Công viên'),
        ('parking', 'Bãi đỗ xe'),
        ('bus_stop', 'Trạm xe buýt'),
        ('hospital', 'Bệnh viện'),
        ('school', 'Trường học'),
        ('library', 'Thư viện'),
        ('other', 'Khác'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField(blank=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Additional data
    opening_hours = models.CharField(max_length=200, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference to NGSI-LD entity
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='public_services'
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"
