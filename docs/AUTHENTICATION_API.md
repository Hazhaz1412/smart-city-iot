# Authentication & User Device Management API

## Overview

Hệ thống authentication cho phép user đăng ký, đăng nhập, và quản lý thiết bị IoT của riêng họ.

## Features

- ✅ User Registration & Login
- ✅ JWT Token Authentication
- ✅ User Profile Management
- ✅ Personal IoT Device Management
- ✅ Device Data Collection
- ✅ Public Device Sharing
- 🔄 OAuth2 (Google, GitHub) - Coming soon

---

## Authentication Endpoints

### 1. Register User

**POST** `/api/v1/auth/register/`

Đăng ký user mới.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+84901234567",
  "organization": "Smart City Lab",
  "location": "Hanoi, Vietnam"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+84901234567",
    "organization": "Smart City Lab",
    "location": "Hanoi, Vietnam",
    "device_count": 0,
    "date_joined": "2025-11-28T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully!"
}
```

### 2. Login

**POST** `/api/v1/auth/login/`

Đăng nhập bằng username/email và password.

**Request Body:**
```json
{
  "username": "johndoe",  // hoặc email
  "password": "SecurePass123!"
}
```

**Response (200):**
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
  },
  "message": "Login successful!"
}
```

### 3. Refresh Token

**POST** `/api/v1/auth/token/refresh/`

Làm mới access token khi hết hạn.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Get/Update Profile

**GET/PUT** `/api/v1/auth/profile/`

Xem và cập nhật thông tin profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (GET):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+84901234567",
  "organization": "Smart City Lab",
  "avatar": "https://example.com/avatar.jpg",
  "bio": "IoT enthusiast",
  "location": "Hanoi, Vietnam",
  "email_notifications": true,
  "device_count": 5,
  "date_joined": "2025-11-28T10:00:00Z"
}
```

---

## Device Management Endpoints

### 1. List User Devices

**GET** `/api/v1/auth/devices/`

Lấy danh sách thiết bị của user.

**Query Parameters:**
- `type` - Filter by device type (weather_station, air_quality_sensor, traffic_sensor, custom)
- `status` - Filter by status (active, inactive, maintenance)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user": 1,
    "user_username": "johndoe",
    "name": "My Weather Station",
    "device_type": "weather_station",
    "device_id": "ws-home-001",
    "description": "Weather station on my rooftop",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hanoi, Vietnam",
    "status": "active",
    "is_public": true,
    "api_endpoint": null,
    "metadata": {
      "elevation": 15,
      "installation_date": "2025-01-01"
    },
    "created_at": "2025-11-28T10:00:00Z",
    "updated_at": "2025-11-28T10:00:00Z",
    "last_seen": "2025-11-28T15:30:00Z",
    "latest_reading": {
      "data": {
        "temperature": 28.5,
        "humidity": 65,
        "pressure": 1013
      },
      "timestamp": "2025-11-28T15:30:00Z"
    }
  }
]
```

### 2. Create Device

**POST** `/api/v1/auth/devices/`

