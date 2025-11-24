"""
Core utilities for NGSI-LD and JSON-LD processing
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class NGSILDContext:
    """Manager for NGSI-LD @context"""
    
    CORE_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    SMART_DATA_MODELS = "https://smartdatamodels.org/context.jsonld"
    
    # Custom context definitions
    CUSTOM_CONTEXT = {
        "sosa": "http://www.w3.org/ns/sosa/",
        "ssn": "http://www.w3.org/ns/ssn/",
        "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
        "schema": "https://schema.org/",
        "smartcity": "https://smartcity.example.com/ontology#",
        
        # Properties
        "temperature": "smartcity:temperature",
        "humidity": "smartcity:humidity",
        "pressure": "smartcity:pressure",
        "airQualityIndex": "smartcity:airQualityIndex",
        "pm25": "smartcity:pm25",
        "pm10": "smartcity:pm10",
        "no2": "smartcity:no2",
        "o3": "smartcity:o3",
        "co": "smartcity:co",
        "so2": "smartcity:so2",
        
        # SOSA/SSN properties
        "observes": "sosa:observes",
        "isHostedBy": "sosa:isHostedBy",
        "madeObservation": "sosa:madeObservation",
        "observedProperty": "sosa:observedProperty",
        "madeBySensor": "sosa:madeBySensor",
        "hasSimpleResult": "sosa:hasSimpleResult",
        "resultTime": "sosa:resultTime",
        "phenomenonTime": "sosa:phenomenonTime",
    }
    
    @classmethod
    def get_context(cls) -> List[str | Dict]:
        """Get the full context array for NGSI-LD"""
        return [
            cls.CORE_CONTEXT,
            cls.CUSTOM_CONTEXT
        ]
    
    @classmethod
    def get_context_dict(cls) -> Dict[str, Any]:
        """Get context as dictionary"""
        return {
            "@context": cls.get_context()
        }


class NGSILDEntity:
    """Base class for NGSI-LD entity creation"""
    
    def __init__(self, entity_id: str, entity_type: str):
        self.entity = {
            "id": f"urn:ngsi-ld:{entity_type}:{entity_id}",
            "type": entity_type,
            "@context": NGSILDContext.get_context()
        }
    
    def add_property(
        self,
        name: str,
        value: Any,
        observed_at: Optional[datetime] = None,
        unit_code: Optional[str] = None
    ):
        """Add a property to the entity"""
        prop = {
            "type": "Property",
            "value": value
        }
        
        if observed_at:
            prop["observedAt"] = observed_at.isoformat()
        
        if unit_code:
            prop["unitCode"] = unit_code
        
        self.entity[name] = prop
        return self
    
    def add_relationship(self, name: str, target_id: str):
        """Add a relationship to the entity"""
        self.entity[name] = {
            "type": "Relationship",
            "object": target_id
        }
        return self
    
    def add_geoproperty(
        self,
        latitude: float,
        longitude: float,
        name: str = "location"
    ):
        """Add a geo property to the entity"""
        self.entity[name] = {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.entity
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.entity, indent=2, ensure_ascii=False)


class SOSAObservation(NGSILDEntity):
    """SOSA Observation entity"""
    
    def __init__(self, observation_id: str):
        super().__init__(observation_id, "Observation")
    
    def set_observed_property(self, property_uri: str):
        """Set the observed property"""
        self.add_relationship("observedProperty", property_uri)
        return self
    
    def set_sensor(self, sensor_id: str):
        """Set the sensor that made the observation"""
        self.add_relationship("madeBySensor", sensor_id)
        return self
    
    def set_result(
        self,
        value: Any,
        result_time: datetime,
        phenomenon_time: Optional[datetime] = None
    ):
        """Set the observation result"""
        self.add_property("hasSimpleResult", value)
        self.add_property("resultTime", result_time.isoformat())
        
        if phenomenon_time:
            self.add_property("phenomenonTime", phenomenon_time.isoformat())
        
        return self


class SOSASensor(NGSILDEntity):
    """SOSA Sensor entity"""
    
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, "Sensor")
    
    def set_observes(self, property_uri: str):
        """Set what property this sensor observes"""
        self.add_relationship("observes", property_uri)
        return self
    
    def set_hosted_by(self, platform_id: str):
        """Set the platform hosting this sensor"""
        self.add_relationship("isHostedBy", platform_id)
        return self


def create_weather_station_entity(
    station_id: str,
    name: str,
    latitude: float,
    longitude: float,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """Create a Weather Station entity"""
    entity = NGSILDEntity(station_id, "WeatherStation")
    entity.add_property("name", name)
    entity.add_geoproperty(latitude, longitude)
    
    if address:
        entity.add_property("address", address)
    
    return entity.to_dict()


def create_air_quality_sensor_entity(
    sensor_id: str,
    name: str,
    latitude: float,
    longitude: float,
    sensor_type: str = "AirQualitySensor"
) -> Dict[str, Any]:
    """Create an Air Quality Sensor entity"""
    entity = NGSILDEntity(sensor_id, sensor_type)
    entity.add_property("name", name)
    entity.add_property("category", ["sensor"])
    entity.add_geoproperty(latitude, longitude)
    
    return entity.to_dict()


def create_air_quality_observed_entity(
    observation_id: str,
    latitude: float,
    longitude: float,
    aqi: Optional[float] = None,
    pm25: Optional[float] = None,
    pm10: Optional[float] = None,
    no2: Optional[float] = None,
    o3: Optional[float] = None,
    co: Optional[float] = None,
    so2: Optional[float] = None,
    date_observed: Optional[datetime] = None
) -> Dict[str, Any]:
    """Create an Air Quality Observed entity"""
    entity = NGSILDEntity(observation_id, "AirQualityObserved")
    entity.add_geoproperty(latitude, longitude)
    
    observed_at = date_observed or datetime.now()
    
    if aqi is not None:
        entity.add_property("airQualityIndex", aqi, observed_at=observed_at)
    
    if pm25 is not None:
        entity.add_property("pm25", pm25, observed_at=observed_at, unit_code="GQ")
    
    if pm10 is not None:
        entity.add_property("pm10", pm10, observed_at=observed_at, unit_code="GQ")
    
    if no2 is not None:
        entity.add_property("no2", no2, observed_at=observed_at, unit_code="GQ")
    
    if o3 is not None:
        entity.add_property("o3", o3, observed_at=observed_at, unit_code="GQ")
    
    if co is not None:
        entity.add_property("co", co, observed_at=observed_at, unit_code="GQ")
    
    if so2 is not None:
        entity.add_property("so2", so2, observed_at=observed_at, unit_code="GQ")
    
    entity.add_property("dateObserved", observed_at.isoformat())
    
    return entity.to_dict()


def create_traffic_flow_observed_entity(
    observation_id: str,
    latitude: float,
    longitude: float,
    intensity: int,
    occupancy: float,
    average_speed: float,
    date_observed: Optional[datetime] = None
) -> Dict[str, Any]:
    """Create a Traffic Flow Observed entity"""
    entity = NGSILDEntity(observation_id, "TrafficFlowObserved")
    entity.add_geoproperty(latitude, longitude)
    
    observed_at = date_observed or datetime.now()
    
    entity.add_property("intensity", intensity, observed_at=observed_at)
    entity.add_property("occupancy", occupancy, observed_at=observed_at, unit_code="P1")
    entity.add_property("averageVehicleSpeed", average_speed, observed_at=observed_at, unit_code="KMH")
    entity.add_property("dateObserved", observed_at.isoformat())
    
    return entity.to_dict()
