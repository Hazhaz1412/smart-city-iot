import secrets
from django.db import models
from django.contrib.auth.models import User
from .models import UserDevice


class DeviceAPIKey(models.Model):
    """
    API Key riêng cho mỗi thiết bị IoT
    - Không expire
    - Chỉ có quyền gửi data cho 1 device cụ thể
    - An toàn hơn JWT token của user
    """
    device = models.OneToOneField(
        UserDevice,
        on_delete=models.CASCADE,
        related_name='api_key',
        help_text="Thiết bị sở hữu API key này"
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="API key (auto-generated)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Vô hiệu hóa key nếu bị lộ"
    )

    class Meta:
        verbose_name = "Device API Key"
        verbose_name_plural = "Device API Keys"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_id} - {self.key[:16]}..."

    @staticmethod
    def generate_key():
        """Tạo API key ngẫu nhiên 64 ký tự"""
        return secrets.token_urlsafe(48)[:64]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            # Đảm bảo unique
            while DeviceAPIKey.objects.filter(key=self.key).exists():
                self.key = self.generate_key()
        super().save(*args, **kwargs)

    def regenerate(self):
        """Regenerate key mới nếu bị lộ"""
        self.key = self.generate_key()
        while DeviceAPIKey.objects.filter(key=self.key).exclude(pk=self.pk).exists():
            self.key = self.generate_key()
        self.save()
