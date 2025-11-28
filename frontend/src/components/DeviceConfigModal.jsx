import { useState } from 'react';

const API_URL = 'http://localhost:8000/api/v1';
const ORION_LD_URL = 'http://localhost:1026';

export default function DeviceConfigModal({ device, onClose }) {
  const [copied, setCopied] = useState('');
  const [activeTab, setActiveTab] = useState('rest'); // 'rest' or 'orion'
  const token = localStorage.getItem('access_token');

  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(''), 2000);
  };

  const pythonExample = `import requests
import json
from datetime import datetime

# Cấu hình thiết bị
DEVICE_ID = "${device.device_id}"
API_TOKEN = "${token}"
API_ENDPOINT = "${API_URL}/auth/devices/${device.id}/add_reading/"

def send_data(sensor_data):
    """
    Gửi dữ liệu từ thiết bị IoT lên server
    
    Args:
        sensor_data: dict chứa dữ liệu cảm biến
        Ví dụ: {"temperature": 25.5, "humidity": 60}
    """
    payload = {
        "data": sensor_data
    }
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
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
    except Exception as e:
        print(f"✗ Error sending data: {e}")
        return False

# Ví dụ sử dụng
if __name__ == "__main__":
    # Đọc dữ liệu từ cảm biến của bạn
    sensor_data = {
        "temperature": 25.5,
        "humidity": 60,
        "pressure": 1013.25,
        "timestamp": datetime.now().isoformat()
    }
    
    send_data(sensor_data)
`;

  const esp32Example = `#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Device configuration
const char* deviceId = "${device.device_id}";
const char* apiToken = "${token}";
const char* apiEndpoint = "${API_URL}/auth/devices/${device.id}/add_reading/";

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\\nConnected!");
}

void sendData(float temperature, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(apiEndpoint);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + apiToken);
    
    // Create JSON payload
    StaticJsonDocument<200> doc;
    JsonObject data = doc.createNestedObject("data");
    data["temperature"] = temperature;
    data["humidity"] = humidity;
    data["timestamp"] = millis();
    
    String payload;
    serializeJson(doc, payload);
    
    // Send POST request
    int httpCode = http.POST(payload);
    
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("✓ Data sent: " + response);
    } else {
      Serial.println("✗ Error: " + String(httpCode));
    }
    
    http.end();
  }
}

void loop() {
  // Read sensor data (replace with your sensor code)
  float temp = 25.5;  // Example: DHT.temperature
  float hum = 60.0;   // Example: DHT.humidity
  
  sendData(temp, hum);
  
  delay(60000);  // Send data every 60 seconds
}
`;

  const curlExample = `# Test gửi dữ liệu bằng curl
curl -X POST "${API_URL}/auth/devices/${device.id}/add_reading/" \\
  -H "Authorization: Bearer ${token}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "data": {
      "temperature": 25.5,
      "humidity": 60,
      "pressure": 1013.25
    }
  }'`;

  const orionPythonExample = `import requests
import json
from datetime import datetime

# Orion-LD Configuration
ORION_LD_URL = "${ORION_LD_URL}"
DEVICE_ID = "urn:ngsi-ld:Device:${device.device_id}"

def send_to_orion(sensor_data):
    """
    Gửi dữ liệu theo chuẩn NGSI-LD lên Orion Context Broker
    
    Args:
        sensor_data: dict chứa dữ liệu cảm biến
    """
    # NGSI-LD Entity (JSON-LD format)
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
                "coordinates": [${device.longitude}, ${device.latitude}]
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

# Ví dụ sử dụng
if __name__ == "__main__":
    sensor_data = {
        "temperature": 25.5,
        "humidity": 60
    }
    send_to_orion(sensor_data)
`;

  const orionCurlExample = `# Tạo Entity NGSI-LD
curl -X POST "${ORION_LD_URL}/ngsi-ld/v1/entities" \\
  -H "Content-Type: application/ld+json" \\
  -d '{
    "id": "urn:ngsi-ld:Device:${device.device_id}",
    "type": "Device",
    "@context": [
      "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ],
    "temperature": {
      "type": "Property",
      "value": 25.5,
      "unitCode": "CEL"
    },
    "humidity": {
      "type": "Property",
      "value": 60,
      "unitCode": "P1"
    },
    "location": {
      "type": "GeoProperty",
      "value": {
        "type": "Point",
        "coordinates": [${device.longitude}, ${device.latitude}]
      }
    }
  }'

# Update existing entity
curl -X PATCH "${ORION_LD_URL}/ngsi-ld/v1/entities/urn:ngsi-ld:Device:${device.device_id}/attrs" \\
  -H "Content-Type: application/ld+json" \\
  -d '{
    "temperature": {
      "type": "Property",
      "value": 26.3,
      "unitCode": "CEL"
    }
  }'`;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h3 className="text-xl font-bold text-gray-900">
            🎉 Thiết bị đã được tạo thành công!
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Quick Summary */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-300 rounded-lg p-5">
            <h4 className="font-bold text-purple-900 mb-3 text-lg">📝 Tóm tắt: User cần làm gì?</h4>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3">
                <span className="text-2xl">1️⃣</span>
                <div>
                  <strong className="text-purple-900">Lưu thông tin thiết bị</strong>
                  <p className="text-purple-700">Device ID: <code className="bg-white px-2 py-0.5 rounded">{device.device_id}</code> và API Token</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">2️⃣</span>
                <div>
                  <strong className="text-purple-900">Chọn phương thức gửi data</strong>
                  <p className="text-purple-700">REST API (Python/ESP32) hoặc Orion-LD (NGSI-LD)</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">3️⃣</span>
                <div>
                  <strong className="text-purple-900">Copy code example phù hợp</strong>
                  <p className="text-purple-700">Chọn tab bên dưới, copy code và chỉnh sửa cho thiết bị của bạn</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">4️⃣</span>
                <div>
                  <strong className="text-purple-900">Deploy vào thiết bị IoT</strong>
                  <p className="text-purple-700">Upload code lên ESP32/Raspberry Pi/Arduino của bạn</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">5️⃣</span>
                <div>
                  <strong className="text-purple-900">Dữ liệu tự động đồng bộ</strong>
                  <p className="text-purple-700">Xem real-time trên bản đồ và dashboard</p>
                </div>
              </div>
            </div>
          </div>

          {/* Device Info */}
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
            <h4 className="font-semibold text-indigo-900 mb-2">📋 Thông tin thiết bị</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Tên thiết bị:</span>
                <span className="font-semibold">{device.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Device ID:</span>
                <div className="flex items-center gap-2">
                  <code className="bg-white px-2 py-1 rounded font-mono text-indigo-700">
                    {device.device_id}
                  </code>
                  <button
                    onClick={() => copyToClipboard(device.device_id, 'device_id')}
                    className="text-indigo-600 hover:text-indigo-800"
                  >
                    {copied === 'device_id' ? '✓' : '📋'}
                  </button>
                </div>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Loại:</span>
                <span className="font-semibold">{device.device_type}</span>
              </div>
            </div>
          </div>

          {/* API Token */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-semibold text-yellow-900 mb-2">🔑 API Token</h4>
            <p className="text-sm text-yellow-700 mb-2">
              Sử dụng token này để xác thực khi gửi dữ liệu:
            </p>
            <div className="flex items-center gap-2">
              <code className="flex-1 bg-white px-3 py-2 rounded font-mono text-xs break-all">
                {token}
              </code>
              <button
                onClick={() => copyToClipboard(token, 'token')}
                className="px-3 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
              >
                {copied === 'token' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>

          {/* API Endpoint */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-900 mb-2">🌐 API Endpoint</h4>
            <p className="text-sm text-green-700 mb-2">
              Gửi dữ liệu đến địa chỉ này:
            </p>
            <div className="flex items-center gap-2">
              <code className="flex-1 bg-white px-3 py-2 rounded font-mono text-xs break-all">
                {API_URL}/auth/devices/{device.id}/add_reading/
              </code>
              <button
                onClick={() => copyToClipboard(`${API_URL}/auth/devices/${device.id}/add_reading/`, 'endpoint')}
                className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                {copied === 'endpoint' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>

          {/* Code Examples */}
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-2">
              <h4 className="font-semibold text-gray-900">💻 Code Examples</h4>
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveTab('rest')}
                  className={`px-4 py-1 rounded-lg text-sm font-medium transition ${
                    activeTab === 'rest'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  REST API
                </button>
                <button
                  onClick={() => setActiveTab('orion')}
                  className={`px-4 py-1 rounded-lg text-sm font-medium transition ${
                    activeTab === 'orion'
                      ? 'bg-orange-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Orion-LD (NGSI-LD)
                </button>
              </div>
            </div>

            {activeTab === 'rest' ? (
              <>
                {/* REST API Examples */}
                {/* Python */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <div className="bg-gray-100 px-4 py-2 flex justify-between items-center">
                    <span className="font-semibold text-gray-700">🐍 Python</span>
                    <button
                      onClick={() => copyToClipboard(pythonExample, 'python')}
                      className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                    >
                      {copied === 'python' ? '✓ Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre className="p-4 bg-gray-50 overflow-x-auto text-xs">
                    <code>{pythonExample}</code>
                  </pre>
                </div>

                {/* ESP32/Arduino */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <div className="bg-gray-100 px-4 py-2 flex justify-between items-center">
                    <span className="font-semibold text-gray-700">🤖 ESP32/Arduino</span>
                    <button
                      onClick={() => copyToClipboard(esp32Example, 'esp32')}
                      className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                    >
                      {copied === 'esp32' ? '✓ Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre className="p-4 bg-gray-50 overflow-x-auto text-xs">
                    <code>{esp32Example}</code>
                  </pre>
                </div>

                {/* curl */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <div className="bg-gray-100 px-4 py-2 flex justify-between items-center">
                    <span className="font-semibold text-gray-700">🔧 curl (Test)</span>
                    <button
                      onClick={() => copyToClipboard(curlExample, 'curl')}
                      className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                    >
                      {copied === 'curl' ? '✓ Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre className="p-4 bg-gray-50 overflow-x-auto text-xs">
                    <code>{curlExample}</code>
                  </pre>
                </div>
              </>
            ) : (
              <>
                {/* Orion-LD Examples */}
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4">
                  <h5 className="font-semibold text-orange-900 mb-2">🔷 NGSI-LD Context Broker</h5>
                  <p className="text-sm text-orange-700">
                    Orion-LD endpoint: <code className="bg-white px-2 py-1 rounded">{ORION_LD_URL}</code>
                  </p>
                </div>

                {/* Python NGSI-LD */}
                <div className="border border-orange-200 rounded-lg overflow-hidden">
                  <div className="bg-orange-100 px-4 py-2 flex justify-between items-center">
                    <span className="font-semibold text-orange-900">🐍 Python + NGSI-LD</span>
                    <button
                      onClick={() => copyToClipboard(orionPythonExample, 'orion_python')}
                      className="px-3 py-1 bg-orange-600 text-white text-sm rounded hover:bg-orange-700"
                    >
                      {copied === 'orion_python' ? '✓ Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre className="p-4 bg-orange-50 overflow-x-auto text-xs">
                    <code>{orionPythonExample}</code>
                  </pre>
                </div>

                {/* curl NGSI-LD */}
                <div className="border border-orange-200 rounded-lg overflow-hidden">
                  <div className="bg-orange-100 px-4 py-2 flex justify-between items-center">
                    <span className="font-semibold text-orange-900">🔧 curl + NGSI-LD</span>
                    <button
                      onClick={() => copyToClipboard(orionCurlExample, 'orion_curl')}
                      className="px-3 py-1 bg-orange-600 text-white text-sm rounded hover:bg-orange-700"
                    >
                      {copied === 'orion_curl' ? '✓ Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre className="p-4 bg-orange-50 overflow-x-auto text-xs">
                    <code>{orionCurlExample}</code>
                  </pre>
                </div>
              </>
            )}
          </div>

          {/* Important Notes */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-900 mb-2">💡 Lưu ý quan trọng</h4>
            <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
              <li>Lưu lại <strong>Device ID</strong> và <strong>API Token</strong> để cấu hình thiết bị IoT</li>
              <li>Token này chỉ hiển thị một lần, hãy sao chép ngay bây giờ</li>
              <li>Dữ liệu gửi lên phải có định dạng: <code>{"{"}"data": {"{"}"key": "value"{"}"}{"}"}</code></li>
              <li>Bạn có thể gửi bất kỳ key nào trong object <code>data</code></li>
              <li>Hệ thống tự động cập nhật <code>last_seen</code> mỗi khi nhận dữ liệu</li>
            </ul>
          </div>
        </div>

        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium"
          >
            Đã hiểu, đóng modal
          </button>
        </div>
      </div>
    </div>
  );
}
