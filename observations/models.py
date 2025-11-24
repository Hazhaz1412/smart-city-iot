"""
Models for observations based on SOSA/SSN ontology
"""
from django.db import models
from sensors.models import Sensor
import uuid


class Observation(models.Model):
    """SOSA Observation model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_id = models.CharField(max_length=200, unique=True, db_index=True)
    
    # SOSA properties
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='observations'
    )
    observed_property = models.CharField(max_length=200)
    
    # Result
    result_value = models.FloatField()
    result_unit = models.CharField(max_length=50, blank=True)
    result_string = models.TextField(blank=True)
    
    # Time properties
    phenomenon_time = models.DateTimeField()
    result_time = models.DateTimeField()
    
    # Location (optional)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-result_time']
        indexes = [
            models.Index(fields=['sensor', 'result_time']),
            models.Index(fields=['observed_property', 'result_time']),
        ]
    
    def __str__(self):
        return f"{self.observed_property}: {self.result_value} at {self.result_time}"


class WeatherObservation(models.Model):
    """Weather observation data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_id = models.CharField(max_length=200, unique=True, db_index=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=300, blank=True)
    
    # Weather data
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    weather_description = models.CharField(max_length=200, blank=True)
    
    # Time
    observed_at = models.DateTimeField()
    
    # Metadata
    source = models.CharField(max_length=100, default='manual')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-observed_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude', 'observed_at']),
        ]
    
    def __str__(self):
        return f"Weather at {self.location_name or f'({self.latitude}, {self.longitude})'} - {self.observed_at}"


class AirQualityObservation(models.Model):
    """Air quality observation data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_id = models.CharField(max_length=200, unique=True, db_index=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=300, blank=True)
    
    # Air quality data
    aqi = models.FloatField(null=True, blank=True)
    pm25 = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    o3 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    so2 = models.FloatField(null=True, blank=True)
    
    # Time
    observed_at = models.DateTimeField()
    
    # Metadata
    source = models.CharField(max_length=100, default='manual')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-observed_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude', 'observed_at']),
        ]
    
    def __str__(self):
        return f"AQI at {self.location_name or f'({self.latitude}, {self.longitude})'} - {self.observed_at}"


class TrafficObservation(models.Model):
    """Traffic flow observation data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_id = models.CharField(max_length=200, unique=True, db_index=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=300, blank=True)
    
    # Traffic data
    intensity = models.IntegerField(help_text="Number of vehicles")
    occupancy = models.FloatField(help_text="Percentage 0-100")
    average_speed = models.FloatField(help_text="km/h")
    congestion_level = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('very_high', 'Very High'),
        ],
        blank=True
    )
    
    # Time
    observed_at = models.DateTimeField()
    
    # Metadata
    source = models.CharField(max_length=100, default='manual')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-observed_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude', 'observed_at']),
        ]
    
    def __str__(self):
        return f"Traffic at {self.location_name or f'({self.latitude}, {self.longitude})'} - {self.observed_at}"
