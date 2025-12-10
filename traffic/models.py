from django.db import models
from django.utils import timezone


class BusStation(models.Model):
    entity_id = models.CharField(max_length=255, unique=True, help_text="NGSI-LD entity ID")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    station_type = models.CharField(max_length=50, choices=[("bus_stop", "Bus Stop"), ("bus_terminal", "Bus Terminal"), ("metro_station", "Metro Station")], default="bus_stop")
    routes = models.JSONField(default=list, help_text="List of bus routes")
    status = models.CharField(max_length=20, choices=[("active", "Active"), ("inactive", "Inactive"), ("maintenance", "Maintenance")], default="active")
    has_shelter = models.BooleanField(default=True)
    has_bench = models.BooleanField(default=True)
    wheelchair_accessible = models.BooleanField(default=False)
    has_real_time_info = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name


class TrafficFlow(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    road_name = models.CharField(max_length=255)
    road_segment = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    congestion_level = models.CharField(max_length=20, choices=[("free", "Free"), ("light", "Light"), ("moderate", "Moderate"), ("heavy", "Heavy"), ("severe", "Severe")], default="free")
    average_speed = models.FloatField(help_text="km/h")
    vehicle_count = models.IntegerField(default=0)
    occupancy = models.FloatField(default=0.0)
    observed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-observed_at"]
    
    def __str__(self):
        return f"{self.road_name} - {self.congestion_level}"


class TrafficIncident(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    incident_type = models.CharField(max_length=50, choices=[("accident", "Accident"), ("roadwork", "Road Work"), ("congestion", "Congestion"), ("weather", "Weather"), ("event", "Event"), ("other", "Other")], default="accident")
    severity = models.CharField(max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="medium")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    status = models.CharField(max_length=20, choices=[("reported", "Reported"), ("verified", "Verified"), ("in_progress", "In Progress"), ("resolved", "Resolved")], default="reported")
    reported_by = models.CharField(max_length=255, blank=True, null=True)
    reported_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-reported_at"]
    
    def __str__(self):
        return self.title


class ParkingSpot(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    parking_type = models.CharField(max_length=50, choices=[("on_street", "On Street"), ("off_street", "Off Street"), ("parking_lot", "Parking Lot"), ("parking_garage", "Parking Garage")], default="on_street")
    total_spaces = models.IntegerField(default=0)
    available_spaces = models.IntegerField(default=0)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    currency = models.CharField(max_length=10, default="VND")
    status = models.CharField(max_length=20, choices=[("open", "Open"), ("closed", "Closed"), ("full", "Full")], default="open")
    has_ev_charging = models.BooleanField(default=False)
    has_disability_spaces = models.BooleanField(default=True)
    is_covered = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    is_24h = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    
    @property
    def occupancy_rate(self):
        if self.total_spaces == 0:
            return 0
        return ((self.total_spaces - self.available_spaces) / self.total_spaces) * 100
