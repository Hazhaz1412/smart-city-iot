#!/bin/bash

# Quick rebuild frontend with cache (faster)
echo "⚡ Quick rebuild frontend (with cache)..."
sudo docker-compose build frontend

echo "🔄 Restarting frontend..."
sudo docker-compose restart frontend

echo "✅ Quick rebuild done!"
echo "🌐 Frontend: http://localhost:3000"
echo "⚠️  If .env changed, use: ./rebuild-frontend.sh"
