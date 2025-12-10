from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from django.conf import settings
import json

User = get_user_model()


def get_encryption_key():
    """Get or generate encryption key for API keys"""
    key = getattr(settings, 'API_KEY_ENCRYPTION_KEY', None)
    if not key:
        # Use SECRET_KEY as base for encryption
        import hashlib
        import base64
        hash_key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        key = base64.urlsafe_b64encode(hash_key)
    return key


class ExternalAPIProvider(models.Model):
    """
    Định nghĩa các nhà cung cấp API bên thứ 3
    Admin có thể thêm các provider mới mà không cần sửa code
    """
    CATEGORY_CHOICES = [
        ('weather', 'Thời tiết'),
        ('air_quality', 'Chất lượng không khí'),
        ('traffic', 'Giao thông'),
        ('maps', 'Bản đồ'),
        ('notifications', 'Thông báo'),
        ('other', 'Khác'),
    ]
    
    name = models.CharField(max_length=100, unique=True, help_text="Tên provider (vd: OpenWeatherMap)")
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug để identify (vd: openweathermap)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True, help_text="Mô tả về provider")
    
    # API Configuration
    base_url = models.URLField(help_text="Base URL của API (vd: https://api.openweathermap.org)")
    documentation_url = models.URLField(blank=True, help_text="Link tài liệu API")
    
    # Authentication type
    AUTH_TYPE_CHOICES = [
        ('api_key_query', 'API Key trong Query Params'),
        ('api_key_header', 'API Key trong Header'),
        ('bearer_token', 'Bearer Token'),
        ('basic_auth', 'Basic Auth'),
        ('oauth2', 'OAuth 2.0'),
        ('none', 'Không cần xác thực'),
    ]
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE_CHOICES, default='api_key_query')
    auth_key_name = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Tên param/header cho API key (vd: appid, X-API-Key)"
    )
    
    # Default headers (JSON)
    default_headers = models.JSONField(default=dict, blank=True, help_text="Headers mặc định (JSON)")
    
    # Rate limiting
    rate_limit_per_minute = models.IntegerField(default=60, help_text="Số request tối đa mỗi phút")
    rate_limit_per_day = models.IntegerField(default=1000, help_text="Số request tối đa mỗi ngày")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False, help_text="Yêu cầu subscription trả phí")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'External API Provider'
        verbose_name_plural = 'External API Providers'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class UserAPIKey(models.Model):
    """
    API Keys của user cho các provider
    Mỗi user có thể có API key riêng cho từng provider
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    provider = models.ForeignKey(ExternalAPIProvider, on_delete=models.CASCADE, related_name='user_keys')
    
    # Encrypted API Key
    _encrypted_key = models.BinaryField(db_column='encrypted_key')
    
    # Optional: additional credentials (encrypted JSON)
    _encrypted_credentials = models.BinaryField(null=True, blank=True, db_column='encrypted_credentials')
    
    # Usage tracking
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'provider']
        ordering = ['-created_at']
        verbose_name = 'User API Key'
        verbose_name_plural = 'User API Keys'
    
    def __str__(self):
        return f"{self.user.username} - {self.provider.name}"
    
    @property
    def api_key(self):
        """Decrypt and return API key"""
        if not self._encrypted_key:
            return None
        try:
            f = Fernet(get_encryption_key())
            return f.decrypt(bytes(self._encrypted_key)).decode()
        except Exception:
            return None
    
    @api_key.setter
    def api_key(self, value):
        """Encrypt and store API key"""
        if value:
            f = Fernet(get_encryption_key())
            self._encrypted_key = f.encrypt(value.encode())
        else:
            self._encrypted_key = None
    
    @property
    def credentials(self):
        """Decrypt and return additional credentials"""
        if not self._encrypted_credentials:
            return {}
        try:
            f = Fernet(get_encryption_key())
            decrypted = f.decrypt(bytes(self._encrypted_credentials)).decode()
            return json.loads(decrypted)
        except Exception:
            return {}
    
    @credentials.setter
    def credentials(self, value):
        """Encrypt and store credentials"""
        if value:
            f = Fernet(get_encryption_key())
            self._encrypted_credentials = f.encrypt(json.dumps(value).encode())
        else:
            self._encrypted_credentials = None
    
    def increment_usage(self):
        """Increment usage count and update last_used"""
        from django.utils import timezone
        self.usage_count += 1
        self.last_used = timezone.now()
        self.save(update_fields=['usage_count', 'last_used'])


class SystemAPIKey(models.Model):
    """
    API Keys hệ thống (global) - chỉ admin quản lý
    Dùng làm fallback khi user không có key riêng
    """
    provider = models.OneToOneField(
        ExternalAPIProvider, 
        on_delete=models.CASCADE, 
        related_name='system_key'
    )
    
    # Encrypted API Key
    _encrypted_key = models.BinaryField(db_column='encrypted_key')
    
    # Optional credentials
    _encrypted_credentials = models.BinaryField(null=True, blank=True, db_column='encrypted_credentials')
    
    # Settings
    is_active = models.BooleanField(default=True)
    allow_user_override = models.BooleanField(
        default=True, 
        help_text="Cho phép user dùng key riêng thay vì key hệ thống"
    )
    
    # Usage tracking
    last_used = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System API Key'
        verbose_name_plural = 'System API Keys'
    
    def __str__(self):
        return f"System Key - {self.provider.name}"
    
    @property
    def api_key(self):
        """Decrypt and return API key"""
        if not self._encrypted_key:
            return None
        try:
            f = Fernet(get_encryption_key())
            return f.decrypt(bytes(self._encrypted_key)).decode()
        except Exception:
            return None
    
    @api_key.setter
    def api_key(self, value):
        """Encrypt and store API key"""
        if value:
            f = Fernet(get_encryption_key())
            self._encrypted_key = f.encrypt(value.encode())
        else:
            self._encrypted_key = None
    
    @property
    def credentials(self):
        """Decrypt and return additional credentials"""
        if not self._encrypted_credentials:
            return {}
        try:
            f = Fernet(get_encryption_key())
            decrypted = f.decrypt(bytes(self._encrypted_credentials)).decode()
            return json.loads(decrypted)
        except Exception:
            return {}
    
    @credentials.setter
    def credentials(self, value):
        """Encrypt and store credentials"""
        if value:
            f = Fernet(get_encryption_key())
            self._encrypted_credentials = f.encrypt(json.dumps(value).encode())
        else:
            self._encrypted_credentials = None
    
    def increment_usage(self):
        """Increment usage count"""
        from django.utils import timezone
        self.usage_count += 1
        self.last_used = timezone.now()
        self.save(update_fields=['usage_count', 'last_used'])


def get_api_key_for_provider(provider_slug, user=None):
    """
    Helper function để lấy API key cho một provider
    Ưu tiên: User key > System key > .env fallback
    """
    from django.conf import settings
    
    try:
        provider = ExternalAPIProvider.objects.get(slug=provider_slug, is_active=True)
    except ExternalAPIProvider.DoesNotExist:
        # Fallback to .env
        env_key_name = f"{provider_slug.upper().replace('-', '_')}_API_KEY"
        return getattr(settings, env_key_name, None)
    
    # Try user key first
    if user and provider.system_key.allow_user_override if hasattr(provider, 'system_key') else True:
        try:
            user_key = UserAPIKey.objects.get(user=user, provider=provider, is_active=True)
            if user_key.api_key:
                return user_key.api_key
        except UserAPIKey.DoesNotExist:
            pass
    
    # Try system key
    try:
        system_key = provider.system_key
        if system_key.is_active and system_key.api_key:
            return system_key.api_key
    except SystemAPIKey.DoesNotExist:
        pass
    
    # Fallback to .env
    env_key_name = f"{provider_slug.upper().replace('-', '_')}_API_KEY"
    return getattr(settings, env_key_name, None)
