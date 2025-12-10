"""
Integration with WAQI (World Air Quality Index) API
https://aqicn.org/api/
"""
import requests
from datetime import datetime
import logging
from django.conf import settings
from .models import get_api_key_for_provider

logger = logging.getLogger(__name__)


class WAQIClient:
    """Client for WAQI (aqicn.org) API"""
    
    BASE_URL = "https://api.waqi.info"
    
    def __init__(self, api_key: str = None, user=None):
        # Try to get key from database first
        if not api_key:
            api_key = get_api_key_for_provider('waqi', user)
        self.api_key = api_key
    
    def get_by_city(self, city: str):
        """Get air quality data by city name"""
        if not self.api_key:
            logger.error("WAQI API key not configured")
            return None
            
        url = f"{self.BASE_URL}/feed/{city}/"
        
        params = {
            "token": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return self._parse_data(data['data'])
            else:
                logger.error(f"WAQI API error: {data.get('data', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch WAQI data: {e}")
            return None
    
    def get_by_coordinates(self, lat: float, lon: float):
        """Get air quality data by coordinates"""
        if not self.api_key:
            logger.error("WAQI API key not configured")
            return None
            
        url = f"{self.BASE_URL}/feed/geo:{lat};{lon}/"
        
        params = {
            "token": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return self._parse_data(data['data'])
            else:
                logger.error(f"WAQI API error: {data.get('data', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch WAQI data: {e}")
            return None
    
    def search_stations(self, keyword: str):
        """Search for air quality stations"""
        if not self.api_key:
            return None
            
        url = f"{self.BASE_URL}/search/"
        
        params = {
            "keyword": keyword,
            "token": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return data['data']
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search WAQI: {e}")
            return None
    
    def _parse_data(self, data: dict):
        """Parse WAQI API response"""
        if not data:
            return None
        
        # Extract coordinates
        city = data.get('city', {})
        geo = city.get('geo', [0, 0])
        
        # Extract pollutants from iaqi
        iaqi = data.get('iaqi', {})
        
        result = {
            'latitude': geo[0] if len(geo) > 0 else None,
            'longitude': geo[1] if len(geo) > 1 else None,
            'location_name': city.get('name', ''),
            'aqi': data.get('aqi'),
            'pm25': iaqi.get('pm25', {}).get('v'),
            'pm10': iaqi.get('pm10', {}).get('v'),
            'o3': iaqi.get('o3', {}).get('v'),
            'no2': iaqi.get('no2', {}).get('v'),
            'so2': iaqi.get('so2', {}).get('v'),
            'co': iaqi.get('co', {}).get('v'),
            'observed_at': datetime.now(),
            'source': 'waqi',
            'dominant_pollutant': data.get('dominentpol', ''),
        }
        
        # Try to parse time
        time_info = data.get('time', {})
        if time_info.get('iso'):
            try:
                result['observed_at'] = datetime.fromisoformat(
                    time_info['iso'].replace('Z', '+00:00')
                )
            except:
                pass
        
        return result


def get_aqi_level(aqi: int):
    """Get AQI level description in Vietnamese"""
    if aqi is None:
        return {'level': 'unknown', 'label': 'Không xác định', 'color': 'gray'}
    
    if aqi <= 50:
        return {'level': 'good', 'label': 'Tốt', 'color': 'green'}
    elif aqi <= 100:
        return {'level': 'moderate', 'label': 'Trung bình', 'color': 'yellow'}
    elif aqi <= 150:
        return {'level': 'unhealthy_sensitive', 'label': 'Không tốt cho nhóm nhạy cảm', 'color': 'orange'}
    elif aqi <= 200:
        return {'level': 'unhealthy', 'label': 'Không tốt', 'color': 'red'}
    elif aqi <= 300:
        return {'level': 'very_unhealthy', 'label': 'Rất không tốt', 'color': 'purple'}
    else:
        return {'level': 'hazardous', 'label': 'Nguy hại', 'color': 'maroon'}
