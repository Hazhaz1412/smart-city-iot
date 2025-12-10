"""
Serializers for External API management
"""
from rest_framework import serializers
from .models import ExternalAPIProvider, UserAPIKey, SystemAPIKey


class ExternalAPIProviderSerializer(serializers.ModelSerializer):
    """Serializer for API Providers (public info)"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    auth_type_display = serializers.CharField(source='get_auth_type_display', read_only=True)
    has_system_key = serializers.SerializerMethodField()
    has_user_key = serializers.SerializerMethodField()
    
    class Meta:
        model = ExternalAPIProvider
        fields = [
            'id', 'name', 'slug', 'category', 'category_display',
            'description', 'base_url', 'documentation_url',
            'auth_type', 'auth_type_display', 'auth_key_name',
            'rate_limit_per_minute', 'rate_limit_per_day',
            'is_active', 'is_premium',
            'has_system_key', 'has_user_key',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_has_system_key(self, obj):
        try:
            return obj.system_key.is_active and obj.system_key.api_key is not None
        except SystemAPIKey.DoesNotExist:
            return False
    
    def get_has_user_key(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return UserAPIKey.objects.filter(
            user=request.user, 
            provider=obj, 
            is_active=True
        ).exists()


class ExternalAPIProviderAdminSerializer(serializers.ModelSerializer):
    """Serializer for API Providers (admin - full access)"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    auth_type_display = serializers.CharField(source='get_auth_type_display', read_only=True)
    system_key_info = serializers.SerializerMethodField()
    user_keys_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ExternalAPIProvider
        fields = '__all__'
    
    def get_system_key_info(self, obj):
        try:
            sk = obj.system_key
            return {
                'is_active': sk.is_active,
                'has_key': sk.api_key is not None,
                'usage_count': sk.usage_count,
                'last_used': sk.last_used
            }
        except SystemAPIKey.DoesNotExist:
            return None
    
    def get_user_keys_count(self, obj):
        return obj.user_keys.filter(is_active=True).count()


class UserAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for User API Keys"""
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    provider_slug = serializers.CharField(source='provider.slug', read_only=True)
    provider_category = serializers.CharField(source='provider.category', read_only=True)
    api_key_masked = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAPIKey
        fields = [
            'id', 'provider', 'provider_name', 'provider_slug', 'provider_category',
            'api_key_masked', 'is_active', 'last_used', 'usage_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['last_used', 'usage_count', 'created_at', 'updated_at']
    
    def get_api_key_masked(self, obj):
        """Return masked API key for display"""
        key = obj.api_key
        if not key:
            return None
        if len(key) <= 8:
            return '*' * len(key)
        return key[:4] + '*' * (len(key) - 8) + key[-4:]


class UserAPIKeyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating User API Keys"""
    api_key = serializers.CharField(write_only=True, required=True)
    credentials = serializers.JSONField(write_only=True, required=False)
    
    class Meta:
        model = UserAPIKey
        fields = ['id', 'provider', 'api_key', 'credentials', 'is_active']
    
    def create(self, validated_data):
        api_key = validated_data.pop('api_key', None)
        credentials = validated_data.pop('credentials', None)
        
        instance = UserAPIKey(**validated_data)
        instance.api_key = api_key
        if credentials:
            instance.credentials = credentials
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        api_key = validated_data.pop('api_key', None)
        credentials = validated_data.pop('credentials', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if api_key:
            instance.api_key = api_key
        if credentials is not None:
            instance.credentials = credentials
        
        instance.save()
        return instance


class SystemAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for System API Keys (admin only)"""
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    provider_slug = serializers.CharField(source='provider.slug', read_only=True)
    api_key_masked = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemAPIKey
        fields = [
            'id', 'provider', 'provider_name', 'provider_slug',
            'api_key_masked', 'is_active', 'allow_user_override',
            'last_used', 'usage_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_used', 'usage_count', 'created_at', 'updated_at']
    
    def get_api_key_masked(self, obj):
        """Return masked API key"""
        key = obj.api_key
        if not key:
            return None
        if len(key) <= 8:
            return '*' * len(key)
        return key[:4] + '*' * (len(key) - 8) + key[-4:]


class SystemAPIKeyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating System API Keys"""
    api_key = serializers.CharField(write_only=True, required=True)
    credentials = serializers.JSONField(write_only=True, required=False)
    
    class Meta:
        model = SystemAPIKey
        fields = ['id', 'provider', 'api_key', 'credentials', 'is_active', 'allow_user_override']
    
    def create(self, validated_data):
        api_key = validated_data.pop('api_key', None)
        credentials = validated_data.pop('credentials', None)
        
        instance = SystemAPIKey(**validated_data)
        instance.api_key = api_key
        if credentials:
            instance.credentials = credentials
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        api_key = validated_data.pop('api_key', None)
        credentials = validated_data.pop('credentials', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if api_key:
            instance.api_key = api_key
        if credentials is not None:
            instance.credentials = credentials
        
        instance.save()
        return instance
