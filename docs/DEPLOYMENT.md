# Hướng dẫn Deploy Production

## Deploy với Docker trên VPS/Server

### 1. Chuẩn bị Server

```bash
# Cài đặt Docker và Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Cài đặt Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone và Cấu hình

```bash
# Clone repository
git clone <your-repo-url>
cd OPS-2

# Tạo .env cho production
cp .env.example .env
nano .env
```

Cấu hình production `.env`:

```env
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=your-domain.com,your-ip-address

DATABASE_NAME=smartcity_db
DATABASE_USER=postgres
DATABASE_PASSWORD=<strong-password>
DATABASE_HOST=postgres
DATABASE_PORT=5432

ORION_LD_URL=http://orion-ld:1026

# Add your API keys
OPENWEATHER_API_KEY=your_real_api_key
OPENAQ_API_KEY=your_real_api_key

REDIS_URL=redis://redis:6379/0
```

### 3. Tạo Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    networks:
      - smartcity_network

  redis:
    image: redis:7-alpine
    restart: always
    networks:
      - smartcity_network

  mongo:
    image: mongo:6.0
    command: --replSet rs0
    volumes:
      - mongo_data:/data/db
    restart: always
    networks:
      - smartcity_network

  orion-ld:
    image: fiware/orion-ld:1.5.1
    depends_on:
      - mongo
    command: -dbhost mongo -logLevel INFO -forwarding
    restart: always
    networks:
      - smartcity_network

  django:
    build: .
    command: gunicorn smartcity.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
      - orion-ld
    restart: always
    networks:
      - smartcity_network

  celery_worker:
    build: .
    command: celery -A smartcity worker -l info
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: always
    networks:
      - smartcity_network

  celery_beat:
    build: .
    command: celery -A smartcity beat -l info
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: always
    networks:
      - smartcity_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/staticfiles
      - ./media:/media
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - django
    restart: always
    networks:
      - smartcity_network

volumes:
  postgres_data:
  mongo_data:

networks:
  smartcity_network:
    driver: bridge
```

### 4. Cấu hình Nginx

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server django:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

        client_max_body_size 100M;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /staticfiles/;
        }

        location /media/ {
            alias /media/;
        }
    }
}
```

### 5. Deploy

```bash
# Build và start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec django python manage.py createsuperuser
```

### 6. Setup SSL với Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --webroot -w ./certbot/www -d your-domain.com

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### 7. Monitoring và Logs

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f django
docker-compose -f docker-compose.prod.yml logs -f celery_worker

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 8. Backup Database

```bash
# Backup PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres smartcity_db > backup.sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres smartcity_db < backup.sql
```

## Deploy trên Kubernetes (Optional)

### 1. Tạo Kubernetes Manifests

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcity-django
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smartcity-django
  template:
    metadata:
      labels:
        app: smartcity-django
    spec:
      containers:
      - name: django
        image: your-registry/smartcity:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_HOST
          value: postgres-service
        - name: REDIS_URL
          value: redis://redis-service:6379/0
```

## CI/CD với GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /path/to/OPS-2
            git pull
            docker-compose -f docker-compose.prod.yml up -d --build
            docker-compose -f docker-compose.prod.yml exec -T django python manage.py migrate
            docker-compose -f docker-compose.prod.yml exec -T django python manage.py collectstatic --noinput
```
