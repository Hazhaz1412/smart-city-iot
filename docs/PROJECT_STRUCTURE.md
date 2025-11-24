# Cấu trúc Thư mục Project

```
OPS-2/
├── smartcity/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Cấu hình chính
│   ├── urls.py                # URL routing chính
│   ├── wsgi.py               # WSGI entry point
│   ├── asgi.py               # ASGI entry point
│   └── celery.py             # Celery configuration
│
├── core/                      # Core utilities
│   ├── __init__.py
│   ├── apps.py
│   ├── ngsi_ld.py            # NGSI-LD helper classes
│   ├── orion_client.py       # Orion-LD client
│   ├── urls.py
│   └── views.py              # Health check, context endpoint
│
├── entities/                  # NGSI-LD entities management
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py             # Entity, WeatherStation, etc.
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets
│   ├── urls.py
│   ├── admin.py
│   └── renderers.py          # JSON-LD renderer
│
├── sensors/                   # SOSA/SSN sensors
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py             # Sensor, Platform, Deployment
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── observations/              # Observation data
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py             # Weather, AirQuality, Traffic observations
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── integrations/              # External data sources
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── openweather.py        # OpenWeatherMap client
│   ├── openaq.py             # OpenAQ client
│   ├── tasks.py              # Celery tasks
│   ├── views.py              # API views
│   ├── urls.py
│   └── admin.py
│
├── scripts/                   # Utility scripts
│   ├── load_sample_data.py   # Load sample data
│   ├── test_orion.py         # Test Orion-LD connection
│   └── setup.py              # Setup script
│
├── docs/                      # Documentation
│   ├── API_TESTING.md        # API testing guide
│   └── DEPLOYMENT.md         # Deployment guide
│
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
├── start.sh                   # Quick start script
├── .env.example              # Environment variables template
├── .gitignore
└── README.md                  # Main documentation
```

## Module Descriptions

### smartcity/
Django project root với cấu hình chính, URL routing, và Celery setup.

### core/
Các utility classes và functions cho NGSI-LD và Orion-LD integration:
- `NGSILDContext`: Quản lý JSON-LD context
- `NGSILDEntity`: Base class tạo NGSI-LD entities
- `SOSAObservation`, `SOSASensor`: SOSA/SSN entities
- `OrionLDClient`: Client để tương tác với Orion-LD

### entities/
Quản lý các NGSI-LD entities:
- Weather Stations
- Air Quality Sensors
- Traffic Sensors
- Public Services (parks, parking lots, etc.)

### sensors/
Triển khai SOSA/SSN ontology:
- Sensor: Thiết bị cảm biến
- Platform: Nơi đặt sensors
- SensorDeployment: Deployment information

### observations/
Lưu trữ dữ liệu observations:
- Weather observations
- Air quality observations
- Traffic observations

### integrations/
Tích hợp với external data sources:
- OpenWeatherMap API
- OpenAQ API
- Celery tasks cho sync tự động

## Data Flow

```
External APIs (OpenWeather, OpenAQ)
    ↓
Integrations Module (fetch data)
    ↓
Observations Models (store in PostgreSQL)
    ↓
NGSI-LD Entities (create JSON-LD format)
    ↓
Orion-LD Context Broker (sync via OrionLDClient)
    ↓
REST API (expose via Django REST Framework)
```

## Database Schema

### Main Tables
- `entities_entity`: Tất cả NGSI-LD entities
- `entities_weatherstation`: Weather stations
- `entities_airqualitysensor`: Air quality sensors
- `sensors_sensor`: SOSA sensors
- `sensors_platform`: SOSA platforms
- `observations_weatherobservation`: Weather data
- `observations_airqualityobservation`: Air quality data

## API Endpoints Structure

```
/api/v1/
├── health                     # Health check
├── context                    # JSON-LD context
│
├── entities/                  # NGSI-LD entities
│   ├── GET, POST             # List, create
│   ├── {id}/                 # Detail
│   ├── {id}/sync_to_orion/   # Sync to Orion-LD
│   └── query_orion/          # Query from Orion-LD
│
├── weather-stations/          # Weather stations
│   ├── GET, POST
│   ├── {id}/
│   └── nearby/               # Find nearby
│
├── air-quality-sensors/       # AQ sensors
│   ├── GET, POST
│   └── {id}/
│
├── sensors/                   # SOSA sensors
├── platforms/                 # SOSA platforms
│
├── weather/                   # Weather observations
│   ├── GET, POST
│   └── latest/               # Latest observation
│
├── air-quality/               # AQ observations
│   ├── GET, POST
│   └── latest/
│
├── traffic/                   # Traffic observations
│
├── sync/
│   ├── weather/              # Sync weather data
│   └── air-quality/          # Sync AQ data
│
└── fetch/
    ├── weather/              # Fetch weather for location
    └── air-quality/          # Fetch AQ for location
```
