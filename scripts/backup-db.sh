#!/bin/bash

# Database backup
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/smartcity_db_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "💾 Backing up database..."
sudo docker-compose exec -T postgres pg_dump -U postgres smartcity_db > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Database backed up to: $BACKUP_FILE"
    echo "📊 Backup size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "❌ Backup failed!"
    exit 1
fi
