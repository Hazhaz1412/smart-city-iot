#!/bin/bash

# Run Django management commands
if [ -z "$1" ]; then
    echo "Usage: ./scripts/django.sh <command>"
    echo "Examples:"
    echo "  ./scripts/django.sh makemigrations"
    echo "  ./scripts/django.sh migrate"
    echo "  ./scripts/django.sh createsuperuser"
    echo "  ./scripts/django.sh shell"
    exit 1
fi

echo "🐍 Running Django command: $@"
sudo docker-compose exec django python manage.py "$@"
