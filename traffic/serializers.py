from rest_framework import serializers
from .models import BusStation, TrafficFlow, TrafficIncident, ParkingSpot


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TrafficFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlow
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TrafficIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficIncident
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ParkingSpotSerializer(serializers.ModelSerializer):
    occupancy_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ParkingSpot
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "occupancy_rate"]
