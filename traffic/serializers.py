from rest_framework import serializers
from .models import BusStation, TrafficFlow, TrafficIncident, ParkingSpot


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TrafficFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlow
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TrafficIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficIncident
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ParkingSpotSerializer(serializers.ModelSerializer):
    occupancy_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ParkingSpot
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "occupancy_rate"]


# ============= NGSI-LD Serializers =============

class BusStationNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Bus Station (TransportStation)"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:TransportStation:{instance.id}",
            "type": "TransportStation",
            "name": {
                "type": "Property",
                "value": instance.name
            },
            "stationType": {
                "type": "Property",
                "value": instance.station_type
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
            "transportationType": {
                "type": "Property",
                "value": ["bus"]
            },
            "refRoutes": {
                "type": "Property",
                "value": instance.routes or []
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "accessibilityFeatures": {
                "type": "Property",
                "value": {
                    "hasShelter": instance.has_shelter,
                    "hasBench": instance.has_bench,
                    "wheelchairAccessible": instance.wheelchair_accessible,
                    "hasRealTimeInfo": instance.has_real_time_info
                }
            },
            "dateCreated": {
                "type": "Property",
                "value": instance.created_at.isoformat() if instance.created_at else None
            },
            "dateModified": {
                "type": "Property",
                "value": instance.updated_at.isoformat() if instance.updated_at else None
            }
        }
    
    class Meta:
        model = BusStation
        fields = "__all__"


class TrafficFlowNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Traffic Flow Observed"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:TrafficFlowObserved:{instance.id}",
            "type": "TrafficFlowObserved",
            "name": {
                "type": "Property",
                "value": instance.road_name
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
                    "streetAddress": instance.road_name or "",
                    "addressLocality": instance.city or "",
                    "addressCountry": "VN"
                }
            },
            "intensity": {
                "type": "Property",
                "value": instance.vehicle_count,
                "unitCode": "vehicles/hour",
                "observedAt": instance.observed_at.isoformat() if instance.observed_at else None
            },
            "averageVehicleSpeed": {
                "type": "Property",
                "value": instance.average_speed,
                "unitCode": "KMH"
            },
            "congestionLevel": {
                "type": "Property",
                "value": instance.congestion_level
            },
            "occupancy": {
                "type": "Property",
                "value": instance.occupancy,
                "unitCode": "P1"
            },
            "dateObserved": {
                "type": "Property",
                "value": instance.observed_at.isoformat() if instance.observed_at else None
            }
        }
    
    class Meta:
        model = TrafficFlow
        fields = "__all__"


class TrafficIncidentNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Traffic Incident"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:TrafficIncident:{instance.id}",
            "type": "TrafficIncident",
            "incidentType": {
                "type": "Property",
                "value": instance.incident_type
            },
            "title": {
                "type": "Property",
                "value": instance.title
            },
            "description": {
                "type": "Property",
                "value": instance.description or ""
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
            "severity": {
                "type": "Property",
                "value": instance.severity
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "reportedAt": {
                "type": "Property",
                "value": instance.reported_at.isoformat() if instance.reported_at else None
            },
            "resolvedAt": {
                "type": "Property",
                "value": instance.resolved_at.isoformat() if instance.resolved_at else None
            }
        }
    
    class Meta:
        model = TrafficIncident
        fields = "__all__"


class ParkingSpotNGSILDSerializer(serializers.ModelSerializer):
    """NGSI-LD compliant serializer for Off Street Parking"""
    
    def to_representation(self, instance):
        return {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://smartdatamodels.org/context.jsonld"
            ],
            "id": instance.entity_id or f"urn:ngsi-ld:OffStreetParking:{instance.id}",
            "type": "OffStreetParking",
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
            "totalSpotNumber": {
                "type": "Property",
                "value": instance.total_spaces
            },
            "availableSpotNumber": {
                "type": "Property",
                "value": instance.available_spaces,
                "observedAt": instance.updated_at.isoformat() if instance.updated_at else None
            },
            "occupancyRate": {
                "type": "Property",
                "value": round((instance.total_spaces - instance.available_spaces) / max(instance.total_spaces, 1) * 100, 2),
                "unitCode": "P1"
            },
            "parkingType": {
                "type": "Property",
                "value": instance.parking_type
            },
            "pricePerHour": {
                "type": "Property",
                "value": float(instance.price_per_hour) if instance.price_per_hour else 0,
                "unitCode": instance.currency or "VND"
            },
            "status": {
                "type": "Property",
                "value": instance.status
            },
            "openingHours": {
                "type": "Property",
                "value": "24/7" if instance.is_24h else f"{instance.opening_time}-{instance.closing_time}" if instance.opening_time and instance.closing_time else "N/A"
            }
        }
    
    class Meta:
        model = ParkingSpot
        fields = "__all__"
