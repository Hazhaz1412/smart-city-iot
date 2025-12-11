from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import (
    Observation,
    WeatherObservation,
    AirQualityObservation,
    TrafficObservation
)
from .serializers import (
    ObservationSerializer,
    WeatherObservationSerializer,
    AirQualityObservationSerializer,
    TrafficObservationSerializer,
    WeatherObservationNGSILDSerializer,
    AirQualityObservationNGSILDSerializer
)


class ObservationViewSet(viewsets.ModelViewSet):
    """ViewSet for Observations"""
    
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    
    def get_queryset(self):
        """Filter observations"""
        queryset = Observation.objects.all()
        
        sensor_id = self.request.query_params.get('sensor', None)
        if sensor_id:
            queryset = queryset.filter(sensor_id=sensor_id)
        
        property_name = self.request.query_params.get('property', None)
        if property_name:
            queryset = queryset.filter(observed_property=property_name)
        
        # Time range filter
        start_time = self.request.query_params.get('start', None)
        end_time = self.request.query_params.get('end', None)
        
        if start_time:
            queryset = queryset.filter(result_time__gte=start_time)
        
        if end_time:
            queryset = queryset.filter(result_time__lte=end_time)
        
        return queryset


class WeatherObservationViewSet(viewsets.ModelViewSet):
    """ViewSet for Weather Observations"""
    
    queryset = WeatherObservation.objects.all()
    serializer_class = WeatherObservationSerializer
    
    def get_queryset(self):
        """Filter weather observations"""
        queryset = WeatherObservation.objects.all()
        
        # Time range filter
        hours = self.request.query_params.get('hours', None)
        if hours:
            cutoff = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(observed_at__gte=cutoff)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest weather observation"""
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        
        queryset = WeatherObservation.objects.all()
        
        if lat and lon:
            # Find nearest location
            lat = float(lat)
            lon = float(lon)
            radius = 0.5  # ~50km
            
            queryset = queryset.filter(
                latitude__range=(lat - radius, lat + radius),
                longitude__range=(lon - radius, lon + radius)
            )
        
        observation = queryset.order_by('-observed_at').first()
        
        if observation:
            serializer = self.get_serializer(observation)
            return Response(serializer.data)
        else:
            return Response({'message': 'No data found'}, status=404)
    
    @action(detail=False, methods=['get'], url_path='ngsi-ld')
    def ngsi_ld(self, request):
        """Get weather observations in NGSI-LD format"""
        queryset = self.get_queryset()
        serializer = WeatherObservationNGSILDSerializer(queryset, many=True)
        return Response(serializer.data, content_type='application/ld+json')
    
    @action(detail=True, methods=['get'], url_path='ngsi-ld')
    def ngsi_ld_detail(self, request, pk=None):
        """Get single weather observation in NGSI-LD format"""
        instance = self.get_object()
        serializer = WeatherObservationNGSILDSerializer(instance)
        return Response(serializer.data, content_type='application/ld+json')


class AirQualityObservationViewSet(viewsets.ModelViewSet):
    """ViewSet for Air Quality Observations"""
    
    queryset = AirQualityObservation.objects.all()
    serializer_class = AirQualityObservationSerializer
    
    def get_queryset(self):
        """Filter air quality observations"""
        queryset = AirQualityObservation.objects.all()
        
        # Time range filter
        hours = self.request.query_params.get('hours', None)
        if hours:
            cutoff = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(observed_at__gte=cutoff)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest air quality observation"""
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        
        queryset = AirQualityObservation.objects.all()
        
        if lat and lon:
            # Find nearest location
            lat = float(lat)
            lon = float(lon)
            radius = 0.5
            
            queryset = queryset.filter(
                latitude__range=(lat - radius, lat + radius),
                longitude__range=(lon - radius, lon + radius)
            )
        
        observation = queryset.order_by('-observed_at').first()
        
        if observation:
            serializer = self.get_serializer(observation)
            return Response(serializer.data)
        else:
            return Response({'message': 'No data found'}, status=404)
    
    @action(detail=False, methods=['get'], url_path='ngsi-ld')
    def ngsi_ld(self, request):
        """Get air quality observations in NGSI-LD format"""
        queryset = self.get_queryset()
        serializer = AirQualityObservationNGSILDSerializer(queryset, many=True)
        return Response(serializer.data, content_type='application/ld+json')
    
    @action(detail=True, methods=['get'], url_path='ngsi-ld')
    def ngsi_ld_detail(self, request, pk=None):
        """Get single air quality observation in NGSI-LD format"""
        instance = self.get_object()
        serializer = AirQualityObservationNGSILDSerializer(instance)
        return Response(serializer.data, content_type='application/ld+json')


class TrafficObservationViewSet(viewsets.ModelViewSet):
    """ViewSet for Traffic Observations"""
    
    queryset = TrafficObservation.objects.all()
    serializer_class = TrafficObservationSerializer
    
    def get_queryset(self):
        """Filter traffic observations"""
        queryset = TrafficObservation.objects.all()
        
        # Time range filter
        hours = self.request.query_params.get('hours', None)
        if hours:
            cutoff = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(observed_at__gte=cutoff)
        
        return queryset
