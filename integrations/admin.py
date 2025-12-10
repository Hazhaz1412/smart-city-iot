from django.contrib import admin
from .models import ExternalAPIProvider, UserAPIKey, SystemAPIKey


@admin.register(ExternalAPIProvider)
class ExternalAPIProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'auth_type', 'is_active', 'is_premium', 'created_at']
    list_filter = ['category', 'auth_type', 'is_active', 'is_premium']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category', 'name']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('API Configuration', {
            'fields': ('base_url', 'documentation_url', 'auth_type', 'auth_key_name', 'default_headers')
        }),
        ('Rate Limiting', {
            'fields': ('rate_limit_per_minute', 'rate_limit_per_day')
        }),
        ('Status', {
            'fields': ('is_active', 'is_premium')
        }),
    )


@admin.register(UserAPIKey)
class UserAPIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'is_active', 'usage_count', 'last_used', 'created_at']
    list_filter = ['provider', 'is_active']
    search_fields = ['user__username', 'user__email', 'provider__name']
    raw_id_fields = ['user']
    readonly_fields = ['usage_count', 'last_used', 'created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Users should add keys via UI, not admin
        return request.user.is_superuser


@admin.register(SystemAPIKey)
class SystemAPIKeyAdmin(admin.ModelAdmin):
    list_display = ['provider', 'is_active', 'allow_user_override', 'usage_count', 'last_used']
    list_filter = ['is_active', 'allow_user_override']
    search_fields = ['provider__name']
    readonly_fields = ['usage_count', 'last_used', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Provider', {
            'fields': ('provider',)
        }),
        ('API Key', {
            'fields': ('is_active', 'allow_user_override'),
            'description': 'API key được mã hóa và không hiển thị ở đây. Sử dụng UI để quản lý.'
        }),
        ('Usage', {
            'fields': ('usage_count', 'last_used', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
