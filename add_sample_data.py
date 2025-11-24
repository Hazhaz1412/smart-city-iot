#!/usr/bin/env python
"""Add sample data to the database"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity.settings')
django.setup()

from entities.models import WeatherStation, AirQualitySensor, PublicService
from observations.models import WeatherObservation, AirQualityObservation

def create_weather_stations():
    stations = [
        {
            'station_id': 'hanoi-center-001',
            'name': 'Trạm Hà Nội Trung tâm',
            'address': 'Hoàn Kiếm, Hà Nội',
            'latitude': 21.0285,
            'longitude': 105.8542,
        },
        {
            'station_id': 'ho-tay-002',
            'name': 'Trạm Hồ Tây',
            'address': 'Tây Hồ, Hà Nội',
            'latitude': 21.0583,
            'longitude': 105.8189,
        },
        {
            'station_id': 'cau-giay-003',
            'name': 'Trạm Cầu Giấy',
            'address': 'Cầu Giấy, Hà Nội',
            'latitude': 21.0333,
            'longitude': 105.7944,
        },
    ]
    
    for data in stations:
        station, created = WeatherStation.objects.get_or_create(
            station_id=data['station_id'],
            defaults=data
        )
        if created:
            print(f"✅ Created weather station: {station.name}")
            
            # Add some observations
            now = datetime.now()
            for i in range(5):
                obs_time = now - timedelta(hours=i)
                WeatherObservation.objects.create(
                    observation_id=f"weather-{station.id}-{i}",
                    location_name=station.name,
                    latitude=station.latitude,
                    longitude=station.longitude,
                    temperature=25 + i * 0.5,
                    humidity=65 + i * 2,
                    pressure=1013 - i,
                    wind_speed=5.0 + i * 0.3,
                    wind_direction=180 + i * 10,
                    observed_at=obs_time,
                    source='sample'
                )
            print("  Added 5 observations")

def create_air_quality_sensors():
    sensors = [
        {
            'sensor_id': 'aqi-hanoi-001',
            'name': 'Cảm biến CK Hà Nội',
            'address': 'Hoàn Kiếm, Hà Nội',
            'latitude': 21.0285,
            'longitude': 105.8542,
        },
        {
            'sensor_id': 'aqi-caugiay-002',
            'name': 'Cảm biến CK Cầu Giấy',
            'address': 'Cầu Giấy, Hà Nội',
            'latitude': 21.0333,
            'longitude': 105.7944,
        },
    ]
    
    for data in sensors:
        sensor, created = AirQualitySensor.objects.get_or_create(
            sensor_id=data['sensor_id'],
            defaults=data
        )
        if created:
            print(f"✅ Created air quality sensor: {sensor.name}")
            
            # Add some observations
            now = datetime.now()
            for i in range(5):
                obs_time = now - timedelta(hours=i)
                pm25 = 45 + i * 5
                AirQualityObservation.objects.create(
                    observation_id=f"aqi-{sensor.id}-{i}",
                    location_name=sensor.name,
                    latitude=sensor.latitude,
                    longitude=sensor.longitude,
                    pm25=pm25,
                    pm10=pm25 * 1.5,
                    aqi=int(pm25 * 2),
                    no2=30 + i * 2,
                    o3=40 + i * 3,
                    co=500 + i * 10,
                    so2=10 + i,
                    observed_at=obs_time,
                    source='sample'
                )
            print("  Added 5 observations")

def create_public_services():
    services = [
        {
            'service_id': 'hospital-bachmai',
            'name': 'Bệnh viện Bạch Mai',
            'service_type': 'hospital',
            'address': 'Đống Đa, Hà Nội',
            'latitude': 21.0036,
            'longitude': 105.8478,
            'description': 'Bệnh viện đa khoa hạng đặc biệt',
            'opening_hours': '24/7',
            'contact_phone': '024-38523798',
        },
        {
            'service_id': 'park-thongnhat',
            'name': 'Công viên Thống Nhất',
            'service_type': 'park',
            'address': 'Hai Bà Trưng, Hà Nội',
            'latitude': 21.0133,
            'longitude': 105.8442,
            'description': 'Công viên lớn nhất Hà Nội',
            'opening_hours': '05:00 - 22:00',
        },
        {
            'service_id': 'school-chuvanan',
            'name': 'Trường THPT Chu Văn An',
            'service_type': 'school',
            'address': 'Ba Đình, Hà Nội',
            'latitude': 21.0358,
            'longitude': 105.8297,
            'description': 'Trường THPT công lập',
            'opening_hours': '07:00 - 17:00',
        },
    ]
    
    for data in services:
        service, created = PublicService.objects.get_or_create(
            service_id=data['service_id'],
            defaults=data
        )
        if created:
            print(f"✅ Created public service: {service.name}")

if __name__ == '__main__':
    print("🚀 Adding sample data...")
    print()
    
    create_weather_stations()
    print()
    
    create_air_quality_sensors()
    print()
    
    create_public_services()
    print()
    
    print("✅ Sample data added successfully!")
    print()
    print("Summary:")
    print(f"  Weather Stations: {WeatherStation.objects.count()}")
    print(f"  Weather Observations: {WeatherObservation.objects.count()}")
    print(f"  Air Quality Sensors: {AirQualitySensor.objects.count()}")
    print(f"  Air Quality Observations: {AirQualityObservation.objects.count()}")
    print(f"  Public Services: {PublicService.objects.count()}")
