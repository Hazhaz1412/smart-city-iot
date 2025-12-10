"""
Management command to seed default API providers
"""
from django.core.management.base import BaseCommand
from integrations.models import ExternalAPIProvider, SystemAPIKey
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed default external API providers'

    def handle(self, *args, **options):
        providers_data = [
            {
                'name': 'OpenWeatherMap',
                'slug': 'openweathermap',
                'category': 'weather',
                'description': 'API thời tiết toàn cầu với dữ liệu realtime, dự báo và lịch sử. Free tier: 1000 calls/day.',
                'base_url': 'https://api.openweathermap.org/data/2.5',
                'documentation_url': 'https://openweathermap.org/api',
                'auth_type': 'api_key_query',
                'auth_key_name': 'appid',
                'rate_limit_per_minute': 60,
                'rate_limit_per_day': 1000,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'OpenAQ',
                'slug': 'openaq',
                'category': 'air_quality',
                'description': 'API chất lượng không khí toàn cầu. Dữ liệu từ các trạm quan trắc chính phủ. Miễn phí.',
                'base_url': 'https://api.openaq.org/v3',
                'documentation_url': 'https://docs.openaq.org/',
                'auth_type': 'api_key_header',
                'auth_key_name': 'X-API-Key',
                'rate_limit_per_minute': 60,
                'rate_limit_per_day': 5000,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'WAQI (AQIcn)',
                'slug': 'waqi',
                'category': 'air_quality',
                'description': 'World Air Quality Index - API chất lượng không khí với nhiều trạm tại Việt Nam. Free tier có giới hạn.',
                'base_url': 'https://api.waqi.info',
                'documentation_url': 'https://aqicn.org/api/',
                'auth_type': 'api_key_query',
                'auth_key_name': 'token',
                'rate_limit_per_minute': 30,
                'rate_limit_per_day': 1000,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'IQAir',
                'slug': 'iqair',
                'category': 'air_quality',
                'description': 'API chất lượng không khí premium với dữ liệu chi tiết. Có dữ liệu Việt Nam.',
                'base_url': 'https://api.airvisual.com/v2',
                'documentation_url': 'https://www.iqair.com/air-pollution-data-api',
                'auth_type': 'api_key_query',
                'auth_key_name': 'key',
                'rate_limit_per_minute': 5,
                'rate_limit_per_day': 100,
                'is_active': True,
                'is_premium': True,
            },
            {
                'name': 'Google Maps',
                'slug': 'google-maps',
                'category': 'maps',
                'description': 'Google Maps Platform API cho bản đồ, directions, places.',
                'base_url': 'https://maps.googleapis.com/maps/api',
                'documentation_url': 'https://developers.google.com/maps/documentation',
                'auth_type': 'api_key_query',
                'auth_key_name': 'key',
                'rate_limit_per_minute': 100,
                'rate_limit_per_day': 2500,
                'is_active': True,
                'is_premium': True,
            },
            {
                'name': 'HERE Maps',
                'slug': 'here-maps',
                'category': 'maps',
                'description': 'HERE Maps API - Thay thế Google Maps với pricing tốt hơn.',
                'base_url': 'https://router.hereapi.com/v8',
                'documentation_url': 'https://developer.here.com/documentation',
                'auth_type': 'api_key_query',
                'auth_key_name': 'apiKey',
                'rate_limit_per_minute': 100,
                'rate_limit_per_day': 250000,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'TomTom Traffic',
                'slug': 'tomtom-traffic',
                'category': 'traffic',
                'description': 'TomTom Traffic API cho dữ liệu giao thông realtime.',
                'base_url': 'https://api.tomtom.com/traffic/services',
                'documentation_url': 'https://developer.tomtom.com/traffic-api',
                'auth_type': 'api_key_query',
                'auth_key_name': 'key',
                'rate_limit_per_minute': 30,
                'rate_limit_per_day': 2500,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'Firebase Cloud Messaging',
                'slug': 'firebase-fcm',
                'category': 'notifications',
                'description': 'Firebase Cloud Messaging cho push notifications.',
                'base_url': 'https://fcm.googleapis.com/v1',
                'documentation_url': 'https://firebase.google.com/docs/cloud-messaging',
                'auth_type': 'bearer_token',
                'auth_key_name': 'Authorization',
                'rate_limit_per_minute': 500,
                'rate_limit_per_day': 100000,
                'is_active': True,
                'is_premium': False,
            },
            {
                'name': 'Telegram Bot',
                'slug': 'telegram-bot',
                'category': 'notifications',
                'description': 'Telegram Bot API cho gửi thông báo qua Telegram.',
                'base_url': 'https://api.telegram.org/bot',
                'documentation_url': 'https://core.telegram.org/bots/api',
                'auth_type': 'none',  # Token is in URL path
                'auth_key_name': '',
                'rate_limit_per_minute': 30,
                'rate_limit_per_day': 1000,
                'is_active': True,
                'is_premium': False,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in providers_data:
            provider, created = ExternalAPIProvider.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {provider.name}'))
            else:
                updated_count += 1
                self.stdout.write(f'Updated: {provider.name}')

        # Set system keys from .env if available
        env_keys = {
            'openweathermap': getattr(settings, 'OPENWEATHER_API_KEY', None),
            'openaq': getattr(settings, 'OPENAQ_API_KEY', None),
        }

        for slug, api_key in env_keys.items():
            if api_key:
                try:
                    provider = ExternalAPIProvider.objects.get(slug=slug)
                    system_key, created = SystemAPIKey.objects.get_or_create(provider=provider)
                    system_key.api_key = api_key
                    system_key.is_active = True
                    system_key.save()
                    self.stdout.write(self.style.SUCCESS(f'System key set for: {provider.name}'))
                except ExternalAPIProvider.DoesNotExist:
                    pass

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created_count}, Updated: {updated_count}'
        ))
