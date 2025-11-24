from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    Entity,
    WeatherStation,
    AirQualitySensor,
    TrafficSensor,
    PublicService
)
from .serializers import (
    EntitySerializer,
    WeatherStationSerializer,
    AirQualitySensorSerializer,
    TrafficSensorSerializer,
    PublicServiceSerializer
)
from core.orion_client import OrionLDClient
from core.ngsi_ld import (
    create_weather_station_entity,
    create_air_quality_sensor_entity
)
import logging

logger = logging.getLogger(__name__)


class EntityViewSet(viewsets.ModelViewSet):
    """ViewSet for NGSI-LD entities"""
    
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    
    def get_queryset(self):
        """Filter entities by type"""
        queryset = Entity.objects.all()
        entity_type = self.request.query_params.get('type', None)
        
        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def sync_to_orion(self, request, pk=None):
        """Sync entity to Orion-LD"""
        entity = self.get_object()
        client = OrionLDClient()
        
        success = client.create_entity(entity.data)
        
        if success:
            entity.synced_to_orion = True
            entity.last_sync_at = timezone.now()
            entity.save()
            
            return Response({
                'status': 'success',
                'message': 'Entity synced to Orion-LD'
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to sync entity to Orion-LD'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def query_orion(self, request):
        """Query entities from Orion-LD"""
        client = OrionLDClient()
        entity_type = request.query_params.get('type', None)
        
        entities = client.query_entities(entity_type=entity_type)
        
        return Response({
            'count': len(entities),
            'results': entities
        })


class WeatherStationViewSet(viewsets.ModelViewSet):
    """ViewSet for Weather Stations"""
    
    queryset = WeatherStation.objects.all()
    serializer_class = WeatherStationSerializer
    
    def perform_create(self, serializer):
        """Create weather station and NGSI-LD entity"""
        station = serializer.save()
        
        # Create NGSI-LD entity
        ngsi_entity = create_weather_station_entity(
            station_id=station.station_id,
            name=station.name,
            latitude=station.latitude,
            longitude=station.longitude,
            address=station.address
        )
        
        # Save to database
        entity = Entity.objects.create(
            entity_id=ngsi_entity['id'],
            entity_type='WeatherStation',
            data=ngsi_entity,
            latitude=station.latitude,
            longitude=station.longitude
        )
        
        station.entity = entity
        station.save()
        
        # Sync to Orion-LD
        client = OrionLDClient()
        client.create_entity(ngsi_entity)
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Find nearby weather stations"""
        lat = float(request.query_params.get('lat', 0))
        lon = float(request.query_params.get('lon', 0))
        radius = float(request.query_params.get('radius', 10))  # km
        
        # Simple bounding box query
        lat_delta = radius / 111.0
        lon_delta = radius / (111.0 * abs(lat))
        
        stations = WeatherStation.objects.filter(
            latitude__range=(lat - lat_delta, lat + lat_delta),
            longitude__range=(lon - lon_delta, lon + lon_delta),
            is_active=True
        )
        
        serializer = self.get_serializer(stations, many=True)
        return Response(serializer.data)


class AirQualitySensorViewSet(viewsets.ModelViewSet):
    """ViewSet for Air Quality Sensors"""
    
    queryset = AirQualitySensor.objects.all()
    serializer_class = AirQualitySensorSerializer
    
    def perform_create(self, serializer):
        """Create air quality sensor and NGSI-LD entity"""
        sensor = serializer.save()
        
        # Create NGSI-LD entity
        ngsi_entity = create_air_quality_sensor_entity(
            sensor_id=sensor.sensor_id,
            name=sensor.name,
            latitude=sensor.latitude,
            longitude=sensor.longitude
        )
        
        # Save to database
        entity = Entity.objects.create(
            entity_id=ngsi_entity['id'],
            entity_type='AirQualitySensor',
            data=ngsi_entity,
            latitude=sensor.latitude,
            longitude=sensor.longitude
        )
        
        sensor.entity = entity
        sensor.save()
        
        # Sync to Orion-LD
        client = OrionLDClient()
        client.create_entity(ngsi_entity)


class TrafficSensorViewSet(viewsets.ModelViewSet):
    """ViewSet for Traffic Sensors"""
    
    queryset = TrafficSensor.objects.all()
    serializer_class = TrafficSensorSerializer


class PublicServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Public Services"""
    
    queryset = PublicService.objects.all()
    serializer_class = PublicServiceSerializer
    
    def get_queryset(self):
        """Filter by service type"""
        queryset = PublicService.objects.all()
        service_type = self.request.query_params.get('type', None)
        
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Find nearby public services"""
        lat = float(request.query_params.get('lat', 0))
        lon = float(request.query_params.get('lon', 0))
        radius = float(request.query_params.get('radius', 5))  # km
        service_type = request.query_params.get('type', None)
        
        # Simple bounding box query
        lat_delta = radius / 111.0
        lon_delta = radius / (111.0 * abs(lat))
        
        services = PublicService.objects.filter(
            latitude__range=(lat - lat_delta, lat + lat_delta),
            longitude__range=(lon - lon_delta, lon + lon_delta),
            is_active=True
        )
        
        if service_type:
            services = services.filter(service_type=service_type)
        
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)
