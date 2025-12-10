from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .openweather import OpenWeatherMapClient
from .openaq import OpenAQClient, calculate_aqi_from_pm25
from observations.models import WeatherObservation, AirQualityObservation
from entities.models import WeatherStation, AirQualitySensor
import logging

logger = logging.getLogger(__name__)


class WeatherSyncView(APIView):
    """Trigger weather data sync"""
    
    def post(self, request):
        """Sync weather data directly (no Celery)"""
        # Get optional lat/lon from request, default to Hanoi
        lat = request.data.get('lat', 21.0285)
        lon = request.data.get('lon', 105.8542)
        
        client = OpenWeatherMapClient()
        
        try:
            # Fetch weather data
            weather_data = client.get_current_weather(float(lat), float(lon))
            
            if weather_data:
                # Save to database
                obs_id = f"weather-sync-{int(timezone.now().timestamp())}"
                
                observation = WeatherObservation.objects.create(
                    observation_id=obs_id,
                    **weather_data
                )
                
                logger.info(f"Created weather observation: {obs_id}")
                
                return Response({
                    'status': 'success',
                    'message': 'Weather data synchronized successfully',
                    'observation_id': obs_id,
                    'data': weather_data
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'No weather data found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Failed to sync weather: {e}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AirQualitySyncView(APIView):
    """Trigger air quality data sync"""
    
    def post(self, request):
        """Sync air quality data directly - try WAQI first, fallback to OpenAQ"""
        # Get optional lat/lon from request, default to Hanoi
        lat = request.data.get('lat', 21.0285)
        lon = request.data.get('lon', 105.8542)
        city = request.data.get('city', 'hanoi')
        
        aq_data = None
        source_used = None
        
        # Try WAQI first (better coverage for Vietnam)
        try:
            from .waqi import WAQIClient
            waqi_client = WAQIClient(user=request.user if request.user.is_authenticated else None)
            
            if waqi_client.api_key:
                # Try by coordinates first
                aq_data = waqi_client.get_by_coordinates(float(lat), float(lon))
                
                # If no data, try by city name
                if not aq_data and city:
                    aq_data = waqi_client.get_by_city(city)
                
                if aq_data:
                    source_used = 'WAQI'
        except Exception as e:
            logger.warning(f"WAQI fetch failed: {e}")
        
        # Fallback to OpenAQ if WAQI didn't work
        if not aq_data:
            try:
                client = OpenAQClient()
                aq_data = client.get_latest_measurements(float(lat), float(lon))
                if aq_data:
                    source_used = 'OpenAQ'
                    # Calculate AQI if not provided
                    if aq_data.get('pm25') and not aq_data.get('aqi'):
                        aq_data['aqi'] = calculate_aqi_from_pm25(aq_data['pm25'])
            except Exception as e:
                logger.warning(f"OpenAQ fetch failed: {e}")
        
        if aq_data:
            try:
                # Save to database
                obs_id = f"airquality-sync-{int(timezone.now().timestamp())}"
                
                # Remove non-model fields
                save_data = {k: v for k, v in aq_data.items() if k not in ['dominant_pollutant']}
                
                observation = AirQualityObservation.objects.create(
                    observation_id=obs_id,
                    **save_data
                )
                
                logger.info(f"Created air quality observation from {source_used}: {obs_id}")
                
                return Response({
                    'status': 'success',
                    'message': f'Air quality data synchronized from {source_used}',
                    'source': source_used,
                    'observation_id': obs_id,
                    'data': aq_data
                })
            except Exception as e:
                logger.error(f"Failed to save air quality data: {e}")
                return Response({
                    'status': 'error',
                    'message': f'Data fetched but save failed: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'status': 'error',
                'message': 'No air quality data found. Please add a WAQI API key in API Settings.'
            }, status=status.HTTP_404_NOT_FOUND)


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


# ============ API Key Management Views ============

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import ExternalAPIProvider, UserAPIKey, SystemAPIKey
from .serializers import (
    ExternalAPIProviderSerializer,
    ExternalAPIProviderAdminSerializer,
    UserAPIKeySerializer,
    UserAPIKeyCreateSerializer,
    SystemAPIKeySerializer,
    SystemAPIKeyCreateSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read-only access for authenticated users, write access for admins"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff


class ExternalAPIProviderViewSet(viewsets.ModelViewSet):
    """
    API Providers management
    - GET: List all providers (all authenticated users)
    - POST/PUT/DELETE: Admin only
    """
    queryset = ExternalAPIProvider.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ExternalAPIProviderAdminSerializer
        return ExternalAPIProviderSerializer
    
    def get_queryset(self):
        queryset = ExternalAPIProvider.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of available categories"""
        return Response([
            {'value': c[0], 'label': c[1]} 
            for c in ExternalAPIProvider.CATEGORY_CHOICES
        ])
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_system_key(self, request, pk=None):
        """Set system API key for a provider"""
        provider = self.get_object()
        api_key = request.data.get('api_key')
        
        if not api_key:
            return Response({
                'error': 'api_key is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        system_key, created = SystemAPIKey.objects.get_or_create(provider=provider)
        system_key.api_key = api_key
        system_key.is_active = request.data.get('is_active', True)
        system_key.allow_user_override = request.data.get('allow_user_override', True)
        
        if request.data.get('credentials'):
            system_key.credentials = request.data['credentials']
        
        system_key.save()
        
        return Response({
            'status': 'success',
            'message': f'System API key {"created" if created else "updated"} for {provider.name}'
        })


class UserAPIKeyViewSet(viewsets.ModelViewSet):
    """
    User's own API Keys management
    Users can only see and manage their own API keys
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserAPIKeyCreateSerializer
        return UserAPIKeySerializer
    
    def get_queryset(self):
        return UserAPIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_provider(self, request):
        """Get user's API key for a specific provider"""
        provider_slug = request.query_params.get('provider')
        if not provider_slug:
            return Response({
                'error': 'provider query param is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_key = UserAPIKey.objects.get(
                user=request.user,
                provider__slug=provider_slug,
                is_active=True
            )
            return Response(UserAPIKeySerializer(user_key).data)
        except UserAPIKey.DoesNotExist:
            return Response({
                'has_key': False,
                'provider': provider_slug
            })
    
    @action(detail=True, methods=['post'])
    def test_key(self, request, pk=None):
        """Test if the API key is valid"""
        user_key = self.get_object()
        provider = user_key.provider
        
        # Basic test - try to make a simple API call
        import requests
        
        try:
            headers = dict(provider.default_headers) if provider.default_headers else {}
            params = {}
            
            if provider.auth_type == 'api_key_header':
                headers[provider.auth_key_name] = user_key.api_key
            elif provider.auth_type == 'api_key_query':
                params[provider.auth_key_name] = user_key.api_key
            elif provider.auth_type == 'bearer_token':
                headers['Authorization'] = f'Bearer {user_key.api_key}'
            
            # Make a simple GET request to base URL
            response = requests.get(
                provider.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code < 400:
                return Response({
                    'status': 'success',
                    'message': 'API key is valid',
                    'response_code': response.status_code
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'API key may be invalid',
                    'response_code': response.status_code
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SystemAPIKeyViewSet(viewsets.ModelViewSet):
    """
    System API Keys management (Admin only)
    """
    queryset = SystemAPIKey.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SystemAPIKeyCreateSerializer
        return SystemAPIKeySerializer


class LatestWeatherView(APIView):
    """Get latest weather observation"""
    
    def get(self, request):
        """Return latest weather data"""
        try:
            latest = WeatherObservation.objects.order_by('-observed_at').first()
            if latest:
                return Response({
                    'temperature': latest.temperature,
                    'humidity': latest.humidity,
                    'pressure': latest.pressure,
                    'wind_speed': latest.wind_speed,
                    'wind_direction': latest.wind_direction,
                    'description': latest.weather_description,
                    'observed_at': latest.observed_at,
                    'location': latest.location_name,
                })
            return Response(None)
        except Exception as e:
            logger.error(f"Error fetching latest weather: {e}")
            return Response(None)


class LatestAirQualityView(APIView):
    """Get latest air quality observation"""
    
    def get(self, request):
        """Return latest air quality data"""
        try:
            latest = AirQualityObservation.objects.order_by('-observed_at').first()
            if latest:
                return Response({
                    'aqi': latest.aqi,
                    'pm25': latest.pm25,
                    'pm10': latest.pm10,
                    'o3': latest.o3,
                    'no2': latest.no2,
                    'so2': latest.so2,
                    'co': latest.co,
                    'observed_at': latest.observed_at,
                    'station': latest.location_name if hasattr(latest, 'location_name') else None,
                    'dominant_pollutant': 'pm25' if latest.pm25 else None,
                })
            return Response(None)
        except Exception as e:
            logger.error(f"Error fetching latest air quality: {e}")
            return Response(None)
