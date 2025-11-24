"""
Models for sensors based on SOSA/SSN ontology
"""
from django.db import models
import uuid


class Sensor(models.Model):
    """SOSA Sensor model"""
    
    SENSOR_TYPES = [
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('pressure', 'Pressure Sensor'),
        ('pm25', 'PM2.5 Sensor'),
        ('pm10', 'PM10 Sensor'),
        ('no2', 'NO2 Sensor'),
        ('o3', 'O3 Sensor'),
        ('co', 'CO Sensor'),
        ('so2', 'SO2 Sensor'),
        ('noise', 'Noise Sensor'),
        ('traffic', 'Traffic Sensor'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)
    description = models.TextField(blank=True)
    
    # SOSA properties
    observes_property = models.CharField(max_length=200)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    manufacturer = models.CharField(max_length=200, blank=True)
    model_name = models.CharField(max_length=200, blank=True)
    serial_number = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_sensor_type_display()})"


class Platform(models.Model):
    """SOSA Platform (hosts sensors)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.CharField(max_length=200, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SensorDeployment(models.Model):
    """Deployment of a sensor on a platform"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    
    deployed_at = models.DateTimeField()
    removed_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-deployed_at']
    
    def __str__(self):
        return f"{self.sensor.name} on {self.platform.name}"
