from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Avg
from .models import BusStation, TrafficFlow, TrafficIncident, ParkingSpot
from .serializers import BusStationSerializer, TrafficFlowSerializer, TrafficIncidentSerializer, ParkingSpotSerializer


class BusStationViewSet(viewsets.ModelViewSet):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'statistics']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        total = BusStation.objects.count()
        by_status = list(BusStation.objects.values("status").annotate(count=Count("id")))
        by_city = list(BusStation.objects.values("city").annotate(count=Count("id")))
        return Response({"total": total, "by_status": by_status, "by_city": by_city})


class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'statistics']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        total = TrafficFlow.objects.count()
        avg_speed = TrafficFlow.objects.aggregate(avg=Avg("average_speed"))["avg"] or 0
        by_congestion = list(TrafficFlow.objects.values("congestion_level").annotate(count=Count("id")))
        return Response({"total": total, "average_speed": round(avg_speed, 2), "by_congestion_level": by_congestion})


class TrafficIncidentViewSet(viewsets.ModelViewSet):
    queryset = TrafficIncident.objects.all()
    serializer_class = TrafficIncidentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'statistics']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        total = TrafficIncident.objects.count()
        active = TrafficIncident.objects.exclude(status="resolved").count()
        by_type = list(TrafficIncident.objects.values("incident_type").annotate(count=Count("id")))
        by_severity = list(TrafficIncident.objects.values("severity").annotate(count=Count("id")))
        return Response({"total": total, "active_incidents": active, "by_type": by_type, "by_severity": by_severity})


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'statistics']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        total_lots = ParkingSpot.objects.count()
        total_spaces = sum(ParkingSpot.objects.values_list("total_spaces", flat=True))
        available_spaces = sum(ParkingSpot.objects.values_list("available_spaces", flat=True))
        occupancy = round(((total_spaces - available_spaces) / total_spaces * 100), 2) if total_spaces > 0 else 0
        return Response({"total_lots": total_lots, "total_spaces": total_spaces, "available_spaces": available_spaces, "occupancy_rate": occupancy})


class TrafficSummaryViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        city = request.query_params.get("city")
        stations_qs = BusStation.objects.all()
        flows_qs = TrafficFlow.objects.all()
        incidents_qs = TrafficIncident.objects.all()
        parking_qs = ParkingSpot.objects.all()
        if city:
            stations_qs = stations_qs.filter(city__icontains=city)
            flows_qs = flows_qs.filter(city__icontains=city)
            incidents_qs = incidents_qs.filter(city__icontains=city)
            parking_qs = parking_qs.filter(city__icontains=city)
        avg_speed = flows_qs.aggregate(avg=Avg("average_speed"))["avg"] or 0
        total_parking = sum(parking_qs.values_list("total_spaces", flat=True))
        available_parking = sum(parking_qs.values_list("available_spaces", flat=True))
        return Response({
            "bus_stations": {"total": stations_qs.count(), "active": stations_qs.filter(status="active").count()},
            "traffic_flow": {"average_speed": round(avg_speed, 2)},
            "incidents": {"total": incidents_qs.count(), "active": incidents_qs.exclude(status="resolved").count()},
            "parking": {"total_lots": parking_qs.count(), "total_spaces": total_parking, "available_spaces": available_parking}
        })
