#!/bin/bash

echo "======================================"
echo "Smart City Backend - Quick Start"
echo "======================================"

# Check if Docker is running
if ! sudo docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Copy env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys!"
fi

echo ""
echo "Starting services with Docker Compose..."
sudo docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Running database migrations..."
sudo docker-compose exec -T django python manage.py makemigrations
sudo docker-compose exec -T django python manage.py migrate

echo ""
echo "Creating superuser..."
sudo docker-compose exec -T django python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@smartcity.local', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
EOF

echo ""
echo "======================================"
echo "✓ Setup completed successfully!"
echo "======================================"
echo ""
echo "Services:"
echo "  - Django API:    http://localhost:8000"
echo "  - Admin Panel:   http://localhost:8000/admin"
echo "  - Orion-LD:      http://localhost:1026"
echo ""
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Useful commands:"
echo "  - View logs:     sudo docker-compose logs -f"
echo "  - Stop services: sudo docker-compose down"
echo "  - Restart:       sudo docker-compose restart"
echo ""
