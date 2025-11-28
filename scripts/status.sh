#!/bin/bash

# Check status of all services
echo "📊 Service Status:"
echo "=================="
sudo docker-compose ps

echo ""
echo "💾 Database Status:"
sudo docker-compose exec postgres psql -U postgres -d smartcity_db -c "SELECT COUNT(*) as total_users FROM accounts_customuser;" 2>/dev/null || echo "❌ Database not accessible"

echo ""
echo "🌐 Health Check:"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000/api/v1/health/"
curl -s http://localhost:8000/api/v1/health/ | python3 -m json.tool 2>/dev/null || echo "❌ Backend not responding"
