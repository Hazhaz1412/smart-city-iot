"""
Integration with OpenWeatherMap API
"""
import requests
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_openweather_api_key(user=None):
    """Get OpenWeatherMap API key from database or settings"""
    try:
        from .models import get_api_key_for_provider
        key = get_api_key_for_provider('openweathermap', user)
        if key:
            return key
    except Exception as e:
        logger.warning(f"Failed to get API key from database: {e}")
    
    # Fallback to settings
    return getattr(settings, 'OPENWEATHER_API_KEY', None)


class OpenWeatherMapClient:
    """Client for OpenWeatherMap API"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key: str = None, user=None):
        self.api_key = api_key or get_openweather_api_key(user)
    
    def get_current_weather(self, lat: float, lon: float):
        """Get current weather data"""
        url = f"{self.BASE_URL}/weather"
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_weather_data(data, lat, lon)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather data: {e}")
            return None
    
    def get_weather_by_city(self, city_name: str):
        """Get current weather by city name"""
        url = f"{self.BASE_URL}/weather"
        
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            lat = data['coord']['lat']
            lon = data['coord']['lon']
            
            return self._parse_weather_data(data, lat, lon)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather data: {e}")
            return None
    
    def _parse_weather_data(self, data: dict, lat: float, lon: float):
        """Parse weather data from API response"""
        return {
            'latitude': lat,
            'longitude': lon,
            'location_name': data.get('name', ''),
            'temperature': data['main'].get('temp'),
            'humidity': data['main'].get('humidity'),
            'pressure': data['main'].get('pressure'),
            'wind_speed': data['wind'].get('speed'),
            'wind_direction': data['wind'].get('deg'),
            'weather_description': data['weather'][0].get('description', ''),
            'observed_at': datetime.fromtimestamp(data['dt']),
            'source': 'openweathermap'
        }
