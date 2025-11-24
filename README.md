# Smart City Backend - OLP 2025

Hệ thống backend thành phố thông minh tuân thủ chuẩn NGSI-LD và SOSA/SSN, với frontend React và hỗ trợ mobile app integration.

![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 🌟 Tính năng

- ✅ **NGSI-LD Compliant**: Tuân thủ chuẩn ETSI NGSI-LD v1.4.1
- ✅ **SOSA/SSN Ontology**: Hỗ trợ đầy đủ W3C sensor ontology
- ✅ **Orion-LD Integration**: Tích hợp FIWARE Context Broker
- ✅ **Real-time Data**: Tự động sync từ OpenWeatherMap, OpenAQ
- ✅ **REST API**: Django REST Framework với pagination, filtering
- ✅ **Interactive UI**: React frontend với maps, charts, real-time updates
- ✅ **Mobile Ready**: Hỗ trợ React Native, Flutter, iOS, Android
- ✅ **Docker Deployment**: One-command deployment với Docker Compose

## 🏗️ Kiến trúc

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   React     │───▶│   Django    │───▶│  Orion-LD   │
│  Frontend   │    │   REST API  │    │   Broker    │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ PostgreSQL  │    │   MongoDB   │
                    └─────────────┘    └─────────────┘
                           │
                    ┌─────────────┐
                    │Redis+Celery │
                    └─────────────┘
```

### Stack công nghệ

**Backend:**
- Django 4.2 + Django REST Framework
- PostgreSQL 15 (main database)
- Redis 7 (cache + task queue)
- Celery (background tasks)

**Context Broker:**
- Orion-LD 1.5.1 (FIWARE)
- MongoDB 6.0 (Orion storage)

**Frontend:**
- React 18.2
- Vite 5.0
- TailwindCSS 3.3
- Leaflet (maps)
- Recharts (charts)

**Standards:**
- NGSI-LD v1.4.1 (ETSI)
- SOSA/SSN (W3C)
- JSON-LD (W3C)
- Smart Data Models

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend dev)
- Git

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd OPS-2

# Copy environment file
cp .env.example .env

# Add your API keys to .env:
# OPENWEATHERMAP_API_KEY=your_key_here
```

### 2. Start All Services

```bash
# Start backend + frontend + databases
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f django
```

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec django python manage.py migrate

# Create admin user
docker-compose exec django python manage.py createsuperuser

# Load sample data (optional)
docker-compose exec django python manage.py create_sample_data
```

### 4. Access Services

- 🌐 **Frontend UI**: http://localhost:3000
- 🔌 **Django API**: http://localhost:8000/api/v1/
- 🔐 **Admin Panel**: http://localhost:8000/admin/
- 📊 **Orion-LD**: http://localhost:1026/
- 📚 **API Docs**: http://localhost:8000/api/docs/

## 📱 Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (hot reload)
npm run dev

# Build for production
npm run build
```

Frontend có:
- ✅ Dashboard với statistics
- ✅ Interactive map (Leaflet)
- ✅ Weather stations & observations
- ✅ Air quality monitoring với AQI
- ✅ Public services directory
- ✅ Real-time data sync

## 📖 API Documentation

### Weather APIs

```bash
# Get all weather stations
GET /api/v1/weather-stations/

# Get weather observations (last 24 hours)
GET /api/v1/weather-observations/?hours=24

# Get latest observation
GET /api/v1/weather-observations/latest/

# Fetch new weather data
POST /api/v1/weather-observations/fetch/
{
  "city": "Hanoi",
  "latitude": 21.0285,
  "longitude": 105.8542
}
```

### Air Quality APIs

```bash
# Get all air quality sensors
GET /api/v1/air-quality-sensors/

# Get observations
GET /api/v1/air-quality-observations/?hours=24

# Fetch new data
POST /api/v1/air-quality-observations/fetch/
{
  "city": "Hanoi"
}
```

### Public Services APIs

```bash
# Get all services
GET /api/v1/public-services/

# Filter by type
GET /api/v1/public-services/?type=hospital

# Find nearby services
GET /api/v1/public-services/nearby/?latitude=21.0285&longitude=105.8542&radius=5000
```

### Integration APIs

```bash
# Sync weather data
POST /api/v1/integrations/sync/weather/

# Sync air quality data
POST /api/v1/integrations/sync/air-quality/

# Check integration status
GET /api/v1/integrations/status/
```

## 📱 Mobile App Integration

Hệ thống hỗ trợ đầy đủ tích hợp mobile app. Xem hướng dẫn chi tiết:

- **[Mobile Integration Guide](docs/MOBILE_INTEGRATION.md)** - Hướng dẫn đầy đủ cho:
  - React Native (với code examples)
  - Flutter (với Dio client)
  - Native iOS (Swift + URLSession)
  - Native Android (Kotlin + Retrofit)

Ví dụ React Native:

```javascript
import { weatherAPI } from './services/smartCity';

// Get weather observations
const data = await weatherAPI.getObservations({ hours: 24 });

// Fetch new weather for current location
const weather = await weatherAPI.fetchWeatherData(
  21.0285,  // latitude
  105.8542, // longitude
  'Hanoi'   // city
);
```

## 🔧 Development

### Run Tests

```bash
# Backend tests
docker-compose exec django python manage.py test

# Frontend tests
cd frontend && npm test
```

### Database Access

```bash
# PostgreSQL shell
docker-compose exec postgres psql -U postgres -d smartcity_db

# Django shell
docker-compose exec django python manage.py shell

# MongoDB shell (Orion data)
docker-compose exec mongo mongosh
```

### Celery Tasks

```bash
# Check active tasks
docker-compose exec celery_worker celery -A smartcity inspect active

# Manual trigger sync
docker-compose exec django python manage.py shell
>>> from integrations.tasks import sync_weather_data
>>> sync_weather_data.delay()
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f django
docker-compose logs -f celery_worker
docker-compose logs -f orion-ld
```

## 📚 Documentation

- **[Quickstart Guide](docs/QUICKSTART.md)** - Chi tiết setup từng bước
- **[API Testing Guide](docs/API_TESTING.md)** - Test tất cả endpoints với curl/httpie
- **[Mobile Integration](docs/MOBILE_INTEGRATION.md)** - React Native, Flutter, iOS, Android
- **[NGSI-LD Guide](docs/NGSI-LD_GUIDE.md)** - Hiểu về NGSI-LD format
- **[SOSA/SSN Guide](docs/SOSA_SSN_GUIDE.md)** - Sensor ontology implementation
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Architecture](docs/ARCHITECTURE.md)** - System design & architecture

