from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from accounts.models import DeviceAPIKey


class DeviceAPIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication cho thiết bị IoT sử dụng API Key
    
    Header: X-Device-API-Key: <key>
    """
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_DEVICE_API_KEY')
        
        if not api_key:
            return None  # Let other auth methods handle it
        
        try:
            device_key = DeviceAPIKey.objects.select_related('device', 'device__user').get(
                key=api_key,
                is_active=True
            )
        except DeviceAPIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive API key')
        
        # Update last_used timestamp
        device_key.last_used = timezone.now()
        device_key.save(update_fields=['last_used'])
        
        # Return (user, auth) tuple
        # We return the device's owner as the authenticated user
        return (device_key.device.user, device_key)
    
    def authenticate_header(self, request):
        return 'X-Device-API-Key'
