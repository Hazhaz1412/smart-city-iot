from rest_framework import serializers
from .models import WaterSupplyPoint, DrainagePoint, StreetLight, EnergyMeter, TelecomTower


class WaterSupplyPointSerializer(serializers.ModelSerializer):
    fill_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WaterSupplyPoint
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_fill_percentage(self, obj):
        if obj.capacity == 0:
            return 0
        return round((obj.current_level / obj.capacity) * 100, 2)


class DrainagePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrainagePoint
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class StreetLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetLight
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class EnergyMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyMeter
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TelecomTowerSerializer(serializers.ModelSerializer):
    utilization_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = TelecomTower
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_utilization_rate(self, obj):
        if obj.max_connections == 0:
            return 0
        return round((obj.active_connections / obj.max_connections) * 100, 2)


# ============= NGSI-LD Serializers =============

class WaterSupplyPointNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Water Supply Point (WaterDistribution)"""
    
    def to_representation(self, instance):
        fill_pct = round((instance.current_level / max(instance.capacity, 1)) * 100, 2)
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:WaterDistribution:{instance.id}",
            "type": "WaterDistribution",
            "name": {
                "type": "Property",
                "value": instance.name
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
                    "streetAddress": instance.address or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "waterType": {
                "type": "Property",
                "value": instance.point_type
            },
            "capacity": {
                "type": "Property",
                "value": float(instance.capacity),
                "unitCode": "LTR"
            },
            "currentLevel": {
                "type": "Property",
                "value": float(instance.current_level),
                "unitCode": "LTR",
                "observedAt": instance.last_reading_at.isoformat() if instance.last_reading_at else None
            },
            "fillPercentage": {
                "type": "Property",
                "value": fill_pct,
                "unitCode": "P1"
            },
            "flowRate": {
                "type": "Property",
                "value": float(instance.flow_rate) if instance.flow_rate else 0,
                "unitCode": "LTR/MIN"
            },
            "pressure": {
                "type": "Property",
                "value": float(instance.pressure) if instance.pressure else 0,
                "unitCode": "BAR"
            },
            "waterQuality": {
                "type": "Property",
                "value": {
                    "phLevel": float(instance.ph_level) if instance.ph_level else None,
                    "chlorineLevel": float(instance.chlorine_level) if instance.chlorine_level else None,
                    "turbidity": float(instance.turbidity) if instance.turbidity else None
                }
            },
            "status": {
                "type": "Property",
                "value": instance.status
            }
        }
    
    class Meta:
        model = WaterSupplyPoint
        fields = "__all__"


class DrainagePointNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Drainage Point (WasteWaterManagement)"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:WasteWaterManagement:{instance.id}",
            "type": "WasteWaterManagement",
            "name": {
                "type": "Property",
                "value": instance.name
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
                    "streetAddress": instance.address or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "drainageType": {
                "type": "Property",
                "value": instance.point_type
            },
            "capacity": {
                "type": "Property",
                "value": float(instance.capacity) if instance.capacity else 0,
                "unitCode": "MTQ"
            },
            "currentLevel": {
                "type": "Property",
                "value": float(instance.current_level) if instance.current_level else 0,
                "unitCode": "P1"
            },
            "flowRate": {
                "type": "Property",
                "value": float(instance.flow_rate) if instance.flow_rate else 0,
                "unitCode": "MTQ/H"
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "floodRisk": {
                "type": "Property",
                "value": instance.flood_risk
            },
            "lastReadingAt": {
                "type": "Property",
                "value": instance.last_reading_at.isoformat() if instance.last_reading_at else None
            }
        }
    
    class Meta:
        model = DrainagePoint
        fields = "__all__"


class StreetLightNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Street Light (Streetlight)"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:Streetlight:{instance.id}",
            "type": "Streetlight",
            "name": {
                "type": "Property",
                "value": f"Pole {instance.pole_id}"
            },
            "poleId": {
                "type": "Property",
                "value": instance.pole_id
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
                    "streetAddress": instance.address or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "lampType": {
                "type": "Property",
                "value": instance.lamp_type
            },
            "powerConsumption": {
                "type": "Property",
                "value": instance.power_rating,
                "unitCode": "WAT"
            },
            "illuminanceLevel": {
                "type": "Property",
                "value": instance.brightness_level,
                "unitCode": "P1"
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "isAutomatic": {
                "type": "Property",
                "value": instance.is_smart
            },
            "features": {
                "type": "Property",
                "value": {
                    "hasMotionSensor": instance.has_motion_sensor,
                    "hasLightSensor": instance.has_light_sensor,
                    "hasCamera": instance.has_camera,
                    "hasAirQualitySensor": instance.has_air_quality_sensor
                }
            },
            "energyConsumedToday": {
                "type": "Property",
                "value": instance.energy_consumed_today,
                "unitCode": "KWH"
            },
            "lastMaintenanceDate": {
                "type": "Property",
                "value": instance.last_maintenance_at.isoformat() if instance.last_maintenance_at else None
            },
            "dateInstalled": {
                "type": "Property",
                "value": instance.installed_at.isoformat() if instance.installed_at else None
            }
        }
    
    class Meta:
        model = StreetLight
        fields = "__all__"


class EnergyMeterNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Energy Meter (EnergyMeter)"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:EnergyMeter:{instance.id}",
            "type": "EnergyMeter",
            "name": {
                "type": "Property",
                "value": instance.name
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
                    "streetAddress": instance.address or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "meterType": {
                "type": "Property",
                "value": instance.meter_type
            },
            "totalEnergyConsumed": {
                "type": "Property",
                "value": float(instance.today_consumption) if instance.today_consumption else 0,
                "unitCode": "KWH"
            },
            "monthConsumption": {
                "type": "Property",
                "value": float(instance.month_consumption) if instance.month_consumption else 0,
                "unitCode": "KWH"
            },
            "currentPower": {
                "type": "Property",
                "value": float(instance.current_power) if instance.current_power else 0,
                "unitCode": "KWT"
            },
            "voltage": {
                "type": "Property",
                "value": float(instance.voltage) if instance.voltage else 0,
                "unitCode": "VLT"
            },
            "current": {
                "type": "Property",
                "value": float(instance.current) if instance.current else 0,
                "unitCode": "AMP"
            },
            "powerFactor": {
                "type": "Property",
                "value": float(instance.power_factor) if instance.power_factor else 0
            },
            "frequency": {
                "type": "Property",
                "value": float(instance.frequency) if instance.frequency else 50,
                "unitCode": "HTZ"
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "lastReadingDate": {
                "type": "Property",
                "value": instance.last_reading_at.isoformat() if instance.last_reading_at else None
            }
        }
    
    class Meta:
        model = EnergyMeter
        fields = "__all__"


class TelecomTowerNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Telecom Tower (PointOfInteraction)"""
    
    def to_representation(self, instance):
        utilization = round((instance.active_connections / max(instance.max_connections, 1)) * 100, 2)
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:PointOfInteraction:{instance.id}",
            "type": "PointOfInteraction",
            "name": {
                "type": "Property",
                "value": instance.name
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
                    "streetAddress": instance.address or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "category": {
                "type": "Property",
                "value": "telecom"
            },
            "towerType": {
                "type": "Property",
                "value": instance.tower_type
            },
            "operator": {
                "type": "Property",
                "value": instance.provider or ""
            },
            "supportedTechnologies": {
                "type": "Property",
                "value": instance.technologies or []
            },
            "frequencyBands": {
                "type": "Property",
                "value": instance.frequency_bands or []
            },
            "height": {
                "type": "Property",
                "value": float(instance.height) if instance.height else 0,
                "unitCode": "MTR"
            },
            "coverageRadius": {
                "type": "Property",
                "value": float(instance.coverage_radius) if instance.coverage_radius else 0,
                "unitCode": "MTR"
            },
            "maxConnections": {
                "type": "Property",
                "value": instance.max_connections
            },
            "activeConnections": {
                "type": "Property",
                "value": instance.active_connections,
                "observedAt": instance.updated_at.isoformat() if instance.updated_at else None
            },
            "utilizationRate": {
                "type": "Property",
                "value": utilization,
                "unitCode": "P1"
            },
            "signalStrength": {
                "type": "Property",
                "value": float(instance.signal_strength) if instance.signal_strength else 0,
                "unitCode": "DBM"
            },
            "status": {
                "type": "Property",
                "value": instance.status
            }
        }
    
    class Meta:
        model = TelecomTower
        fields = "__all__"
