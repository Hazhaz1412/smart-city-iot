from rest_framework import serializers
from .models import Sensor, Platform, SensorDeployment


class SensorSerializer(serializers.ModelSerializer):
    """Serializer for Sensor"""
    
    sensor_type_display = serializers.CharField(
        source='get_sensor_type_display',
        read_only=True
    )
    
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform"""
    
    class Meta:
        model = Platform
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SensorDeploymentSerializer(serializers.ModelSerializer):
    """Serializer for SensorDeployment"""
    
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = SensorDeployment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
