from rest_framework import serializers
from .models import (
    Observation,
    WeatherObservation,
    AirQualityObservation,
    TrafficObservation
)


class ObservationSerializer(serializers.ModelSerializer):
    """Serializer for Observation"""
    
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    
    class Meta:
        model = Observation
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class WeatherObservationSerializer(serializers.ModelSerializer):
    """Serializer for Weather Observation"""
    
    class Meta:
        model = WeatherObservation
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AirQualityObservationSerializer(serializers.ModelSerializer):
    """Serializer for Air Quality Observation"""
    
    class Meta:
        model = AirQualityObservation
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class TrafficObservationSerializer(serializers.ModelSerializer):
    """Serializer for Traffic Observation"""
    
    class Meta:
        model = TrafficObservation
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
