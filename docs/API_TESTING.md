# API Testing Guide

## Sử dụng cURL để test API

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### 2. Tạo Weather Station

```bash
curl -X POST http://localhost:8000/api/v1/weather-stations/ \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "hanoi-station-test",
    "name": "Trạm Thời tiết Test Hà Nội",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hà Nội, Việt Nam",
    "is_active": true
  }'
```

### 3. Lấy danh sách Weather Stations

```bash
curl http://localhost:8000/api/v1/weather-stations/
```

### 4. Tìm Weather Stations gần đây

```bash
curl "http://localhost:8000/api/v1/weather-stations/nearby/?lat=21.0285&lon=105.8542&radius=10"
```

### 5. Lấy dữ liệu thời tiết từ OpenWeatherMap

```bash
# Lấy theo tọa độ
curl "http://localhost:8000/api/v1/fetch/weather?lat=21.0285&lon=105.8542"

# Lấy theo tên thành phố
curl "http://localhost:8000/api/v1/fetch/weather?city=Hanoi"
```

### 6. Lưu dữ liệu thời tiết vào database

```bash
curl -X POST http://localhost:8000/api/v1/fetch/weather \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 21.0285,
    "lon": 105.8542,
    "location_name": "Hà Nội"
  }'
```

### 7. Lấy dữ liệu chất lượng không khí

```bash
curl "http://localhost:8000/api/v1/fetch/air-quality?lat=21.0285&lon=105.8542"
```

### 8. Lấy observation thời tiết gần nhất

```bash
curl "http://localhost:8000/api/v1/weather/latest/?lat=21.0285&lon=105.8542"
```

### 9. Lấy observation chất lượng không khí trong 24h

```bash
curl "http://localhost:8000/api/v1/air-quality/?hours=24"
```

### 10. Đồng bộ tất cả dữ liệu thời tiết

```bash
curl -X POST http://localhost:8000/api/v1/sync/weather
```

### 11. Đồng bộ tất cả dữ liệu chất lượng không khí

```bash
curl -X POST http://localhost:8000/api/v1/sync/air-quality
```

### 12. Query entities từ Orion-LD

```bash
curl "http://localhost:8000/api/v1/entities/query_orion/?type=WeatherStation"
```

### 13. Sync entity đến Orion-LD

```bash
# Lấy ID của entity trước
ENTITY_ID=$(curl http://localhost:8000/api/v1/entities/ | jq -r '.results[0].id')

# Sync entity
curl -X POST "http://localhost:8000/api/v1/entities/$ENTITY_ID/sync_to_orion/"
```

### 14. Tạo Air Quality Sensor

```bash
curl -X POST http://localhost:8000/api/v1/air-quality-sensors/ \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "hanoi-aq-test",
    "name": "Cảm biến AQ Test Hà Nội",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hà Nội, Việt Nam",
    "is_active": true
  }'
```

### 15. Tạo Public Service

```bash
curl -X POST http://localhost:8000/api/v1/public-services/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "hanoi-park-test",
    "name": "Công viên Test",
    "service_type": "park",
    "description": "Công viên thử nghiệm",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hà Nội, Việt Nam",
    "opening_hours": "05:00-22:00",
    "is_active": true
  }'
```

### 16. Tìm Public Services gần đây theo loại

```bash
curl "http://localhost:8000/api/v1/public-services/nearby/?lat=21.0285&lon=105.8542&radius=5&type=park"
```

## Sử dụng Python để test API

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Tạo weather station
data = {
    "station_id": "python-test-station",
    "name": "Python Test Station",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hanoi, Vietnam"
}
response = requests.post(f"{BASE_URL}/weather-stations/", json=data)
print(response.json())

# 3. Lấy dữ liệu thời tiết
params = {"lat": 21.0285, "lon": 105.8542}
response = requests.get(f"{BASE_URL}/fetch/weather", params=params)
print(response.json())

# 4. Query từ Orion-LD
params = {"type": "WeatherStation"}
response = requests.get(f"{BASE_URL}/entities/query_orion/", params=params)
print(response.json())
```

## Direct Orion-LD API Testing

### Query entities từ Orion-LD trực tiếp

```bash
curl http://localhost:1026/ngsi-ld/v1/entities \
  -H "Accept: application/ld+json"
```

### Tạo entity trực tiếp vào Orion-LD

```bash
curl -X POST http://localhost:1026/ngsi-ld/v1/entities \
  -H "Content-Type: application/ld+json" \
  -d '{
    "id": "urn:ngsi-ld:WeatherStation:test-direct",
    "type": "WeatherStation",
    "@context": [
      "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ],
    "name": {
      "type": "Property",
      "value": "Direct Test Station"
    },
    "location": {
      "type": "GeoProperty",
      "value": {
        "type": "Point",
        "coordinates": [105.8542, 21.0285]
      }
    }
  }'
```

### Lấy entity từ Orion-LD

```bash
curl http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:WeatherStation:test-direct \
  -H "Accept: application/ld+json"
```
