"""
Integration with OpenAQ API
"""
import requests
from datetime import datetime
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class OpenAQClient:
    """Client for OpenAQ API v3"""
    
    BASE_URL = "https://api.openaq.org/v3"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENAQ_API_KEY
    
    def get_latest_measurements(
        self,
        lat: float,
        lon: float,
        radius: float = 10000
    ):
        """Get latest air quality measurements near a location"""
        url = f"{self.BASE_URL}/locations"
        
        # OpenAQ v3 uses radius in km, coordinates as separate params
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": int(radius / 1000),  # Convert meters to km
            "limit": 10,
            "order_by": "distance"
        }
        
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                # Get the latest measurements for the closest location
                location = data['results'][0]
                return self._get_location_latest(location['id'])
            else:
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch air quality data: {e}")
            return None
    
    def _get_location_latest(self, location_id: int):
        """Get latest measurements for a specific location"""
        url = f"{self.BASE_URL}/locations/{location_id}/latest"
        
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results'):
                return self._parse_measurements_v3(data['results'])
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch location latest: {e}")
            return None
    
    def get_measurements_by_location(self, location_id: int):
        """Get measurements by location ID"""
        return self._get_location_latest(location_id)
    
    def _parse_measurements_v3(self, results: list):
        """Parse air quality measurements from v3 API"""
        if not results:
            return None
        
        measurements = {}
        latest_time = None
        location_name = None
        coords = {'latitude': None, 'longitude': None}
        
        for result in results:
            param = result.get('parameter', {})
            param_name = param.get('name', '').lower()
            value = result.get('value')
            
            # Map parameter names
            param_map = {
                'pm2.5': 'pm25',
                'pm10': 'pm10',
                'no2': 'no2',
                'o3': 'o3',
                'co': 'co',
                'so2': 'so2'
            }
            
            if param_name in param_map:
                measurements[param_map[param_name]] = value
            
            # Get timestamp from first result
            if not latest_time and result.get('datetime'):
                try:
                    latest_time = datetime.fromisoformat(
                        result['datetime'].get('utc', '').replace('Z', '+00:00')
                    )
                except:
                    latest_time = datetime.now()
            
            # Get location info from first result
            if not location_name:
                location = result.get('location', {})
                location_name = location.get('name', '')
                coordinates = location.get('coordinates', {})
                coords['latitude'] = coordinates.get('latitude')
                coords['longitude'] = coordinates.get('longitude')
        
        return {
            'latitude': coords['latitude'],
            'longitude': coords['longitude'],
            'location_name': location_name,
            'pm25': measurements.get('pm25'),
            'pm10': measurements.get('pm10'),
            'no2': measurements.get('no2'),
            'o3': measurements.get('o3'),
            'co': measurements.get('co'),
            'so2': measurements.get('so2'),
            'observed_at': latest_time or datetime.now(),
            'source': 'openaq'
        }


def calculate_aqi_from_pm25(pm25: float) -> float:
    """Calculate AQI from PM2.5 concentration (US EPA standard)"""
    if pm25 <= 12.0:
        return linear_scale(pm25, 0, 12.0, 0, 50)
    elif pm25 <= 35.4:
        return linear_scale(pm25, 12.1, 35.4, 51, 100)
    elif pm25 <= 55.4:
        return linear_scale(pm25, 35.5, 55.4, 101, 150)
    elif pm25 <= 150.4:
        return linear_scale(pm25, 55.5, 150.4, 151, 200)
    elif pm25 <= 250.4:
        return linear_scale(pm25, 150.5, 250.4, 201, 300)
    elif pm25 <= 350.4:
        return linear_scale(pm25, 250.5, 350.4, 301, 400)
    else:
        return linear_scale(pm25, 350.5, 500.4, 401, 500)


def linear_scale(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float
) -> float:
    """Linear interpolation"""
    return ((value - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min
