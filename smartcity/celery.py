"""
Celery configuration for smartcity project.
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity.settings')

app = Celery('smartcity')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'sync-weather-data': {
        'task': 'integrations.tasks.sync_weather_data',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'sync-air-quality-data': {
        'task': 'integrations.tasks.sync_air_quality_data',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}
