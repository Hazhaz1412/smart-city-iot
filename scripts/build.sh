#!/bin/bash

# Build all services from scratch
echo "🔨 Building all services..."
sudo docker-compose build --no-cache

echo "✅ Build completed!"
