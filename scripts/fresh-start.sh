#!/bin/bash

# Stop and remove all containers, networks, and volumes
echo "🛑 Stopping all services..."
sudo docker-compose down -v

echo "🔨 Building all services..."
sudo docker-compose build --no-cache

echo "🚀 Starting all services..."
sudo docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 5

echo "📊 Running migrations..."
sudo docker-compose exec django python manage.py migrate

echo "✅ Fresh start completed!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
