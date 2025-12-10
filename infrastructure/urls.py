from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterSupplyPointViewSet, DrainagePointViewSet, StreetLightViewSet, EnergyMeterViewSet, TelecomTowerViewSet, InfrastructureSummaryViewSet

router = DefaultRouter()
router.register(r"water-supply", WaterSupplyPointViewSet, basename="water-supply")
router.register(r"drainage", DrainagePointViewSet, basename="drainage")
router.register(r"street-lights", StreetLightViewSet, basename="street-light")
router.register(r"energy", EnergyMeterViewSet, basename="energy")
router.register(r"telecom", TelecomTowerViewSet, basename="telecom")
router.register(r"summary", InfrastructureSummaryViewSet, basename="infrastructure-summary")

urlpatterns = [
    path("", include(router.urls)),
]
