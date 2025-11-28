#!/bin/bash

# Database restore from backup
BACKUP_DIR="./backups"

if [ -z "$1" ]; then
    echo "📋 Available backups:"
    ls -lh $BACKUP_DIR/*.sql 2>/dev/null || echo "No backups found!"
    echo ""
    echo "Usage: ./scripts/restore-db.sh <backup_file>"
    echo "Example: ./scripts/restore-db.sh backups/smartcity_db_20251128_120000.sql"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will replace the current database!"
echo "Backup file: $BACKUP_FILE"
read -p "Continue? (y/N): " confirm

if [ "$confirm" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo "🔄 Restoring database..."
sudo docker-compose exec -T postgres psql -U postgres -d smartcity_db < $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Database restored successfully!"
    echo "🔄 Restarting Django..."
    sudo docker-compose restart django
else
    echo "❌ Restore failed!"
    exit 1
fi
