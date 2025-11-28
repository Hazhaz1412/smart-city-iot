from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, UserDevice, DeviceData


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 
                  'phone_number', 'organization', 'location')
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'organization', 'avatar', 'bio', 'location',
                  'email_notifications', 'device_count', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined', 'device_count')
    
    def get_device_count(self, obj):
        return obj.devices.count()


class UserDeviceSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    latest_reading = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDevice
        fields = ('id', 'user', 'user_username', 'name', 'device_type', 'device_id', 
                  'description', 'latitude', 'longitude', 'address', 'status', 'is_public',
                  'is_verified', 'verified_at', 'api_endpoint', 'metadata', 'created_at', 
                  'updated_at', 'last_seen', 'latest_reading')
        read_only_fields = ('id', 'user', 'device_id', 'is_verified', 'verified_at', 
                           'created_at', 'updated_at', 'last_seen')
        extra_kwargs = {
            'api_key': {'write_only': True}
        }
    
    def get_latest_reading(self, obj):
        latest = obj.readings.first()
        if latest:
            return {
                'data': latest.data,
                'timestamp': latest.timestamp
            }
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeviceDataSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = DeviceData
        fields = ('id', 'device', 'device_name', 'data', 'timestamp', 'recorded_at')
        read_only_fields = ('id', 'timestamp')


class DeviceDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = ('device', 'data', 'recorded_at')
    
    def validate_device(self, value):
        # Ensure user owns the device
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("You don't have permission to add data to this device.")
        return value
