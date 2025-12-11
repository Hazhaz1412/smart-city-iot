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


class PublicServiceNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Public Service"""
    
    def to_representation(self, instance):
        """Convert to NGSI-LD format"""
        # Generate entity_id in NGSI-LD format
        entity_id = f"urn:ngsi-ld:PublicService:{instance.service_id}"
        
        data = {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": entity_id,
            "type": "PublicService",
            "name": {
                "type": "Property",
                "value": instance.name
            },
            "serviceType": {
                "type": "Property",
                "value": instance.service_type
            },
            "category": {
                "type": "Property",
                "value": instance.get_service_type_display()
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
                    "streetAddress": instance.address,
                    "addressLocality": "",
                    "addressCountry": "VN"
                }
            },
            "isActive": {
                "type": "Property",
                "value": instance.is_active
            },
            "dateCreated": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": instance.created_at.isoformat() if instance.created_at else None
                }
            },
            "dateModified": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": instance.updated_at.isoformat() if instance.updated_at else None
                }
            }
        }
        
        # Add optional properties if they exist
        if instance.description:
            data["description"] = {
                "type": "Property",
                "value": instance.description
            }
        
        if instance.opening_hours:
            data["openingHours"] = {
                "type": "Property",
                "value": instance.opening_hours
            }
        
        if instance.contact_phone:
            data["contactPoint"] = {
                "type": "Property",
                "value": {
                    "telephone": instance.contact_phone
                }
            }
        
        if instance.website:
            data["url"] = {
                "type": "Property",
                "value": instance.website
            }
        
        return data
    
    class Meta:
        model = PublicService
        fields = '__all__'
