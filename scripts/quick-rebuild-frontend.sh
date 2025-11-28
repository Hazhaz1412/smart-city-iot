#!/bin/bash

# Quick rebuild frontend (no cache to avoid stale builds)
echo "⚡ Quick rebuild frontend (no cache)..."
sudo docker-compose build --no-cache frontend

echo "🔄 Starting frontend..."
sudo docker-compose up -d frontend

echo "✅ Quick rebuild done!"
echo "🌐 Frontend: http://localhost:3000"
echo "💡 Hard refresh browser: Ctrl+Shift+R"
