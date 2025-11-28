# 📘 Hướng dẫn chi tiết: Kết nối thiết bị IoT với Smart City Platform

## 🎯 Tóm tắt nhanh: 5 bước để máy chủ nhận được data

### 1️⃣ Tạo thiết bị trên Web
- Đăng nhập: http://localhost:3000
- Vào **"Thiết bị của tôi"**
- Click **"Thêm thiết bị mới"**
- Điền thông tin + chọn vị trí trên bản đồ
- Click **"Thêm thiết bị"**

### 2️⃣ Lưu thông tin quan trọng
Modal sẽ hiện lên với:
- **Device ID**: `WS-123456` (tự động tạo)
- **Device API Key**: `xgY3hTk...` (64 ký tự, không expire)
- **API Endpoint**: `http://localhost:8000/api/v1/auth/devices/3/add_reading/`

⚠️ **LƯU Ý**: Copy API Key ngay! Chỉ hiển thị 1 lần khi tạo device.

### 3️⃣ Chọn phương thức gửi data
Modal có 2 tabs:
- **REST API**: Gửi trực tiếp qua HTTP POST (khuyên dùng cho ESP32/Python)
- **Orion-LD**: Gửi theo chuẩn NGSI-LD/JSON-LD (cho FIWARE ecosystem)

### 4️⃣ Copy code example và chỉnh sửa
- Chọn tab phù hợp (REST API hoặc Orion-LD)
- Chọn ngôn ngữ (Python, ESP32/Arduino, curl)
- Click **"Copy Code"**
- Paste vào project của bạn
- Thay đổi sensor reading theo thiết bị thực tế

### 5️⃣ Upload code lên thiết bị IoT
- ESP32/Arduino: Upload qua Arduino IDE/PlatformIO
- Raspberry Pi: Chạy script Python
- Test với curl: Kiểm tra connection

---

## 🐍 Example 1: Python Script (Raspberry Pi / Computer)

### Cài đặt
```bash
pip install requests
```

### Code mẫu
```python
import requests
import json
import time
from datetime import datetime

# ===== CẤU HÌNH THIẾT BỊ =====
DEVICE_ID = "WS-123456"  # Thay bằng Device ID của bạn
API_KEY = "xgY3hTkNLmQpRsVwXyZ..."  # Thay bằng Device API Key của bạn
API_ENDPOINT = "http://localhost:8000/api/v1/auth/devices/3/add_reading/"  # Thay ID

# ===== HÀM GỬI DATA =====
def send_data(sensor_data):
    """
    Gửi dữ liệu lên Smart City Platform
    
    Args:
        sensor_data: dict chứa measurements
        Ví dụ: {"temperature": 25.5, "humidity": 60}
    
    Returns:
        bool: True nếu gửi thành công
    """
    payload = {
        "data": sensor_data
    }
    
    headers = {
        "X-Device-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        print(f"✓ Data sent successfully: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending data: {e}")
        return False

# ===== ĐỌC CẢM BIẾN =====
def read_sensors():
    """
    Đọc dữ liệu từ cảm biến thực tế của bạn
    
    Ví dụ này dùng giá trị giả, bạn cần thay thế bằng:
    - DHT22: temperature, humidity
    - BMP280: pressure, altitude
    - MQ-135: air_quality, co2
    """
    # TODO: Thay thế bằng code đọc sensor thực tế
    # import Adafruit_DHT
    # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    
    return {
        "temperature": 25.5,  # °C
        "humidity": 60,       # %
        "pressure": 1013.25,  # hPa
        "timestamp": datetime.now().isoformat()
    }

# ===== MAIN LOOP =====
if __name__ == "__main__":
    print(f"🚀 Starting IoT device: {DEVICE_ID}")
    print(f"📡 Sending data to: {API_ENDPOINT}")
    print("-" * 50)
    
    while True:
        try:
            # Đọc sensor
            sensor_data = read_sensors()
            print(f"📊 Reading: {sensor_data}")
            
            # Gửi lên server
            success = send_data(sensor_data)
            
            if success:
                print("✓ Data sent successfully")
            else:
                print("✗ Failed to send data")
            
            # Đợi 60 giây trước khi gửi tiếp
            print("⏳ Waiting 60 seconds...\n")
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n⏹️  Stopping device...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(60)
```

### Chạy script
```bash
python iot_device.py
```

---

## 🤖 Example 2: ESP32 / Arduino

### Cài đặt thư viện
Trong Arduino IDE, cài:
- **WiFi** (built-in)
- **HTTPClient** (built-in)
- **ArduinoJson** (by Benoit Blanchon)

### Code mẫu
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===== WIFI CONFIGURATION =====
const char* ssid = "YOUR_WIFI_SSID";        // Thay SSID WiFi
const char* password = "YOUR_WIFI_PASSWORD"; // Thay mật khẩu WiFi

// ===== DEVICE CONFIGURATION =====
const char* deviceId = "WS-123456";  // Thay Device ID
const char* apiKey = "xgY3hTkNLmQpRsVwXyZ...";  // Thay Device API Key
const char* apiEndpoint = "http://192.168.1.100:8000/api/v1/auth/devices/3/add_reading/";

