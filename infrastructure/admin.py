from django.contrib import admin
from .models import WaterSupplyPoint, DrainagePoint, StreetLight, EnergyMeter, TelecomTower


@admin.register(WaterSupplyPoint)
class WaterSupplyPointAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "name", "point_type", "status", "capacity", "current_level", "city"]
    list_filter = ["point_type", "status", "city"]
    search_fields = ["entity_id", "name", "city"]


@admin.register(DrainagePoint)
class DrainagePointAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "name", "point_type", "status", "flood_risk", "city"]
    list_filter = ["point_type", "status", "flood_risk", "city"]
    search_fields = ["entity_id", "name", "city"]


@admin.register(StreetLight)
class StreetLightAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "pole_id", "lamp_type", "status", "brightness_level", "is_smart", "city"]
    list_filter = ["lamp_type", "status", "is_smart", "city"]
    search_fields = ["entity_id", "pole_id", "city"]


@admin.register(EnergyMeter)
class EnergyMeterAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "meter_id", "name", "meter_type", "status", "current_power", "city"]
    list_filter = ["meter_type", "status", "city"]
    search_fields = ["entity_id", "meter_id", "name", "city"]


@admin.register(TelecomTower)
class TelecomTowerAdmin(admin.ModelAdmin):
    list_display = ["entity_id", "tower_id", "name", "tower_type", "provider", "status", "city"]
    list_filter = ["tower_type", "status", "provider", "city"]
    search_fields = ["entity_id", "tower_id", "name", "provider", "city"]
