# Quick Start Guide - Hướng dẫn Bắt đầu Nhanh

## 🚀 Khởi động trong 5 phút

### Bước 1: Clone và Cấu hình (1 phút)

```bash
cd /home/huan/Coding/OPS-2

# Tạo file môi trường
cp .env.example .env

# Chỉnh sửa .env và thêm API keys (optional cho demo)
nano .env
```

### Bước 2: Khởi động với Docker (2 phút)

```bash
# Sử dụng script tự động
./start.sh

# Hoặc khởi động thủ công
docker-compose up -d
```

### Bước 3: Chạy Migrations (1 phút)

```bash
# Tạo và chạy migrations
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate

# Tạo superuser
docker-compose exec django python manage.py createsuperuser
```

### Bước 4: Load dữ liệu mẫu (1 phút)

```bash
docker-compose exec django python manage.py shell < scripts/load_sample_data.py
```

### Bước 5: Test API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Lấy danh sách weather stations
curl http://localhost:8000/api/v1/weather-stations/

# Truy cập admin panel
# http://localhost:8000/admin
```

## 📋 Checklist Sau Khi Cài Đặt

- [ ] Tất cả services đang chạy: `docker-compose ps`
- [ ] Database đã migrate: check logs
- [ ] Superuser đã tạo: có thể login admin
- [ ] API hoạt động: curl health endpoint
- [ ] Orion-LD đã khởi động: `curl http://localhost:1026/version`

## 🔧 Lệnh Thường Dùng

### Docker
```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs service cụ thể
docker-compose logs -f django
docker-compose logs -f orion-ld

# Restart service
docker-compose restart django

# Stop tất cả
docker-compose down

# Xóa volumes (cẩn thận!)
docker-compose down -v
```

### Django
```bash
# Django shell
docker-compose exec django python manage.py shell

# Tạo migrations
docker-compose exec django python manage.py makemigrations

# Chạy migrations
docker-compose exec django python manage.py migrate

# Tạo superuser
docker-compose exec django python manage.py createsuperuser

# Collect static files
docker-compose exec django python manage.py collectstatic
```

### Database
```bash
# Truy cập PostgreSQL shell
docker-compose exec postgres psql -U postgres -d smartcity_db

# Backup database
docker-compose exec postgres pg_dump -U postgres smartcity_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U postgres smartcity_db
```

## 🧪 Testing APIs

### 1. Tạo Weather Station

```bash
curl -X POST http://localhost:8000/api/v1/weather-stations/ \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "test-station-1",
    "name": "Test Weather Station",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "address": "Hanoi, Vietnam"
  }'
```

### 2. Fetch Weather Data từ OpenWeatherMap

```bash
# Cần API key trong .env
curl "http://localhost:8000/api/v1/fetch/weather?lat=21.0285&lon=105.8542&city=Hanoi"
```

### 3. Query Entities từ Orion-LD

```bash
curl "http://localhost:8000/api/v1/entities/query_orion/?type=WeatherStation"
```

### 4. Test Orion-LD trực tiếp

```bash
# Version check
curl http://localhost:1026/version

# Query entities
curl http://localhost:1026/ngsi-ld/v1/entities \
  -H "Accept: application/ld+json"
```

## 📊 Accessing Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Django API | http://localhost:8000/api/v1/ | - |
| Admin Panel | http://localhost:8000/admin | admin/admin123 |
| Orion-LD | http://localhost:1026 | - |
| PostgreSQL | localhost:5432 | postgres/postgres |
| Redis | localhost:6379 | - |
| MongoDB | localhost:27017 | - |

## 🐛 Troubleshooting

### Services không khởi động

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild images
docker-compose up -d --build
```

### Database connection error

```bash
# Wait for postgres to be ready
docker-compose exec postgres pg_isready

# Restart postgres
docker-compose restart postgres
```

### Orion-LD không hoạt động

```bash
# Check MongoDB
docker-compose exec mongo mongosh --eval "db.version()"

# Restart Orion-LD
docker-compose restart orion-ld

# Check logs
docker-compose logs orion-ld
```

### Port already in use

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process or change port in docker-compose.yml
```

## 🎯 Next Steps

1. **Thêm API Keys**: Edit `.env` để thêm OpenWeatherMap và OpenAQ API keys
2. **Load Sample Data**: Chạy `scripts/load_sample_data.py`
3. **Test Integration**: Test fetch weather/air quality data
4. **Explore Admin**: Truy cập admin panel để quản lý data
5. **Read Docs**: Đọc docs trong `/docs` folder

## 📚 Documentation

- [README.md](../README.md) - Tổng quan project
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - Cấu trúc code
- [NGSI-LD_GUIDE.md](./NGSI-LD_GUIDE.md) - Hướng dẫn NGSI-LD
- [API_TESTING.md](./API_TESTING.md) - Chi tiết API testing
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Hướng dẫn deploy production

## 💡 Tips

- Sử dụng `docker-compose logs -f` để monitor real-time logs
- Thêm API keys để test tích hợp với external sources
- Explore Django admin để quản lý data dễ dàng
- Sử dụng Postman/Insomnia để test API thay vì curl
- Read NGSI-LD guide để hiểu data models

## 🆘 Cần Trợ Giúp?

1. Check logs: `docker-compose logs -f`
2. Read documentation trong `/docs`
3. Check GitHub issues
4. Contact team

---

**Happy Coding! 🎉**
