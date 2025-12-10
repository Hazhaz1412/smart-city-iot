from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusStationViewSet, TrafficFlowViewSet, TrafficIncidentViewSet, ParkingSpotViewSet, TrafficSummaryViewSet

router = DefaultRouter()
router.register(r"bus-stations", BusStationViewSet, basename="bus-station")
router.register(r"traffic-flows", TrafficFlowViewSet, basename="traffic-flow")
router.register(r"incidents", TrafficIncidentViewSet, basename="incident")
router.register(r"parking", ParkingSpotViewSet, basename="parking")
router.register(r"summary", TrafficSummaryViewSet, basename="traffic-summary")

urlpatterns = [
    path("", include(router.urls)),
]
