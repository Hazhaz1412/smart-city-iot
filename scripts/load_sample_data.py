"""
Sample data loading script
"""
from entities.models import WeatherStation, AirQualitySensor, PublicService
from django.utils import timezone

print("Loading sample data...")

# Weather Stations in Vietnam
weather_stations = [
    {
        "station_id": "hanoi-station-1",
        "name": "Trạm Thời tiết Hà Nội - Đống Đa",
        "latitude": 21.0285,
        "longitude": 105.8542,
        "address": "Đống Đa, Hà Nội, Việt Nam"
    },
    {
        "station_id": "hcm-station-1",
        "name": "Trạm Thời tiết TP.HCM - Quận 1",
        "latitude": 10.7769,
        "longitude": 106.7009,
        "address": "Quận 1, TP.HCM, Việt Nam"
    },
    {
        "station_id": "danang-station-1",
        "name": "Trạm Thời tiết Đà Nẵng",
        "latitude": 16.0544,
        "longitude": 108.2022,
        "address": "Hải Châu, Đà Nẵng, Việt Nam"
    }
]

for data in weather_stations:
    station, created = WeatherStation.objects.get_or_create(
        station_id=data['station_id'],
        defaults=data
    )
    if created:
        print(f"Created weather station: {station.name}")

# Air Quality Sensors
air_quality_sensors = [
    {
        "sensor_id": "hanoi-aq-1",
        "name": "Cảm biến Chất lượng Không khí Hà Nội - Hoàn Kiếm",
        "latitude": 21.0285,
        "longitude": 105.8542,
        "address": "Hoàn Kiếm, Hà Nội, Việt Nam"
    },
    {
        "sensor_id": "hcm-aq-1",
        "name": "Cảm biến Chất lượng Không khí TP.HCM - Q1",
        "latitude": 10.7769,
        "longitude": 106.7009,
        "address": "Quận 1, TP.HCM, Việt Nam"
    }
]

for data in air_quality_sensors:
    sensor, created = AirQualitySensor.objects.get_or_create(
        sensor_id=data['sensor_id'],
        defaults=data
    )
    if created:
        print(f"Created air quality sensor: {sensor.name}")

# Public Services
public_services = [
    {
        "service_id": "hanoi-park-1",
        "name": "Công viên Thống Nhất",
        "service_type": "park",
        "description": "Công viên lớn ở trung tâm Hà Nội",
        "latitude": 21.0167,
        "longitude": 105.8406,
        "address": "Hai Bà Trưng, Hà Nội",
        "opening_hours": "05:00-22:00"
    },
    {
        "service_id": "hanoi-parking-1",
        "name": "Bãi đỗ xe Vincom Bà Triệu",
        "service_type": "parking",
        "latitude": 21.0155,
        "longitude": 105.8458,
        "address": "191 Bà Triệu, Hà Nội"
    },
    {
        "service_id": "hcm-park-1",
        "name": "Công viên 23/9",
        "service_type": "park",
        "description": "Công viên lịch sử ở TP.HCM",
        "latitude": 10.7696,
        "longitude": 106.6593,
        "address": "Phạm Ngũ Lão, Quận 1, TP.HCM",
        "opening_hours": "05:00-21:00"
    }
]

for data in public_services:
    service, created = PublicService.objects.get_or_create(
        service_id=data['service_id'],
        defaults=data
    )
    if created:
        print(f"Created public service: {service.name}")

print("Sample data loaded successfully!")
