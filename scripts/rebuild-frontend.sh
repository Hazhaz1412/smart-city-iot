#!/bin/bash

# Rebuild only frontend
echo "🎨 Rebuilding frontend (no cache)..."
sudo docker-compose build --no-cache frontend

echo "🚀 Starting frontend..."
sudo docker-compose up -d frontend

echo "✅ Frontend rebuilt!"
echo "🌐 Frontend: http://localhost:3000"
echo "💡 Hard refresh browser: Ctrl+Shift+R"
