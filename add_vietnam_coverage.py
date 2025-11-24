#!/usr/bin/env python
"""Add comprehensive Vietnam coverage data"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity.settings')
django.setup()

from entities.models import WeatherStation, AirQualitySensor, PublicService
from observations.models import WeatherObservation, AirQualityObservation

# Major cities and locations across Vietnam
VIETNAM_LOCATIONS = [
    # North Region
    {'name': 'Hà Nội - Hoàn Kiếm', 'lat': 21.0285, 'lon': 105.8542, 'region': 'Miền Bắc'},
    {'name': 'Hà Nội - Cầu Giấy', 'lat': 21.0333, 'lon': 105.7944, 'region': 'Miền Bắc'},
    {'name': 'Hà Nội - Đống Đa', 'lat': 21.0170, 'lon': 105.8270, 'region': 'Miền Bắc'},
    {'name': 'Hà Nội - Tây Hồ', 'lat': 21.0583, 'lon': 105.8189, 'region': 'Miền Bắc'},
    {'name': 'Hải Phòng - Hồng Bàng', 'lat': 20.8650, 'lon': 106.6830, 'region': 'Miền Bắc'},
    {'name': 'Hải Phòng - Lê Chân', 'lat': 20.8439, 'lon': 106.6880, 'region': 'Miền Bắc'},
    {'name': 'Hạ Long - Quảng Ninh', 'lat': 20.9500, 'lon': 107.0833, 'region': 'Miền Bắc'},
    {'name': 'Thái Nguyên', 'lat': 21.5670, 'lon': 105.8252, 'region': 'Miền Bắc'},
    {'name': 'Sapa - Lào Cai', 'lat': 22.3363, 'lon': 103.8438, 'region': 'Miền Bắc'},
    {'name': 'Bắc Ninh', 'lat': 21.1861, 'lon': 106.0763, 'region': 'Miền Bắc'},
    {'name': 'Ninh Bình', 'lat': 20.2506, 'lon': 105.9745, 'region': 'Miền Bắc'},
    
    # Central Region
    {'name': 'Vinh - Nghệ An', 'lat': 18.6792, 'lon': 105.6811, 'region': 'Miền Trung'},
    {'name': 'Đông Hà - Quảng Trị', 'lat': 16.8197, 'lon': 107.1003, 'region': 'Miền Trung'},
    {'name': 'Huế - TT-Huế', 'lat': 16.4637, 'lon': 107.5909, 'region': 'Miền Trung'},
    {'name': 'Đà Nẵng - Hải Châu', 'lat': 16.0544, 'lon': 108.2022, 'region': 'Miền Trung'},
    {'name': 'Đà Nẵng - Sơn Trà', 'lat': 16.0828, 'lon': 108.2386, 'region': 'Miền Trung'},
    {'name': 'Hội An - Quảng Nam', 'lat': 15.8801, 'lon': 108.3380, 'region': 'Miền Trung'},
    {'name': 'Tam Kỳ - Quảng Nam', 'lat': 15.5735, 'lon': 108.4746, 'region': 'Miền Trung'},
    {'name': 'Quảng Ngãi', 'lat': 15.1214, 'lon': 108.8044, 'region': 'Miền Trung'},
    {'name': 'Quy Nhơn - Bình Định', 'lat': 13.7830, 'lon': 109.2196, 'region': 'Miền Trung'},
    {'name': 'Tuy Hòa - Phú Yên', 'lat': 13.0955, 'lon': 109.2961, 'region': 'Miền Trung'},
    {'name': 'Nha Trang - Khánh Hòa', 'lat': 12.2388, 'lon': 109.1967, 'region': 'Miền Trung'},
    {'name': 'Phan Rang - Ninh Thuận', 'lat': 11.5676, 'lon': 108.9872, 'region': 'Miền Trung'},
    {'name': 'Đà Lạt - Lâm Đồng', 'lat': 11.9404, 'lon': 108.4583, 'region': 'Tây Nguyên'},
    {'name': 'Buôn Ma Thuột - Đắk Lắk', 'lat': 12.6667, 'lon': 108.0500, 'region': 'Tây Nguyên'},
    {'name': 'Pleiku - Gia Lai', 'lat': 13.9833, 'lon': 108.0000, 'region': 'Tây Nguyên'},
    {'name': 'Kon Tum', 'lat': 14.3497, 'lon': 108.0005, 'region': 'Tây Nguyên'},
    
    # South Region
    {'name': 'Phan Thiết - Bình Thuận', 'lat': 10.9280, 'lon': 108.1020, 'region': 'Miền Nam'},
    {'name': 'Vũng Tàu - BR-VT', 'lat': 10.3460, 'lon': 107.0843, 'region': 'Miền Nam'},
    {'name': 'TP.HCM - Quận 1', 'lat': 10.7769, 'lon': 106.7009, 'region': 'Miền Nam'},
    {'name': 'TP.HCM - Quận 3', 'lat': 10.7860, 'lon': 106.6890, 'region': 'Miền Nam'},
    {'name': 'TP.HCM - Bình Thạnh', 'lat': 10.8109, 'lon': 106.7100, 'region': 'Miền Nam'},
    {'name': 'TP.HCM - Thủ Đức', 'lat': 10.8503, 'lon': 106.7717, 'region': 'Miền Nam'},
    {'name': 'TP.HCM - Tân Bình', 'lat': 10.7996, 'lon': 106.6529, 'region': 'Miền Nam'},
    {'name': 'Biên Hòa - Đồng Nai', 'lat': 10.9510, 'lon': 106.8234, 'region': 'Miền Nam'},
    {'name': 'Thủ Dầu Một - Bình Dương', 'lat': 10.9804, 'lon': 106.6519, 'region': 'Miền Nam'},
    {'name': 'Tây Ninh', 'lat': 11.3351, 'lon': 106.0980, 'region': 'Miền Nam'},
    {'name': 'Long Xuyên - An Giang', 'lat': 10.3861, 'lon': 105.4348, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Cần Thơ - Ninh Kiều', 'lat': 10.0340, 'lon': 105.7220, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Cần Thơ - Cái Răng', 'lat': 10.0124, 'lon': 105.7800, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Sóc Trăng', 'lat': 9.6037, 'lon': 105.9742, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Cà Mau', 'lat': 9.1769, 'lon': 105.1524, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Rạch Giá - Kiên Giang', 'lat': 10.0154, 'lon': 105.0807, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Phú Quốc - Kiên Giang', 'lat': 10.2226, 'lon': 103.9675, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Mỹ Tho - Tiền Giang', 'lat': 10.3599, 'lon': 106.3600, 'region': 'Đồng bằng sông Cửu Long'},
    {'name': 'Vĩnh Long', 'lat': 10.2533, 'lon': 105.9722, 'region': 'Đồng bằng sông Cửu Long'},
]

def create_weather_stations():
    print("🌤️  Creating weather stations across Vietnam...")
    count = 0
    for i, location in enumerate(VIETNAM_LOCATIONS):
        station_id = f"weather-vn-{i+1:03d}"
        station, created = WeatherStation.objects.get_or_create(
            station_id=station_id,
            defaults={
                'name': f"Trạm Thời tiết {location['name']}",
                'address': f"{location['name']}, Việt Nam",
                'latitude': location['lat'],
                'longitude': location['lon'],
            }
        )
        if created:
            count += 1
            # Add 3 recent observations
            now = datetime.now()
            for j in range(3):
                obs_time = now - timedelta(hours=j)
                temp_base = 28 if 'Miền Nam' in location['region'] else 25
                WeatherObservation.objects.create(
                    observation_id=f"{station_id}-obs-{j}",
                    location_name=station.name,
                    latitude=station.latitude,
                    longitude=station.longitude,
                    temperature=temp_base + random.uniform(-5, 8),
                    humidity=65 + random.randint(-15, 20),
                    pressure=1013 + random.randint(-5, 5),
                    wind_speed=random.uniform(2, 15),
                    wind_direction=random.randint(0, 359),
                    observed_at=obs_time,
                    source='sample'
                )
    print(f"   ✅ Created {count} new weather stations")

def create_air_quality_sensors():
    print("💨 Creating air quality sensors...")
    count = 0
    # Add AQI sensors to major cities only (more realistic)
    major_cities = [loc for loc in VIETNAM_LOCATIONS 
                    if any(city in loc['name'] for city in ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 
                                                              'TP.HCM', 'Cần Thơ', 'Nha Trang',
                                                              'Huế', 'Hạ Long'])]
    
    for i, location in enumerate(major_cities):
        sensor_id = f"aqi-vn-{i+1:03d}"
        sensor, created = AirQualitySensor.objects.get_or_create(
            sensor_id=sensor_id,
            defaults={
                'name': f"Cảm biến CK {location['name']}",
                'address': f"{location['name']}, Việt Nam",
                'latitude': location['lat'],
                'longitude': location['lon'],
            }
        )
        if created:
            count += 1
            # Add 3 recent observations
            now = datetime.now()
            for j in range(3):
                obs_time = now - timedelta(hours=j)
                pm25 = random.uniform(20, 80)  # Realistic AQI range for Vietnam
                AirQualityObservation.objects.create(
                    observation_id=f"{sensor_id}-obs-{j}",
                    location_name=sensor.name,
                    latitude=sensor.latitude,
                    longitude=sensor.longitude,
                    pm25=pm25,
                    pm10=pm25 * random.uniform(1.3, 1.7),
                    aqi=int(pm25 * random.uniform(1.8, 2.2)),
                    no2=random.uniform(15, 50),
                    o3=random.uniform(30, 80),
                    co=random.uniform(400, 800),
                    so2=random.uniform(5, 25),
                    observed_at=obs_time,
                    source='sample'
                )
    print(f"   ✅ Created {count} new air quality sensors")

def create_public_services():
    print("🏥 Creating public services...")
    services_data = [
        # Major hospitals
        {'name': 'Bệnh viện Bạch Mai', 'type': 'hospital', 'city': 'Hà Nội', 'lat': 21.0036, 'lon': 105.8478},
        {'name': 'Bệnh viện Việt Đức', 'type': 'hospital', 'city': 'Hà Nội', 'lat': 21.0243, 'lon': 105.8460},
        {'name': 'Bệnh viện Chợ Rẫy', 'type': 'hospital', 'city': 'TP.HCM', 'lat': 10.7556, 'lon': 106.6563},
        {'name': 'Bệnh viện Trung ương Huế', 'type': 'hospital', 'city': 'Huế', 'lat': 16.4510, 'lon': 107.5980},
        {'name': 'Bệnh viện C Đà Nẵng', 'type': 'hospital', 'city': 'Đà Nẵng', 'lat': 16.0678, 'lon': 108.2208},
        {'name': 'Bệnh viện Việt Tiệp Hải Phòng', 'type': 'hospital', 'city': 'Hải Phòng', 'lat': 20.8536, 'lon': 106.6838},
        {'name': 'Bệnh viện Đa khoa Cần Thơ', 'type': 'hospital', 'city': 'Cần Thơ', 'lat': 10.0326, 'lon': 105.7690},
        
        # Major parks
        {'name': 'Công viên Thống Nhất', 'type': 'park', 'city': 'Hà Nội', 'lat': 21.0133, 'lon': 105.8442},
        {'name': 'Công viên Lê Văn Tám', 'type': 'park', 'city': 'TP.HCM', 'lat': 10.7694, 'lon': 106.6961},
        {'name': 'Công viên 29/3', 'type': 'park', 'city': 'Đà Nẵng', 'lat': 16.0560, 'lon': 108.2235},
        {'name': 'Vườn hoa Lạc Hồng Tây', 'type': 'park', 'city': 'Hải Phòng', 'lat': 20.8613, 'lon': 106.6803},
        
        # Universities
        {'name': 'ĐH Quốc gia Hà Nội', 'type': 'school', 'city': 'Hà Nội', 'lat': 21.0377, 'lon': 105.7829},
        {'name': 'ĐH Bách khoa Hà Nội', 'type': 'school', 'city': 'Hà Nội', 'lat': 21.0054, 'lon': 105.8433},
        {'name': 'ĐH Quốc gia TP.HCM', 'type': 'school', 'city': 'TP.HCM', 'lat': 10.7625, 'lon': 106.6821},
        {'name': 'ĐH Đà Nẵng', 'type': 'school', 'city': 'Đà Nẵng', 'lat': 16.0736, 'lon': 108.1509},
    ]
    
    count = 0
    for i, data in enumerate(services_data):
        service_id = f"service-vn-{i+1:03d}"
        service, created = PublicService.objects.get_or_create(
            service_id=service_id,
            defaults={
                'name': data['name'],
                'service_type': data['type'],
                'address': f"{data['city']}, Việt Nam",
                'latitude': data['lat'],
                'longitude': data['lon'],
                'description': f"{data['name']} tại {data['city']}",
                'opening_hours': '24/7' if data['type'] == 'hospital' else '06:00 - 22:00',
            }
        )
        if created:
            count += 1
    print(f"   ✅ Created {count} new public services")

if __name__ == '__main__':
    print("=" * 60)
    print("🇻🇳  ADDING VIETNAM-WIDE COVERAGE DATA")
    print("=" * 60)
    print()
    
    create_weather_stations()
    print()
    
    create_air_quality_sensors()
    print()
    
    create_public_services()
    print()
    
    print("=" * 60)
    print("✅ VIETNAM COVERAGE COMPLETED!")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print(f"   Weather Stations: {WeatherStation.objects.count()}")
    print(f"   Weather Observations: {WeatherObservation.objects.count()}")
    print(f"   Air Quality Sensors: {AirQualitySensor.objects.count()}")
    print(f"   Air Quality Observations: {AirQualityObservation.objects.count()}")
    print(f"   Public Services: {PublicService.objects.count()}")
    print()
    print("🗺️  Coverage:")
    print("   - Miền Bắc: 11 locations")
    print("   - Miền Trung & Tây Nguyên: 16 locations")
    print("   - Miền Nam & Đồng bằng sông Cửu Long: 17 locations")
    print("   📍 Total: 44 locations across Vietnam")
    print()