Thêm thiết bị IoT mới.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "My Weather Station",
  "device_type": "weather_station",
  "device_id": "ws-home-001",
  "description": "Weather station on my rooftop",
  "latitude": 21.0285,
  "longitude": 105.8542,
  "address": "Hanoi, Vietnam",
  "status": "active",
  "is_public": true,
  "api_endpoint": "https://api.example.com/weather",
  "api_key": "secret_key_123",
  "metadata": {
    "elevation": 15,
    "installation_date": "2025-01-01"
  }
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "name": "My Weather Station",
  ...
}
```

### 3. Get Device Detail

**GET** `/api/v1/auth/devices/{id}/`

Xem chi tiết một thiết bị.

### 4. Update Device

**PUT/PATCH** `/api/v1/auth/devices/{id}/`

Cập nhật thông tin thiết bị.

### 5. Delete Device

**DELETE** `/api/v1/auth/devices/{id}/`

Xóa thiết bị.

### 6. Add Device Reading

**POST** `/api/v1/auth/devices/{id}/add_reading/`

Thêm dữ liệu đo từ thiết bị.

**Request Body:**
```json
{
  "data": {
    "temperature": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 5.2
  },
  "recorded_at": "2025-11-28T15:30:00Z"  // optional
}
```

**Response (201):**
```json
{
  "id": 123,
  "device": 1,
  "device_name": "My Weather Station",
  "data": {
    "temperature": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 5.2
  },
  "timestamp": "2025-11-28T15:30:00Z",
  "recorded_at": "2025-11-28T15:30:00Z"
}
```

### 7. Get Device Readings

**GET** `/api/v1/auth/devices/{id}/readings/`

Lấy lịch sử dữ liệu của thiết bị.

**Query Parameters:**
- `hours` - Số giờ lịch sử (default: 24)
- `limit` - Số lượng records tối đa (default: 100)

**Response (200):**
```json
[
  {
    "id": 123,
    "device": 1,
    "device_name": "My Weather Station",
    "data": {
      "temperature": 28.5,
      "humidity": 65
    },
    "timestamp": "2025-11-28T15:30:00Z",
    "recorded_at": "2025-11-28T15:30:00Z"
  },
  ...
]
```

### 8. Get Device Statistics

**GET** `/api/v1/auth/devices/statistics/`

Thống kê thiết bị của user.

**Response (200):**
```json
{
  "total_devices": 5,
  "active_devices": 4,
  "inactive_devices": 1,
  "public_devices": 3,
  "by_type": {
    "weather_station": 2,
    "air_quality_sensor": 2,
    "traffic_sensor": 1
  },
  "total_readings": 1543
}
```

---

## Public Device Endpoints (No Auth Required)

### 1. List Public Devices

**GET** `/api/v1/auth/public-devices/`

Xem tất cả thiết bị public của mọi user.

**Response:** Giống như list user devices

### 2. Get Public Device Detail

**GET** `/api/v1/auth/public-devices/{id}/`

### 3. Get Public Device Readings

**GET** `/api/v1/auth/public-devices/{id}/readings/`

Query parameters giống như device readings.

---

## Device Types

```python
DEVICE_TYPES = [
    ('weather_station', 'Weather Station'),
    ('air_quality_sensor', 'Air Quality Sensor'),
    ('traffic_sensor', 'Traffic Sensor'),
    ('custom', 'Custom Device'),
]
```

## Device Status

```python
STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('maintenance', 'Maintenance'),
]
```

---

## Example Usage Flow

### 1. Register & Login
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### 2. Add Device
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
    "is_public": true
  }'
```

### 3. Send Data to Device
```bash
curl -X POST http://localhost:8000/api/v1/auth/devices/1/add_reading/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 28.5,
      "humidity": 65,
      "pressure": 1013
    }
  }'
```

### 4. View Device Data
```bash
# Your devices
curl -X GET http://localhost:8000/api/v1/auth/devices/1/readings/?hours=24 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Public devices (no auth)
curl -X GET http://localhost:8000/api/v1/auth/public-devices/
```

---

## Token Expiration

- **Access Token**: 1 giờ
- **Refresh Token**: 7 ngày

Khi access token hết hạn, dùng refresh token để lấy access token mới:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Error Codes

- **400** - Bad Request (validation errors)
- **401** - Unauthorized (invalid/expired token)
- **403** - Forbidden (không có quyền)
- **404** - Not Found
- **500** - Server Error

---

## Security Best Practices

1. **Luôn dùng HTTPS** trong production
2. **Không share access token** qua URL hoặc public
3. **Store tokens securely** (localStorage/sessionStorage cho web, Keychain/Keystore cho mobile)
4. **Validate input** trước khi gửi
5. **Set is_public=false** cho device nhạy cảm
6. **API keys** được encrypt trong database

---

## Coming Soon

- 🔄 OAuth2 với Google
- 🔄 OAuth2 với GitHub
- 🔄 Device sharing với user khác
- 🔄 Real-time notifications
- 🔄 Device groups/collections
- 🔄 Advanced analytics dashboard