## 🗂️ Project Structure

```
OPS-2/
├── smartcity/              # Django project settings
├── core/                   # NGSI-LD utilities, Orion client
├── entities/               # Entity models (WeatherStation, Sensors, etc.)
├── sensors/                # SOSA/SSN sensor models
├── observations/           # Observation models & APIs
├── integrations/           # External API integrations (OpenWeather, OpenAQ)
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api.js         # API client wrapper
│   │   ├── pages/         # React pages
│   │   └── App.jsx        # Main app component
│   ├── Dockerfile
│   └── nginx.conf
├── docs/                   # Documentation
├── docker-compose.yml      # Docker services configuration
└── README.md
```

## 🌐 NGSI-LD Entities

Hệ thống hỗ trợ các entity types sau:

### Weather Station
```json
{
  "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
  "id": "urn:ngsi-ld:WeatherStation:hanoi-001",
  "type": "WeatherStation",
  "name": {"type": "Property", "value": "Hanoi Central Station"},
  "location": {
    "type": "GeoProperty",
    "value": {"type": "Point", "coordinates": [105.8542, 21.0285]}
  }
}
```

### Air Quality Sensor
```json
{
  "id": "urn:ngsi-ld:AirQualitySensor:hanoi-aqi-001",
  "type": "AirQualitySensor",
  "aqi": {"type": "Property", "value": 85, "observedAt": "2024-01-20T10:00:00Z"}
}
```

Xem [NGSI-LD Guide](docs/NGSI-LD_GUIDE.md) để biết thêm chi tiết.

## 🔄 Automatic Data Sync

Celery tasks tự động sync data:

- **Weather**: Mỗi 15 phút từ OpenWeatherMap
- **Air Quality**: Mỗi 30 phút từ OpenAQ

Cấu hình trong `integrations/tasks.py`:

```python
@shared_task
def sync_weather_data():
    """Sync weather data from OpenWeatherMap"""
    # Auto-runs every 15 minutes
    
@shared_task
def sync_air_quality_data():
    """Sync air quality from OpenAQ"""
    # Auto-runs every 30 minutes
```

## 🚢 Production Deployment

### Environment Variables

```env
DEBUG=False
SECRET_KEY=<your-secret-key>
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://redis:6379/0
ORION_LD_URL=http://orion:1026
OPENWEATHERMAP_API_KEY=<your-key>
```

### Build & Deploy

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec django python manage.py migrate --no-input

# Collect static files
docker-compose exec django python manage.py collectstatic --no-input
```

Xem [Deployment Guide](docs/DEPLOYMENT.md) cho chi tiết.

## 🧪 Testing

```bash
# Run all tests
docker-compose exec django python manage.py test

# Run specific app tests
docker-compose exec django python manage.py test entities
docker-compose exec django python manage.py test observations

# Run with coverage
docker-compose exec django coverage run --source='.' manage.py test
docker-compose exec django coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Xem [Contributing Guide](docs/CONTRIBUTING.md) cho chi tiết.

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

Dự án được phát triển cho Olympic Tin học Sinh viên (OLP) 2025.

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our server](https://discord.gg/example)
- 📖 Docs: [Documentation](https://docs.example.com)

## 🙏 Acknowledgments

- [FIWARE](https://www.fiware.org/) - Orion-LD Context Broker
- [ETSI](https://www.etsi.org/) - NGSI-LD Standard
- [W3C](https://www.w3.org/) - SOSA/SSN Ontology
- [OpenWeatherMap](https://openweathermap.org/) - Weather data
- [OpenAQ](https://openaq.org/) - Air quality data

---

**Built with ❤️ for OLP 2025 Smart City Challenge**
