"""
Celery tasks for data synchronization
"""
from celery import shared_task
from django.utils import timezone
from .openweather import OpenWeatherMapClient
from .openaq import OpenAQClient, calculate_aqi_from_pm25
from observations.models import WeatherObservation, AirQualityObservation
from entities.models import WeatherStation, AirQualitySensor
from core.ngsi_ld import (
    create_air_quality_observed_entity,
    create_weather_station_entity
)
from core.orion_client import OrionLDClient
import logging
import uuid

logger = logging.getLogger(__name__)


@shared_task
def sync_weather_data():
    """Sync weather data from OpenWeatherMap"""
    logger.info("Starting weather data synchronization")
    
    # Get all active weather stations
    stations = WeatherStation.objects.filter(is_active=True)
    
    client = OpenWeatherMapClient()
    orion_client = OrionLDClient()
    
    count = 0
    for station in stations:
        try:
            # Fetch weather data
            weather_data = client.get_current_weather(
                station.latitude,
                station.longitude
            )
            
            if weather_data:
                # Save to database
                obs_id = f"weather-{station.station_id}-{int(timezone.now().timestamp())}"
                
                observation = WeatherObservation.objects.create(
                    observation_id=obs_id,
                    **weather_data
                )
                
                count += 1
                logger.info(f"Created weather observation for {station.name}")
                
                # Sync to Orion-LD if needed
                # You can create NGSI-LD entity here
                
        except Exception as e:
            logger.error(f"Failed to sync weather for {station.name}: {e}")
    
    logger.info(f"Weather sync completed: {count} observations created")
    return count


@shared_task
def sync_air_quality_data():
    """Sync air quality data from OpenAQ"""
    logger.info("Starting air quality data synchronization")
    
    # Get all active air quality sensors
    sensors = AirQualitySensor.objects.filter(is_active=True)
    
    client = OpenAQClient()
    orion_client = OrionLDClient()
    
    count = 0
    for sensor in sensors:
        try:
            # Fetch air quality data
            aq_data = client.get_latest_measurements(
                sensor.latitude,
                sensor.longitude,
                radius=10000  # 10km
            )
            
            if aq_data:
                # Calculate AQI if not provided
                if aq_data.get('pm25') and not aq_data.get('aqi'):
                    aq_data['aqi'] = calculate_aqi_from_pm25(aq_data['pm25'])
                
                # Save to database
                obs_id = f"airquality-{sensor.sensor_id}-{int(timezone.now().timestamp())}"
                
                observation = AirQualityObservation.objects.create(
                    observation_id=obs_id,
                    **aq_data
                )
                
                # Create NGSI-LD entity
                ngsi_entity = create_air_quality_observed_entity(
                    observation_id=obs_id,
                    latitude=aq_data['latitude'],
                    longitude=aq_data['longitude'],
                    aqi=aq_data.get('aqi'),
                    pm25=aq_data.get('pm25'),
                    pm10=aq_data.get('pm10'),
                    no2=aq_data.get('no2'),
                    o3=aq_data.get('o3'),
                    co=aq_data.get('co'),
                    so2=aq_data.get('so2'),
                    date_observed=aq_data['observed_at']
                )
                
                # Sync to Orion-LD
                orion_client.create_entity(ngsi_entity)
                
                count += 1
                logger.info(f"Created air quality observation for {sensor.name}")
                
        except Exception as e:
            logger.error(f"Failed to sync air quality for {sensor.name}: {e}")
    
    logger.info(f"Air quality sync completed: {count} observations created")
    return count


@shared_task
def sync_single_location_weather(lat: float, lon: float, location_name: str = ""):
    """Sync weather data for a single location"""
    client = OpenWeatherMapClient()
    
    try:
        weather_data = client.get_current_weather(lat, lon)
        
        if weather_data:
            obs_id = f"weather-manual-{uuid.uuid4().hex[:8]}"
            weather_data['location_name'] = location_name or weather_data.get('location_name', '')
            
            observation = WeatherObservation.objects.create(
                observation_id=obs_id,
                **weather_data
            )
            
            logger.info(f"Created weather observation for {location_name}")
            return observation.id
    except Exception as e:
        logger.error(f"Failed to sync weather: {e}")
        return None


@shared_task
def sync_single_location_air_quality(lat: float, lon: float, location_name: str = ""):
    """Sync air quality data for a single location"""
    client = OpenAQClient()
    
    try:
        aq_data = client.get_latest_measurements(lat, lon)
        
        if aq_data:
            if aq_data.get('pm25') and not aq_data.get('aqi'):
                aq_data['aqi'] = calculate_aqi_from_pm25(aq_data['pm25'])
            
            obs_id = f"airquality-manual-{uuid.uuid4().hex[:8]}"
            aq_data['location_name'] = location_name or aq_data.get('location_name', '')
            
            observation = AirQualityObservation.objects.create(
                observation_id=obs_id,
                **aq_data
            )
            
            logger.info(f"Created air quality observation for {location_name}")
            return observation.id
    except Exception as e:
        logger.error(f"Failed to sync air quality: {e}")
        return None
