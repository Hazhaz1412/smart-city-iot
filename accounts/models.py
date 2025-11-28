from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class CustomUser(AbstractUser):
    """Extended User model with additional fields"""
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # OAuth fields
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    github_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class UserDevice(models.Model):
    """User's IoT devices - allows users to add their own devices"""
    DEVICE_TYPES = [
        ('weather_station', 'Weather Station'),
        ('air_quality_sensor', 'Air Quality Sensor'),
        ('traffic_sensor', 'Traffic Sensor'),
        ('custom', 'Custom Device'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='devices')
    
    # Device info
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    device_id = models.CharField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_public = models.BooleanField(default=False, help_text="Allow others to view this device data")
    is_verified = models.BooleanField(default=False, help_text="Verified by admin as trusted device")
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_devices')
    
    # API/Connection info
    api_endpoint = models.URLField(blank=True, null=True, help_text="External API endpoint for this device")
    api_key = models.CharField(max_length=500, blank=True, null=True, help_text="API key for external service")
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generate unique device_id if not provided
        if not self.device_id:
            # Create prefix based on device type
            prefix_map = {
                'weather_station': 'WS',
                'air_quality_sensor': 'AQ',
                'traffic_sensor': 'TS',
                'custom': 'CT'
            }
            prefix = prefix_map.get(self.device_type, 'DV')
            
            # Generate unique ID: TYPE-XXXXXX (e.g., WS-A3B5C7)
            unique_id = uuid.uuid4().hex[:6].upper()
            self.device_id = f"{prefix}-{unique_id}"
            
            # Ensure uniqueness (in case of collision)
            counter = 1
            base_id = self.device_id
            while UserDevice.objects.filter(device_id=self.device_id).exists():
                self.device_id = f"{base_id}{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_devices'
        ordering = ['-created_at']
        unique_together = [['user', 'device_id']]

    def __str__(self):
        return f"{self.name} ({self.device_type}) - {self.user.username}"


class DeviceData(models.Model):
    """Store data readings from user devices"""
    device = models.ForeignKey(UserDevice, on_delete=models.CASCADE, related_name='readings')
    
    # Data payload (flexible JSON structure)
    data = models.JSONField()
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    recorded_at = models.DateTimeField(blank=True, null=True, help_text="Actual time of measurement")
    
    class Meta:
        db_table = 'device_data'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"
