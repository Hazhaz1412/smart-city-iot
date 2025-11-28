from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserDevice, DeviceData


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'organization', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'organization')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'organization', 'avatar', 'bio', 'location')
        }),
        ('OAuth', {
            'fields': ('google_id', 'github_id')
        }),
        ('Preferences', {
            'fields': ('email_notifications',)
        }),
    )


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'device_id', 'user', 'status', 'is_public', 'last_seen', 'created_at')
    list_filter = ('device_type', 'status', 'is_public', 'created_at')
    search_fields = ('name', 'device_id', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at', 'last_seen')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'device_type', 'device_id', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address')
        }),
        ('Status', {
            'fields': ('status', 'is_public', 'last_seen')
        }),
        ('API Connection', {
            'fields': ('api_endpoint', 'api_key')
        }),
        ('Metadata', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'recorded_at')
    list_filter = ('timestamp', 'device__device_type')
    search_fields = ('device__name', 'device__device_id')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
