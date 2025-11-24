from rest_framework import viewsets
from .models import Sensor, Platform, SensorDeployment
from .serializers import (
    SensorSerializer,
    PlatformSerializer,
    SensorDeploymentSerializer
)


class SensorViewSet(viewsets.ModelViewSet):
    """ViewSet for Sensors"""
    
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    
    def get_queryset(self):
        """Filter by sensor type"""
        queryset = Sensor.objects.all()
        sensor_type = self.request.query_params.get('type', None)
        
        if sensor_type:
            queryset = queryset.filter(sensor_type=sensor_type)
        
        return queryset


class PlatformViewSet(viewsets.ModelViewSet):
    """ViewSet for Platforms"""
    
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class SensorDeploymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Sensor Deployments"""
    
    queryset = SensorDeployment.objects.all()
    serializer_class = SensorDeploymentSerializer
