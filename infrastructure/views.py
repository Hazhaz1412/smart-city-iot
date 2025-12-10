from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Sum, Avg
from .models import WaterSupplyPoint, DrainagePoint, StreetLight, EnergyMeter, TelecomTower
from .serializers import WaterSupplyPointSerializer, DrainagePointSerializer, StreetLightSerializer, EnergyMeterSerializer, TelecomTowerSerializer


class WaterSupplyPointViewSet(viewsets.ModelViewSet):
    queryset = WaterSupplyPoint.objects.all()
    serializer_class = WaterSupplyPointSerializer
    
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
        total = WaterSupplyPoint.objects.count()
        total_capacity = WaterSupplyPoint.objects.aggregate(sum=Sum("capacity"))["sum"] or 0
        total_current = WaterSupplyPoint.objects.aggregate(sum=Sum("current_level"))["sum"] or 0
        by_type = list(WaterSupplyPoint.objects.values("point_type").annotate(count=Count("id")))
        by_status = list(WaterSupplyPoint.objects.values("status").annotate(count=Count("id")))
        return Response({"total_points": total, "total_capacity": total_capacity, "current_storage": total_current, "by_type": by_type, "by_status": by_status})


class DrainagePointViewSet(viewsets.ModelViewSet):
    queryset = DrainagePoint.objects.all()
    serializer_class = DrainagePointSerializer
    
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
        total = DrainagePoint.objects.count()
        by_type = list(DrainagePoint.objects.values("point_type").annotate(count=Count("id")))
        by_status = list(DrainagePoint.objects.values("status").annotate(count=Count("id")))
        by_flood_risk = list(DrainagePoint.objects.values("flood_risk").annotate(count=Count("id")))
        return Response({"total_points": total, "critical_count": DrainagePoint.objects.filter(status="critical").count(), "by_type": by_type, "by_status": by_status, "by_flood_risk": by_flood_risk})


class StreetLightViewSet(viewsets.ModelViewSet):
    queryset = StreetLight.objects.all()
    serializer_class = StreetLightSerializer
    
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
        total = StreetLight.objects.count()
        smart_count = StreetLight.objects.filter(is_smart=True).count()
        total_energy = StreetLight.objects.aggregate(sum=Sum("energy_consumed_today"))["sum"] or 0
        by_status = list(StreetLight.objects.values("status").annotate(count=Count("id")))
        return Response({"total_lights": total, "smart_lights": smart_count, "total_energy_today": total_energy, "by_status": by_status})
    
    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None):
        light = self.get_object()
        if light.status == "on":
            light.status = "off"
        elif light.status == "off":
            light.status = "on"
        else:
            return Response({"error": "Cannot toggle in current status"}, status=400)
        light.save()
        return Response({"status": light.status})


class EnergyMeterViewSet(viewsets.ModelViewSet):
    queryset = EnergyMeter.objects.all()
    serializer_class = EnergyMeterSerializer
    
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
        total = EnergyMeter.objects.count()
        total_power = EnergyMeter.objects.aggregate(sum=Sum("current_power"))["sum"] or 0
        total_today = EnergyMeter.objects.aggregate(sum=Sum("today_consumption"))["sum"] or 0
        by_type = list(EnergyMeter.objects.values("meter_type").annotate(count=Count("id")))
        by_status = list(EnergyMeter.objects.values("status").annotate(count=Count("id")))
        return Response({"total_meters": total, "total_current_power": round(total_power, 2), "total_consumption_today": round(total_today, 2), "by_type": by_type, "by_status": by_status})


class TelecomTowerViewSet(viewsets.ModelViewSet):
    queryset = TelecomTower.objects.all()
    serializer_class = TelecomTowerSerializer
    
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
        total = TelecomTower.objects.count()
        total_connections = TelecomTower.objects.aggregate(sum=Sum("active_connections"))["sum"] or 0
        max_connections = TelecomTower.objects.aggregate(sum=Sum("max_connections"))["sum"] or 0
        by_type = list(TelecomTower.objects.values("tower_type").annotate(count=Count("id")))
        by_provider = list(TelecomTower.objects.values("provider").annotate(count=Count("id")))
        return Response({"total_towers": total, "total_active_connections": total_connections, "by_type": by_type, "by_provider": by_provider})


class InfrastructureSummaryViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        city = request.query_params.get("city")
        water_qs = WaterSupplyPoint.objects.all()
        drainage_qs = DrainagePoint.objects.all()
        lights_qs = StreetLight.objects.all()
        energy_qs = EnergyMeter.objects.all()
        telecom_qs = TelecomTower.objects.all()
        if city:
            water_qs = water_qs.filter(city__icontains=city)
            drainage_qs = drainage_qs.filter(city__icontains=city)
            lights_qs = lights_qs.filter(city__icontains=city)
            energy_qs = energy_qs.filter(city__icontains=city)
            telecom_qs = telecom_qs.filter(city__icontains=city)
        water_capacity = water_qs.aggregate(sum=Sum("capacity"))["sum"] or 0
        water_current = water_qs.aggregate(sum=Sum("current_level"))["sum"] or 0
        total_energy = energy_qs.aggregate(sum=Sum("current_power"))["sum"] or 0
        total_connections = telecom_qs.aggregate(sum=Sum("active_connections"))["sum"] or 0
        return Response({
            "water_supply": {"total_points": water_qs.count(), "operational": water_qs.filter(status="operational").count(), "capacity": water_capacity, "current_level": water_current},
            "drainage": {"total_points": drainage_qs.count(), "normal": drainage_qs.filter(status="normal").count(), "critical": drainage_qs.filter(status="critical").count()},
            "street_lights": {"total": lights_qs.count(), "on": lights_qs.filter(status="on").count(), "smart_lights": lights_qs.filter(is_smart=True).count()},
            "energy": {"total_meters": energy_qs.count(), "total_current_power": round(total_energy, 2)},
            "telecom": {"total_towers": telecom_qs.count(), "active": telecom_qs.filter(status="active").count(), "total_connections": total_connections}
        })
