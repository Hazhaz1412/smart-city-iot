#!/bin/bash

# View logs for all services or specific service
if [ -z "$1" ]; then
    echo "📋 Showing logs for all services..."
    sudo docker-compose logs -f
else
    echo "📋 Showing logs for $1..."
    sudo docker-compose logs -f $1
fi
