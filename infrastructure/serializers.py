from rest_framework import serializers
from .models import WaterSupplyPoint, DrainagePoint, StreetLight, EnergyMeter, TelecomTower


class WaterSupplyPointSerializer(serializers.ModelSerializer):
    fill_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WaterSupplyPoint
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_fill_percentage(self, obj):
        if obj.capacity == 0:
            return 0
        return round((obj.current_level / obj.capacity) * 100, 2)


class DrainagePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrainagePoint
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class StreetLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetLight
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class EnergyMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyMeter
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TelecomTowerSerializer(serializers.ModelSerializer):
    utilization_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = TelecomTower
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_utilization_rate(self, obj):
        if obj.max_connections == 0:
            return 0
        return round((obj.active_connections / obj.max_connections) * 100, 2)
