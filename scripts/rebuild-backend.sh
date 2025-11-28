#!/bin/bash

# Rebuild only backend
echo "⚙️ Rebuilding backend (no cache)..."
sudo docker-compose build --no-cache django

echo "🔄 Restarting backend services..."
sudo docker-compose up -d django celery_worker celery_beat

echo "📊 Running migrations..."
sleep 3
sudo docker-compose exec django python manage.py migrate

echo "✅ Backend rebuilt!"
echo "🔧 Backend API: http://localhost:8000"