// ===== SENSOR PINS =====
#define DHT_PIN 4      // DHT22 data pin
#define LED_PIN 2      // Built-in LED

// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  // Connect to WiFi
  Serial.println("\n🚀 Starting IoT Device");
  Serial.print("📶 Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));  // Blink LED
  }
  
  Serial.println("\n✓ WiFi connected!");
  Serial.print("📡 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("🔗 API Endpoint: ");
  Serial.println(apiEndpoint);
  Serial.println("-" * 50);
  
  digitalWrite(LED_PIN, HIGH);  // LED on when connected
}

// ===== ĐỌC CẢM BIẾN =====
void readSensors(float &temperature, float &humidity) {
  // TODO: Thay bằng code đọc sensor thực tế
  // #include <DHT.h>
  // DHT dht(DHT_PIN, DHT22);
  // temperature = dht.readTemperature();
  // humidity = dht.readHumidity();
  
  // Giá trị giả để demo
  temperature = 25.5 + random(-50, 50) / 10.0;
  humidity = 60.0 + random(-100, 100) / 10.0;
}

// ===== GỬI DATA LÊN SERVER =====
bool sendData(float temperature, float humidity) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi disconnected!");
    return false;
  }
  
  HTTPClient http;
  
  // Start connection
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-API-Key", apiKey);
  
  // Create JSON payload
  StaticJsonDocument<200> doc;
  JsonObject data = doc.createNestedObject("data");
  data["temperature"] = temperature;
  data["humidity"] = humidity;
  data["timestamp"] = millis();
  data["wifi_signal"] = WiFi.RSSI();  // Bonus: WiFi strength
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.print("📤 Sending: ");
  Serial.println(payload);
  
  // Send POST request
  int httpCode = http.POST(payload);
  
  // Check response
  bool success = false;
  if (httpCode > 0) {
    Serial.print("✓ Response code: ");
    Serial.println(httpCode);
    
    if (httpCode == 201) {
      String response = http.getString();
      Serial.print("✓ Data sent: ");
      Serial.println(response);
      success = true;
      
      // Blink LED 3 times on success
      for (int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, LOW);
        delay(100);
        digitalWrite(LED_PIN, HIGH);
        delay(100);
      }
    }
  } else {
    Serial.print("✗ Error code: ");
    Serial.println(httpCode);
    Serial.println(http.errorToString(httpCode));
  }
  
  http.end();
  return success;
}

// ===== MAIN LOOP =====
void loop() {
  float temperature, humidity;
  
  // Read sensors
  Serial.println("\n📊 Reading sensors...");
  readSensors(temperature, humidity);
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  
  // Send data
  bool success = sendData(temperature, humidity);
  
  if (!success) {
    Serial.println("✗ Failed to send data, will retry...");
  }
  
  // Wait 60 seconds
  Serial.println("⏳ Waiting 60 seconds...\n");
  delay(60000);  // 60 seconds
}
```

### Upload code
1. Chọn board: **ESP32 Dev Module**
2. Chọn port: `/dev/ttyUSB0` (Linux) hoặc `COM3` (Windows)
3. Click **Upload**
4. Mở **Serial Monitor** (115200 baud) để xem logs

---

## 🔧 Example 3: Test với curl

### Test nhanh
```bash
curl -X POST "http://localhost:8000/api/v1/auth/devices/3/add_reading/" \
  -H "X-Device-API-Key: xgY3hTkNLmQpRsVwXyZ..." \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 25.5,
      "humidity": 60,
      "pressure": 1013.25
    }
  }'
```

### Test với script
```bash
#!/bin/bash
DEVICE_ID="WS-123456"
API_KEY="xgY3hTkNLmQpRsVwXyZ..."
ENDPOINT="http://localhost:8000/api/v1/auth/devices/3/add_reading/"

while true; do
  # Generate random data
  TEMP=$(echo "scale=1; 20 + $RANDOM % 10" | bc)
  HUM=$(echo "scale=1; 50 + $RANDOM % 30" | bc)
  
  echo "📤 Sending: temp=$TEMP, hum=$HUM"
  
  curl -X POST "$ENDPOINT" \
    -H "X-Device-API-Key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"data\": {\"temperature\": $TEMP, \"humidity\": $HUM}}" \
    -s | jq .
  
  echo "⏳ Waiting 60s..."
  sleep 60
done
```

Chạy:
```bash
chmod +x test_device.sh
./test_device.sh
```

---

## 🔷 Example 4: Orion-LD (NGSI-LD)

### Python với NGSI-LD
```python
import requests
import json
from datetime import datetime

ORION_LD_URL = "http://localhost:1026"
DEVICE_ID = "urn:ngsi-ld:Device:WS-123456"

