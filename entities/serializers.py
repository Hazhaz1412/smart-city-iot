from rest_framework import serializers
from .models import (
    Entity,
    WeatherStation,
    AirQualitySensor,
    TrafficSensor,
    PublicService
)


class EntitySerializer(serializers.ModelSerializer):
    """Serializer for Entity model"""
    
    class Meta:
        model = Entity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeatherStationSerializer(serializers.ModelSerializer):
    """Serializer for Weather Station"""
    
    class Meta:
        model = WeatherStation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AirQualitySensorSerializer(serializers.ModelSerializer):
    """Serializer for Air Quality Sensor"""
    
    class Meta:
        model = AirQualitySensor
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TrafficSensorSerializer(serializers.ModelSerializer):
    """Serializer for Traffic Sensor"""
    
    class Meta:
        model = TrafficSensor
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PublicServiceSerializer(serializers.ModelSerializer):
    """Serializer for Public Service"""
    
    service_type_display = serializers.CharField(
        source='get_service_type_display',
        read_only=True
    )
    
    class Meta:
        model = PublicService
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
