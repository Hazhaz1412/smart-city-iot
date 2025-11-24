from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import (
    sync_weather_data,
    sync_air_quality_data,
    sync_single_location_weather,
    sync_single_location_air_quality
)
from .openweather import OpenWeatherMapClient
from .openaq import OpenAQClient
import logging

logger = logging.getLogger(__name__)


class WeatherSyncView(APIView):
    """Trigger weather data sync"""
    
    def post(self, request):
        """Start weather sync task"""
        task = sync_weather_data.delay()
        
        return Response({
            'status': 'started',
            'task_id': task.id,
            'message': 'Weather data synchronization started'
        })


class AirQualitySyncView(APIView):
    """Trigger air quality data sync"""
    
    def post(self, request):
        """Start air quality sync task"""
        task = sync_air_quality_data.delay()
        
        return Response({
            'status': 'started',
            'task_id': task.id,
            'message': 'Air quality data synchronization started'
        })


class SingleLocationWeatherView(APIView):
    """Get weather data for a single location"""
    
    def get(self, request):
        """Fetch weather data"""
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        city = request.query_params.get('city')
        
        if not ((lat and lon) or city):
            return Response({
                'error': 'Either lat/lon or city is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        client = OpenWeatherMapClient()
        
        try:
            if city:
                data = client.get_weather_by_city(city)
            else:
                data = client.get_current_weather(float(lat), float(lon))
            
            if data:
                return Response(data)
            else:
                return Response({
                    'error': 'No data found'
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to fetch weather: {e}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Save weather data to database"""
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        location_name = request.data.get('location_name', '')
        
        if not (lat and lon):
            return Response({
                'error': 'lat and lon are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task = sync_single_location_weather.delay(
            float(lat),
            float(lon),
            location_name
        )
        
        return Response({
            'status': 'started',
            'task_id': task.id,
            'message': 'Weather data fetch started'
        })


class SingleLocationAirQualityView(APIView):
    """Get air quality data for a single location"""
    
    def get(self, request):
        """Fetch air quality data"""
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        
        if not (lat and lon):
            return Response({
                'error': 'lat and lon are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        client = OpenAQClient()
        
        try:
            data = client.get_latest_measurements(float(lat), float(lon))
            
            if data:
                return Response(data)
            else:
                return Response({
                    'error': 'No data found'
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to fetch air quality: {e}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Save air quality data to database"""
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        location_name = request.data.get('location_name', '')
        
        if not (lat and lon):
            return Response({
                'error': 'lat and lon are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task = sync_single_location_air_quality.delay(
            float(lat),
            float(lon),
            location_name
        )
        
        return Response({
            'status': 'started',
            'task_id': task.id,
            'message': 'Air quality data fetch started'
        })
