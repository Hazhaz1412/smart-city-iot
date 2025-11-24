.PHONY: help start stop restart logs shell migrate test clean setup

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start: ## Start all services
	docker-compose up -d
	@echo "Services started. Access API at http://localhost:8000"

stop: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs (use CTRL+C to exit)
	docker-compose logs -f

shell: ## Open Django shell
	docker-compose exec django python manage.py shell

dbshell: ## Open database shell
	docker-compose exec postgres psql -U postgres -d smartcity_db

migrate: ## Run database migrations
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate

test: ## Run tests
	docker-compose exec django python manage.py test

clean: ## Remove all containers and volumes
	docker-compose down -v
	rm -rf __pycache__ */__pycache__ */*/__pycache__

setup: ## Initial setup (first time only)
	cp -n .env.example .env || true
	docker-compose up -d
	@echo "Waiting for services to start..."
	@sleep 10
	docker-compose exec -T django python manage.py makemigrations
	docker-compose exec -T django python manage.py migrate
	@echo "Creating superuser (username: admin, password: admin123)..."
	@docker-compose exec -T django python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@smartcity.local', 'admin123')"
	@echo ""
	@echo "Setup complete! 🎉"
	@echo "API: http://localhost:8000/api/v1/"
	@echo "Admin: http://localhost:8000/admin (admin/admin123)"

load-sample: ## Load sample data
	docker-compose exec django python manage.py shell < scripts/load_sample_data.py

test-orion: ## Test Orion-LD connection
	docker-compose exec django python scripts/test_orion.py

build: ## Build Docker images
	docker-compose build

rebuild: ## Rebuild and restart services
	docker-compose up -d --build

status: ## Show status of all services
	docker-compose ps

backup-db: ## Backup PostgreSQL database
	docker-compose exec postgres pg_dump -U postgres smartcity_db > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backup_*.sql"

restore-db: ## Restore database from backup (usage: make restore-db FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then echo "Usage: make restore-db FILE=backup.sql"; exit 1; fi
	cat $(FILE) | docker-compose exec -T postgres psql -U postgres smartcity_db

collectstatic: ## Collect static files
	docker-compose exec django python manage.py collectstatic --noinput

createsuperuser: ## Create a new superuser
	docker-compose exec django python manage.py createsuperuser

celery-logs: ## Show Celery worker logs
	docker-compose logs -f celery_worker

orion-logs: ## Show Orion-LD logs
	docker-compose logs -f orion-ld

django-logs: ## Show Django logs
	docker-compose logs -f django
