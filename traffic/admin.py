from django.contrib import admin
from .models import BusStation, TrafficFlow, TrafficIncident, ParkingSpot


@admin.register(BusStation)
class BusStationAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "name", "station_type", "status", "city", "created_at"]
    list_filter = ["station_type", "status", "city"]
    search_fields = ["entity_id", "name", "city"]


@admin.register(TrafficFlow)
class TrafficFlowAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "road_name", "congestion_level", "average_speed", "city", "observed_at"]
    list_filter = ["congestion_level", "city"]
    search_fields = ["entity_id", "road_name", "city"]


@admin.register(TrafficIncident)
class TrafficIncidentAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "title", "incident_type", "severity", "status", "city", "reported_at"]
    list_filter = ["incident_type", "severity", "status", "city"]
    search_fields = ["entity_id", "title", "city"]


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "name", "parking_type", "total_spaces", "available_spaces", "status", "city"]
    list_filter = ["parking_type", "status", "city"]
    search_fields = ["entity_id", "name", "city"]
