# 🚀 Authentication & User Device Management - Quick Start

## Tính năng mới

✅ **User Registration & Login** với JWT tokens  
✅ **User Profile Management**  
✅ **Personal IoT Device Management** - User tự thêm và quản lý thiết bị của mình  
✅ **Real-time Device Data Collection**  
✅ **Public Device Sharing** - Chia sẻ thiết bị public cho mọi người xem  
✅ **Device Statistics & Analytics**

---

## Demo nhanh

### 1. Đăng ký user mới

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "organization": "Smart City Lab"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    ...
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Login (nếu đã có account)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### 3. Thêm thiết bị IoT của bạn

```bash
curl -X POST http://localhost:8000/api/v1/auth/devices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Weather Station",
    "device_type": "weather_station",
    "device_id": "ws-home-001",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hanoi, Vietnam",
    "is_public": true,
    "description": "Weather station on my rooftop"
  }'
```

### 4. Gửi dữ liệu từ thiết bị

```bash
curl -X POST http://localhost:8000/api/v1/auth/devices/1/add_reading/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 28.5,
      "humidity": 65,
      "pressure": 1013,
      "wind_speed": 5.2
    }
  }'
```

### 5. Xem thiết bị public của mọi người (không cần login)

```bash
curl http://localhost:8000/api/v1/auth/public-devices/
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Đăng ký
- `POST /api/v1/auth/login/` - Đăng nhập
- `POST /api/v1/auth/token/refresh/` - Refresh token
- `GET/PUT /api/v1/auth/profile/` - Xem/sửa profile

### Device Management (Cần authentication)
- `GET /api/v1/auth/devices/` - List thiết bị của bạn
- `POST /api/v1/auth/devices/` - Thêm thiết bị mới
- `GET /api/v1/auth/devices/{id}/` - Chi tiết thiết bị
- `PUT/PATCH /api/v1/auth/devices/{id}/` - Cập nhật thiết bị
- `DELETE /api/v1/auth/devices/{id}/` - Xóa thiết bị
- `POST /api/v1/auth/devices/{id}/add_reading/` - Thêm dữ liệu
- `GET /api/v1/auth/devices/{id}/readings/` - Xem lịch sử dữ liệu
- `GET /api/v1/auth/devices/statistics/` - Thống kê

### Public Devices (Không cần auth)
- `GET /api/v1/auth/public-devices/` - Xem tất cả thiết bị public
- `GET /api/v1/auth/public-devices/{id}/` - Chi tiết thiết bị public
- `GET /api/v1/auth/public-devices/{id}/readings/` - Dữ liệu thiết bị public

---

## Device Types

- `weather_station` - Trạm thời tiết
- `air_quality_sensor` - Cảm biến chất lượng không khí
- `traffic_sensor` - Cảm biến giao thông
- `custom` - Thiết bị tùy chỉnh

---

## JWT Token

**Access Token**: Hết hạn sau 1 giờ  
**Refresh Token**: Hết hạn sau 7 ngày

Khi access token hết hạn, dùng refresh token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Use Cases

### 📱 Mobile App Developer
```javascript
// React Native / Flutter
const registerUser = async () => {
  const response = await fetch('http://api.smartcity.com/api/v1/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'user123',
      email: 'user@example.com',
      password: 'SecurePass123!',
      password2: 'SecurePass123!'
    })
  });
  const data = await response.json();
  // Store tokens
  localStorage.setItem('access_token', data.tokens.access);
  localStorage.setItem('refresh_token', data.tokens.refresh);
}
```

### 🏠 IoT Device Owner
```python
# Arduino/ESP32 gửi dữ liệu
import requests

TOKEN = "your_access_token"
DEVICE_ID = 1

data = {
    "data": {
        "temperature": 28.5,
        "humidity": 65
    }
}

response = requests.post(
    f"http://api.smartcity.com/api/v1/auth/devices/{DEVICE_ID}/add_reading/",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json=data
)
```

### 🌍 Public Data Consumer
```bash
# Không cần authentication - xem thiết bị public
curl http://localhost:8000/api/v1/auth/public-devices/ | jq .
```

---

## Database Schema

### CustomUser
- Username, email, password
- Profile: phone, organization, avatar, bio, location
- OAuth: google_id, github_id
- Preferences: email_notifications

### UserDevice
- Thuộc về user
- Device info: name, type, device_id
- Location: lat/long, address
- Status: active/inactive/maintenance
- Privacy: is_public (share với mọi người)
- API connection: endpoint, api_key
- Metadata: JSON tùy chỉnh

### DeviceData
- Thuộc về device
- Data: JSON linh hoạt (bất kỳ sensor data nào)
- Timestamps: timestamp, recorded_at

---

## Admin Panel

Truy cập: http://localhost:8000/admin

**Superuser mặc định:**
- Username: `admin`
- Password: `admin123`

Có thể xem và quản lý:
- Users
- User Devices
- Device Data

---

## Full Documentation

📖 Chi tiết API: [docs/AUTHENTICATION_API.md](docs/AUTHENTICATION_API.md)

---

## Tested & Working ✅

```bash
✅ User Registration
✅ User Login
✅ JWT Token Authentication
✅ Profile Management
✅ Device Creation
✅ Device Data Upload
✅ Device Readings Query
✅ Public Device Sharing
✅ Device Statistics
```

---

## Next Steps

🔄 **OAuth2 Integration** (Google, GitHub)  
🔄 **Device Sharing** between users  
🔄 **Real-time Notifications** (WebSocket)  
🔄 **Device Groups/Collections**  
🔄 **Advanced Analytics Dashboard**  
🔄 **Device Control** (actuators, commands)

---

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework 3.14
- **Auth**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis, Celery
- **Standards**: NGSI-LD, SOSA/SSN
- **Deployment**: Docker Compose

---

Tạo bởi: Smart City IoT Platform Team 🚀
