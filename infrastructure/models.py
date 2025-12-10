from django.db import models
from django.utils import timezone


class WaterSupplyPoint(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    point_type = models.CharField(max_length=50, choices=[("reservoir", "Reservoir"), ("treatment_plant", "Treatment Plant"), ("pump_station", "Pump Station"), ("distribution_point", "Distribution Point"), ("hydrant", "Fire Hydrant")], default="distribution_point")
    capacity = models.FloatField(default=0, help_text="Capacity in cubic meters")
    current_level = models.FloatField(default=0, help_text="Current level in cubic meters")
    flow_rate = models.FloatField(default=0, help_text="Flow rate in m3/h")
    pressure = models.FloatField(default=0, help_text="Pressure in bar")
    ph_level = models.FloatField(blank=True, null=True)
    chlorine_level = models.FloatField(blank=True, null=True, help_text="mg/L")
    turbidity = models.FloatField(blank=True, null=True, help_text="NTU")
    status = models.CharField(max_length=20, choices=[("operational", "Operational"), ("maintenance", "Maintenance"), ("offline", "Offline"), ("critical", "Critical")], default="operational")
    last_reading_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name


class DrainagePoint(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    point_type = models.CharField(max_length=50, choices=[("storm_drain", "Storm Drain"), ("sewer_main", "Sewer Main"), ("pump_station", "Pump Station"), ("treatment_plant", "Treatment Plant"), ("outfall", "Outfall"), ("manhole", "Manhole")], default="storm_drain")
    capacity = models.FloatField(default=0, help_text="Capacity in cubic meters")
    current_level = models.FloatField(default=0, help_text="Current level percentage")
    flow_rate = models.FloatField(default=0, help_text="Flow rate in m3/h")
    status = models.CharField(max_length=20, choices=[("normal", "Normal"), ("warning", "Warning"), ("critical", "Critical"), ("blocked", "Blocked"), ("maintenance", "Maintenance")], default="normal")
    flood_risk = models.CharField(max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="low")
    last_reading_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name


class StreetLight(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    pole_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    lamp_type = models.CharField(max_length=50, choices=[("led", "LED"), ("sodium", "High Pressure Sodium"), ("metal_halide", "Metal Halide"), ("fluorescent", "Fluorescent")], default="led")
    power_rating = models.IntegerField(default=100, help_text="Power rating in watts")
    brightness_level = models.IntegerField(default=100, help_text="Brightness 0-100")
    is_smart = models.BooleanField(default=False, help_text="Has IoT connectivity")
    has_motion_sensor = models.BooleanField(default=False)
    has_light_sensor = models.BooleanField(default=False)
    has_camera = models.BooleanField(default=False)
    has_air_quality_sensor = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[("on", "On"), ("off", "Off"), ("dimmed", "Dimmed"), ("fault", "Fault"), ("maintenance", "Maintenance")], default="off")
    energy_consumed_today = models.FloatField(default=0, help_text="kWh consumed today")
    total_operating_hours = models.FloatField(default=0)
    installed_at = models.DateField(blank=True, null=True)
    last_maintenance_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Pole {self.pole_id}"


class EnergyMeter(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    meter_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    meter_type = models.CharField(max_length=50, choices=[("residential", "Residential"), ("commercial", "Commercial"), ("industrial", "Industrial"), ("public", "Public Infrastructure"), ("grid", "Grid Substation")], default="public")
    current_power = models.FloatField(default=0, help_text="Current power in kW")
    voltage = models.FloatField(default=220, help_text="Voltage in V")
    current = models.FloatField(default=0, help_text="Current in A")
    power_factor = models.FloatField(default=1.0)
    frequency = models.FloatField(default=50, help_text="Grid frequency in Hz")
    today_consumption = models.FloatField(default=0, help_text="kWh consumed today")
    month_consumption = models.FloatField(default=0, help_text="kWh consumed this month")
    status = models.CharField(max_length=20, choices=[("normal", "Normal"), ("warning", "Warning"), ("critical", "Critical"), ("offline", "Offline")], default="normal")
    last_reading_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name


class TelecomTower(models.Model):
    entity_id = models.CharField(max_length=255, unique=True)
    tower_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, default="Ho Chi Minh")
    tower_type = models.CharField(max_length=50, choices=[("cell_tower", "Cell Tower"), ("small_cell", "Small Cell"), ("fiber_node", "Fiber Node"), ("wifi_hotspot", "WiFi Hotspot"), ("radio_tower", "Radio Tower")], default="cell_tower")
    height = models.FloatField(default=0, help_text="Height in meters")
    coverage_radius = models.FloatField(default=0, help_text="Coverage radius in meters")
    provider = models.CharField(max_length=100, blank=True, null=True)
    technologies = models.JSONField(default=list, help_text="Supported technologies")
    frequency_bands = models.JSONField(default=list, help_text="Frequency bands used")
    active_connections = models.IntegerField(default=0)
    max_connections = models.IntegerField(default=0)
    bandwidth_usage = models.FloatField(default=0, help_text="Bandwidth usage percentage")
    signal_strength = models.FloatField(default=0, help_text="Signal strength in dBm")
    status = models.CharField(max_length=20, choices=[("active", "Active"), ("degraded", "Degraded"), ("maintenance", "Maintenance"), ("offline", "Offline")], default="active")
    installed_at = models.DateField(blank=True, null=True)
    last_maintenance_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