def send_to_orion(sensor_data):
    """Gửi dữ liệu theo chuẩn NGSI-LD"""
    entity = {
        "id": DEVICE_ID,
        "type": "Device",
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ],
        "temperature": {
            "type": "Property",
            "value": sensor_data.get("temperature"),
            "unitCode": "CEL"
        },
        "humidity": {
            "type": "Property",
            "value": sensor_data.get("humidity"),
            "unitCode": "P1"
        },
        "dateObserved": {
            "type": "Property",
            "value": {
                "@type": "DateTime",
                "@value": datetime.now().isoformat()
            }
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [105.8342, 21.0278]  # Hanoi
            }
        }
    }
    
    headers = {
        "Content-Type": "application/ld+json"
    }
    
    try:
        # Create or update entity
        response = requests.post(
            f"{ORION_LD_URL}/ngsi-ld/v1/entities",
            json=entity,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 409:
            # Entity exists, update it
            response = requests.patch(
                f"{ORION_LD_URL}/ngsi-ld/v1/entities/{DEVICE_ID}/attrs",
                json={k: v for k, v in entity.items() if k not in ['id', 'type', '@context']},
                headers=headers,
                timeout=10
            )
        
        print(f"✓ Data sent to Orion-LD: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Usage
sensor_data = {"temperature": 25.5, "humidity": 60}
send_to_orion(sensor_data)
```

---

## 🔑 Quản lý API Keys

### Xem API Key của device
```bash
curl -X GET "http://localhost:8000/api/v1/auth/devices/3/api_key/" \
  -H "Authorization: Bearer YOUR_USER_JWT_TOKEN"
```

Response:
```json
{
  "device_id": "WS-123456",
  "api_key": "xgY3hTkNLmQpRsVwXyZ...",
  "created_at": "2025-11-28T10:30:00Z",
  "last_used": "2025-11-28T12:45:30Z",
  "is_active": true,
  "message": "Keep this API key secret!"
}
```

### Regenerate API Key (nếu bị lộ)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/devices/3/regenerate_api_key/" \
  -H "Authorization: Bearer YOUR_USER_JWT_TOKEN"
```

⚠️ **Cảnh báo**: Key cũ sẽ không hoạt động nữa. Phải cập nhật code trên thiết bị IoT với key mới.

---

## 📊 Xem dữ liệu đã gửi

### Trên Web
1. Vào **http://localhost:3000/my-devices**
2. Click thiết bị
3. Xem **"Dữ liệu gần đây"**

### Qua API
```bash
curl "http://localhost:8000/api/v1/auth/devices/3/readings/?hours=24&limit=100" \
  -H "Authorization: Bearer YOUR_USER_JWT_TOKEN"
```

---

## ❓ Troubleshooting

### Lỗi 401 Unauthorized
```
{"detail": "Invalid or inactive API key"}
```
**Giải pháp**:
- Kiểm tra API Key có đúng không
- Kiểm tra header: `X-Device-API-Key` (chú ý chữ hoa/thường)
- Kiểm tra device có bị disable không

### Lỗi 403 Forbidden
```
{"detail": "You don't have permission..."}
```
**Giải pháp**:
- Bạn đang dùng device ID/API key của người khác
- Mỗi device chỉ nhận data từ API key của chính nó

### Lỗi 404 Not Found
```
{"detail": "Not found."}
```
**Giải pháp**:
- Kiểm tra device ID trong URL
- Device có thể đã bị xóa

### ESP32 không kết nối WiFi
**Giải pháp**:
- Kiểm tra SSID và password
- Thử restart ESP32
- Kiểm tra WiFi 2.4GHz (ESP32 không hỗ trợ 5GHz)

### Data không hiện trên map
**Giải pháp**:
- Kiểm tra device có `is_public=True` không
- Check status device (phải là `active`)
- Hard refresh browser: `Ctrl+Shift+R`

---

## 📖 Tài liệu tham khảo

- **API Documentation**: http://localhost:8000/api/v1/docs/
- **Swagger UI**: http://localhost:8000/swagger/
- **NGSI-LD Spec**: https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.07.01_60/gs_CIM009v010701p.pdf
- **Smart Data Models**: https://smartdatamodels.org/

---

## 💡 Tips & Best Practices

1. **Gửi data định kỳ**: 60-300 giây/lần (không quá thường xuyên)
2. **Xử lý lỗi**: Retry khi gửi thất bại, log errors
3. **Bảo mật**: Không commit API key vào git, dùng environment variables
4. **Battery**: Nếu dùng pin, tăng interval để tiết kiệm năng lượng
5. **Timestamp**: Luôn gửi timestamp trong data để track chính xác
6. **WiFi signal**: Gửi kèm `wifi_signal` để monitor connection quality
7. **Error handling**: Implement exponential backoff cho retries

---

## 🎓 Ví dụ thực tế

### Weather Station hoàn chỉnh
Xem: `examples/weather_station_esp32/`
- DHT22: Temperature + Humidity
- BMP280: Pressure + Altitude  
- Rain sensor
- UV sensor
- Deep sleep mode

### Air Quality Monitor
Xem: `examples/air_quality_rpi/`
- MQ-135: Air quality index
- MQ-7: CO levels
- PM2.5 sensor
- OLED display

### Traffic Counter
Xem: `examples/traffic_counter_arduino/`
- Ultrasonic sensor
- Vehicle counting
- Speed estimation
- Data aggregation

---

**Made with ❤️ for Smart City Platform**
