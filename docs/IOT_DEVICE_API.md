# 📡 IoT Device API Documentation

## Gửi dữ liệu từ thiết bị của bạn

### 1. Endpoint để gửi data

```bash
POST /api/v1/auth/devices/{device_id}/add_reading/
```

### 2. Authentication

Sử dụng JWT token của user (owner của device):

```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 3. Request Body

```json
{
  "data": {
    "temperature": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "any_other_field": "value"
  },
  "recorded_at": "2025-11-28T15:30:00Z"  // optional
}
```

### 4. Ví dụ với Python

```python
import requests
import json
from datetime import datetime

# Thông tin device và token
DEVICE_ID = "3"  # ID của device (lấy từ trang chi tiết)
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGc..."  # Token từ login
API_URL = "http://localhost:8000/api/v1"

# Dữ liệu cảm biến
sensor_data = {
    "data": {
        "temperature": 28.5,
        "humidity": 65,
        "pm25": 35,
        "pm10": 50
    },
    "recorded_at": datetime.utcnow().isoformat() + "Z"
}

# Gửi dữ liệu
response = requests.post(
    f"{API_URL}/auth/devices/{DEVICE_ID}/add_reading/",
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    },
    json=sensor_data
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### 5. Ví dụ với ESP32/Arduino

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* apiUrl = "http://YOUR_SERVER:8000/api/v1/auth/devices/3/add_reading/";
const char* token = "YOUR_ACCESS_TOKEN";

void sendData(float temp, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(apiUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + String(token));
    
    // Tạo JSON
    StaticJsonDocument<200> doc;
    JsonObject data = doc.createNestedObject("data");
    data["temperature"] = temp;
    data["humidity"] = humidity;
    
    String json;
    serializeJson(doc, json);
    
    // Gửi POST request
    int httpCode = http.POST(json);
    
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);
    }
    
    http.end();
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  
  Serial.println("Connected!");
}

void loop() {
  float temp = readTemperature();  // Hàm đọc nhiệt độ
  float humidity = readHumidity();  // Hàm đọc độ ẩm
  
  sendData(temp, humidity);
  
  delay(60000);  // Gửi mỗi 1 phút
}
```

### 6. Ví dụ với curl

```bash
curl -X POST \
  http://localhost:8000/api/v1/auth/devices/3/add_reading/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 28.5,
      "humidity": 65,
      "pm25": 35
    }
  }'
```

### 7. Response

```json
{
  "id": 123,
  "device": 3,
  "device_name": "air3",
  "data": {
    "temperature": 28.5,
    "humidity": 65,
    "pm25": 35
  },
  "timestamp": "2025-11-28T15:30:00.123456Z",
  "recorded_at": null
}
```

### 8. Lấy Access Token

Sau khi đăng nhập, token được lưu trong localStorage:

```javascript
const token = localStorage.getItem('access_token');
```

Hoặc đăng nhập qua API:

```bash
curl -X POST \
  http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hoanghuanpham3",
    "password": "your_password"
  }'
```

Response:

```json
{
  "user": { ... },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 9. Định dạng dữ liệu linh hoạt

Field `data` có thể chứa bất kỳ cấu trúc JSON nào:

```json
{
  "data": {
    "temperature": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 5.2,
    "wind_direction": "NE",
    "custom_field": "any value",
    "nested": {
      "field": "value"
    }
  }
}
```

### 10. Rate Limiting

- Khuyến nghị: 1 reading / phút
- Maximum: 60 readings / phút

### 11. Error Codes

- `401`: Token không hợp lệ hoặc hết hạn
- `403`: Device không thuộc về user
- `404`: Device không tồn tại
- `400`: Dữ liệu không hợp lệ

### 12. Xem dữ liệu đã gửi

```bash
GET /api/v1/auth/devices/{device_id}/readings/?hours=24&limit=100
```

Response:

```json
[
  {
    "id": 123,
    "data": { "temperature": 28.5 },
    "timestamp": "2025-11-28T15:30:00Z"
  }
]
```
