# Google OAuth Setup Guide

## Cách lấy Google OAuth Credentials

### 1. Truy cập Google Cloud Console
- Vào https://console.cloud.google.com/
- Đăng nhập với tài khoản Google của bạn

### 2. Tạo Project mới (hoặc chọn project có sẵn)
- Click vào dropdown project ở góc trên bên trái
- Click "NEW PROJECT"
- Đặt tên project: `Smart City IoT`
- Click "CREATE"

### 3. Bật Google+ API
- Vào menu bên trái → "APIs & Services" → "Library"
- Tìm kiếm "Google+ API"
- Click vào và nhấn "ENABLE"

### 4. Tạo OAuth Credentials
- Vào "APIs & Services" → "Credentials"
- Click "CREATE CREDENTIALS" → "OAuth client ID"
- Nếu chưa có OAuth consent screen:
  - Click "CONFIGURE CONSENT SCREEN"
  - Chọn "External"
  - Điền thông tin:
    - App name: `Smart City IoT`
    - User support email: email của bạn
    - Developer contact: email của bạn
  - Click "SAVE AND CONTINUE"
  - Scope: để mặc định, click "SAVE AND CONTINUE"
  - Test users: thêm email của bạn
  - Click "SAVE AND CONTINUE"

### 5. Tạo OAuth Client ID
- Quay lại "Credentials" → "CREATE CREDENTIALS" → "OAuth client ID"
- Application type: "Web application"
- Name: `Smart City IoT Web Client`
- Authorized JavaScript origins:
  ```
  http://localhost:3000
  http://localhost:8000
  ```
- Authorized redirect URIs:
  ```
  http://localhost:3000
  http://localhost:8000/auth/google/
  ```
- Click "CREATE"

### 6. Copy Credentials
Sau khi tạo xong, bạn sẽ thấy popup với:
- **Client ID**: `123456789-abc...xyz.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-abc...xyz`

### 7. Cập nhật vào project

#### Backend (.env file):
```bash
GOOGLE_OAUTH_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
```

#### Frontend (frontend/.env file):
```bash
VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
```

### 8. Restart containers
```bash
sudo docker-compose restart django
sudo docker-compose restart frontend
```

## Test Google Login

1. Truy cập http://localhost:3000/login
2. Bạn sẽ thấy button "Sign in with Google"
3. Click vào button
4. Chọn tài khoản Google
5. Cho phép ứng dụng truy cập thông tin cơ bản
6. Bạn sẽ được chuyển đến trang "Thiết bị của tôi"

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Kiểm tra lại Authorized redirect URIs trong Google Console
- Đảm bảo URL khớp chính xác (http vs https, port number)

### Error: "invalid_client"
- Kiểm tra CLIENT_ID và CLIENT_SECRET có đúng không
- Restart Django container sau khi thay đổi .env

### Google button không hiển thị
- Mở Console (F12) kiểm tra lỗi JavaScript
- Đảm bảo VITE_GOOGLE_CLIENT_ID đã được set trong frontend/.env
- Hard refresh (Ctrl+Shift+R)

## Tính năng

✅ Đăng nhập bằng Google (1 click)
✅ Tự động tạo tài khoản nếu chưa có
✅ Liên kết Google ID với tài khoản hiện có
✅ JWT tokens được tạo tự động
✅ Redirect về trang "Thiết bị của tôi" sau khi login

## API Endpoint

**POST** `/api/v1/auth/google/`

Request body:
```json
{
  "token": "google_id_token_from_frontend"
}
```

Response:
```json
{
  "user": {
    "id": 1,
    "username": "john.doe",
    "email": "john@gmail.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ...",
    "refresh": "eyJ..."
  },
  "message": "Login successful!"
}
```

## Security Notes

- Google ID được lưu trong trường `google_id` của CustomUser
- User có thể login bằng cả Google và password
- OAuth users có `unusable_password()` - không thể login bằng password nếu chỉ đăng ký qua Google
- Token được verify với Google servers trước khi tạo JWT
