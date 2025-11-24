# Hệ Thống Backend Thành Phố Thông Minh - OLP 2025

## 🎯 Tổng Quan Dự Án

Hệ thống backend hoàn chỉnh cho ứng dụng thành phố thông minh, tuân thủ các tiêu chuẩn quốc tế về dữ liệu mở và IoT.

## ✨ Tính Năng Chính

### 1. Tuân Thủ Standards Quốc Tế
- **NGSI-LD**: API standard của ETSI cho Smart Cities
- **SOSA/SSN**: W3C ontology cho sensor networks
- **JSON-LD**: Linked Data format
- **Smart Data Models**: FIWARE data models

### 2. Quản Lý Dữ Liệu Đô Thị
- 🌤️ **Thời tiết**: Weather stations, temperature, humidity, pressure
- 🌫️ **Chất lượng không khí**: AQI, PM2.5, PM10, NO2, O3, CO, SO2
- 🚗 **Giao thông**: Traffic flow, congestion, speed
- 🏛️ **Dịch vụ công cộng**: Parks, parking, bus stops, hospitals

### 3. Tích Hợp Nguồn Dữ Liệu Mở
- **OpenWeatherMap**: Real-time weather data
- **OpenAQ**: Air quality measurements
- **Extensible**: Dễ dàng thêm nguồn mới (OSM, GTFS, etc.)

### 4. Orion-LD Context Broker
- FIWARE Orion-LD integration
- Real-time data context management
- Temporal and spatial queries
- Subscription notifications

### 5. Auto-Sync với Celery
- Periodic data synchronization
- Background task processing
- Scheduled updates
- Queue management

## 📁 Cấu Trúc Project

```
OPS-2/
├── smartcity/              # Django settings
├── core/                   # NGSI-LD utilities
├── entities/               # Entity management
├── sensors/                # SOSA/SSN sensors
├── observations/           # Observation data
├── integrations/           # External APIs
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── docker-compose.yml      # Docker setup
└── README.md              # Main docs
```

## 🚀 Quick Start

### Khởi động nhanh

```bash
# Clone project
cd /home/huan/Coding/OPS-2

# Setup và start
./start.sh

# Hoặc thủ công
cp .env.example .env
docker-compose up -d
docker-compose exec django python manage.py migrate
```

### Truy cập

- **API**: http://localhost:8000/api/v1/
- **Admin**: http://localhost:8000/admin (admin/admin123)
- **Orion-LD**: http://localhost:1026

## 📚 Documentation

| File | Mô Tả |
|------|-------|
| [README.md](README.md) | Overview và hướng dẫn đầy đủ |
| [QUICKSTART.md](QUICKSTART.md) | Hướng dẫn bắt đầu nhanh |
| [REQUIREMENTS_ANALYSIS.md](REQUIREMENTS_ANALYSIS.md) | Phân tích yêu cầu đề thi |
| [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Cấu trúc code chi tiết |
| [docs/NGSI-LD_GUIDE.md](docs/NGSI-LD_GUIDE.md) | Hướng dẫn NGSI-LD |
| [docs/API_TESTING.md](docs/API_TESTING.md) | Testing APIs |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment |

## 🔧 Tech Stack

### Backend
- **Django 4.2**: Web framework
- **Django REST Framework**: API
- **PostgreSQL**: Database
- **Redis**: Cache & queue
- **Celery**: Task queue

### Standards
- **NGSI-LD**: Smart Cities API
- **JSON-LD**: Linked Data
- **SOSA/SSN**: Sensor ontology
- **Smart Data Models**: FIWARE

### Infrastructure
- **Orion-LD**: Context Broker
- **MongoDB**: Orion-LD storage
- **Docker**: Containerization
- **Nginx**: Web server (production)

## 📊 API Examples

### Get Weather Data
```bash
curl "http://localhost:8000/api/v1/fetch/weather?lat=21.0285&lon=105.8542"
```

### Create Weather Station
```bash
curl -X POST http://localhost:8000/api/v1/weather-stations/ \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "hanoi-1",
    "name": "Hanoi Station",
    "latitude": 21.0285,
    "longitude": 105.8542
  }'
```

### Query from Orion-LD
```bash
curl "http://localhost:8000/api/v1/entities/query_orion/?type=WeatherStation"
```

## 🎯 Đáp Ứng Yêu Cầu OLP 2025

### ✅ Yêu Cầu Bắt Buộc
- [x] Nền tảng dữ liệu đô thị mở
- [x] Mô hình dữ liệu SOSA/SSN
- [x] API NGSI-LD standard
- [x] Smart Data Models
- [x] Tích hợp nguồn dữ liệu mở
- [x] Deployment với Docker
- [x] Documentation đầy đủ

### ⭐ Tính Năng Nổi Bật
- Orion-LD Context Broker
- Real-time auto-sync
- Spatial queries
- Multiple domains
- Production ready
- Extensible architecture

## 🏗️ Kiến Trúc

```
External APIs → Integrations → Django Backend
                                      ↓
                                PostgreSQL
                                      ↓
                              NGSI-LD Entities
                                      ↓
                                 Orion-LD
                                      ↓
                                  REST API
```

## 📖 Học & Tham Khảo

### Standards
- [NGSI-LD Spec](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf)
- [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)
- [Smart Data Models](https://smartdatamodels.org/)

### FIWARE
- [Orion-LD Docs](https://fiware-orion.readthedocs.io/)
- [FIWARE Catalogue](https://www.fiware.org/developers/catalogue/)

### Django
- [Django](https://docs.djangoproject.com/)
- [DRF](https://www.django-rest-framework.org/)

## 🔄 Development Workflow

```bash
# Start development
docker-compose up -d

# Watch logs
docker-compose logs -f django

# Make changes
# ... edit code ...

# Restart if needed
docker-compose restart django

# Run tests
docker-compose exec django python manage.py test

# Stop
docker-compose down
```

## 📦 Production Deployment

```bash
# Build for production
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate

# Collect static
docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic
```

Xem chi tiết: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - xem file LICENSE

## 👥 Team

Developed for **OLP 2025 - Open Source Software Competition**

## 📞 Support

- 📧 Email: support@smartcity.local
- 📚 Docs: `/docs` folder
- 🐛 Issues: GitHub Issues

---

**🌟 Happy Coding!**

Built with ❤️ for Vietnam Smart Cities
