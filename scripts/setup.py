"""
Setup script to initialize database and create sample data
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def run_setup():
    print("=" * 50)
    print("Smart City Backend Setup")
    print("=" * 50)
    
    # Create migrations
    print("\n1. Creating migrations...")
    call_command('makemigrations')
    
    # Run migrations
    print("\n2. Running migrations...")
    call_command('migrate')
    
    # Create superuser
    print("\n3. Creating superuser...")
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@smartcity.local',
            password='admin123'
        )
        print("✓ Superuser created: admin / admin123")
    else:
        print("✓ Superuser already exists")
    
    # Collect static files
    print("\n4. Collecting static files...")
    call_command('collectstatic', '--noinput')
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now:")
    print("1. Access admin panel: http://localhost:8000/admin")
    print("2. Username: admin")
    print("3. Password: admin123")
    print("\nAPI Documentation: http://localhost:8000/api/v1/")

if __name__ == '__main__':
    run_setup()
