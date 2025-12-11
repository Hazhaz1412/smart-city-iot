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


# ==================== NGSI-LD SERIALIZERS ====================

class WeatherObservationNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Weather Observed"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.observation_id or f"urn:ngsi-ld:WeatherObserved:{instance.id}",
            "type": "WeatherObserved",
            "name": {
                "type": "Property",
                "value": instance.location_name or f"Weather Station ({instance.latitude}, {instance.longitude})"
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": [instance.longitude, instance.latitude]
                }
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressLocality": instance.location_name or "",
                    "addressCountry": "VN"
                }
            },
            "temperature": {
                "type": "Property",
                "value": instance.temperature,
                "unitCode": "CEL",
                "observedAt": instance.observed_at.isoformat() if instance.observed_at else None
            },
            "relativeHumidity": {
                "type": "Property",
                "value": instance.humidity,
                "unitCode": "P1"
            },
            "atmosphericPressure": {
                "type": "Property",
                "value": instance.pressure,
                "unitCode": "HPA"
            },
            "windSpeed": {
                "type": "Property",
                "value": instance.wind_speed,
                "unitCode": "MTS"
            },
            "windDirection": {
                "type": "Property",
                "value": instance.wind_direction,
                "unitCode": "DD"
            },
            "precipitation": {
                "type": "Property",
                "value": instance.precipitation,
                "unitCode": "MMT"
            },
            "weatherType": {
                "type": "Property",
                "value": instance.weather_description or ""
            },
            "dateObserved": {
                "type": "Property",
                "value": instance.observed_at.isoformat() if instance.observed_at else None
            },
            "source": {
                "type": "Property",
                "value": instance.source or "manual"
            }
        }
    
    class Meta:
        model = WeatherObservation
        fields = "__all__"


class AirQualityObservationNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Air Quality Observed"""
    
    def get_aqi_category(self, aqi):
        """Get AQI category based on value"""
        if aqi is None:
            return "unknown"
        if aqi <= 50:
            return "good"
        elif aqi <= 100:
            return "moderate"
        elif aqi <= 150:
            return "unhealthyForSensitiveGroups"
        elif aqi <= 200:
            return "unhealthy"
        elif aqi <= 300:
            return "veryUnhealthy"
        else:
            return "hazardous"
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.observation_id or f"urn:ngsi-ld:AirQualityObserved:{instance.id}",
            "type": "AirQualityObserved",
            "name": {
                "type": "Property",
                "value": instance.location_name or f"Air Quality Station ({instance.latitude}, {instance.longitude})"
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": [instance.longitude, instance.latitude]
                }
            },
            "address": {
                "type": "Property",
                "value": {
                    "addressLocality": instance.location_name or "",
                    "addressCountry": "VN"
                }
            },
            "airQualityIndex": {
                "type": "Property",
                "value": instance.aqi,
                "observedAt": instance.observed_at.isoformat() if instance.observed_at else None
            },
            "airQualityLevel": {
                "type": "Property",
                "value": self.get_aqi_category(instance.aqi)
            },
            "pm25": {
                "type": "Property",
                "value": instance.pm25,
                "unitCode": "GQ"
            },
            "pm10": {
                "type": "Property",
                "value": instance.pm10,
                "unitCode": "GQ"
            },
            "no2": {
                "type": "Property",
                "value": instance.no2,
                "unitCode": "GQ"
            },
            "o3": {
                "type": "Property",
                "value": instance.o3,
                "unitCode": "GQ"
            },
            "co": {
                "type": "Property",
                "value": instance.co,
                "unitCode": "GQ"
            },
            "so2": {
                "type": "Property",
                "value": instance.so2,
                "unitCode": "GQ"
            },
            "dateObserved": {
                "type": "Property",
                "value": instance.observed_at.isoformat() if instance.observed_at else None
            },
            "source": {
                "type": "Property",
                "value": instance.source or "manual"
            }
        }
    
    class Meta:
        model = AirQualityObservation
        fields = "__all__"
