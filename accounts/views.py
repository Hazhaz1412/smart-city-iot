from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.db.models import Q, Count
from datetime import timedelta
from django.utils import timezone
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .models import CustomUser, UserDevice, DeviceData
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    UserDeviceSerializer,
    DeviceDataSerializer,
    DeviceDataCreateSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """Register a new user"""
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login with username/email and password"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username/email and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to authenticate with username or email
    user = authenticate(username=username, password=password)
    
    if not user:
        # Try with email
        try:
            user_obj = CustomUser.objects.get(email=username)
            user = authenticate(username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            pass
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful!'
        })
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """Login or register with Google OAuth"""
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Google token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify the token with Google
        from django.conf import settings
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        )
        
        # Get user info from token
        email = idinfo.get('email')
        google_id = idinfo.get('sub')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        
        if not email:
            return Response({
                'error': 'Email not provided by Google'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        user = None
        try:
            user = CustomUser.objects.get(Q(email=email) | Q(google_id=google_id))
            # Update google_id if not set
            if not user.google_id:
                user.google_id = google_id
                user.save()
        except CustomUser.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
            # Make username unique if needed
            base_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_id=google_id
            )
            # Set unusable password for OAuth users
            user.set_unusable_password()
            user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful!'
        })
        
    except ValueError as e:
        return Response({
            'error': f'Invalid Google token: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Authentication failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user


class UserDeviceViewSet(viewsets.ModelViewSet):
    """CRUD operations for user devices"""
    serializer_class = UserDeviceSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        # Only show devices owned by the current user
        user = self.request.user
        queryset = UserDevice.objects.filter(user=user)
        
        # Filter by device type
        device_type = self.request.query_params.get('type', None)
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.select_related('user').prefetch_related('readings')
    
    def perform_create(self, serializer):
        """Automatically set the user when creating a device"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Verify ownership before updating"""
        device = self.get_object()
        if device.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to edit this device")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Verify ownership before deleting"""
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to delete this device")
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def add_reading(self, request, pk=None):
        """Add a data reading to this device"""
        device = self.get_object()
        
        serializer = DeviceDataCreateSerializer(
            data={'device': device.id, **request.data},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        reading = serializer.save()
        
        # Update last_seen
        device.last_seen = timezone.now()
        device.save(update_fields=['last_seen'])
        
        return Response(
            DeviceDataSerializer(reading).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def readings(self, request, pk=None):
        """Get readings for this device"""
        device = self.get_object()
        
        # Get time range
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        readings = DeviceData.objects.filter(
            device=device,
            timestamp__gte=since
        ).order_by('-timestamp')
        
        # Pagination
        limit = int(request.query_params.get('limit', 100))
        readings = readings[:limit]
        
        serializer = DeviceDataSerializer(readings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get all public devices from all users"""
        devices = UserDevice.objects.filter(
            is_public=True,
            status='active'
        ).select_related('user')
        
        serializer = self.get_serializer(devices, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get user device statistics"""
        user = request.user
        devices = UserDevice.objects.filter(user=user)
        
        stats = {
            'total_devices': devices.count(),
            'active_devices': devices.filter(status='active').count(),
            'inactive_devices': devices.filter(status='inactive').count(),
            'public_devices': devices.filter(is_public=True).count(),
            'verified_devices': devices.filter(is_verified=True).count(),
            'by_type': dict(devices.values('device_type').annotate(count=Count('id')).values_list('device_type', 'count')),
            'total_readings': DeviceData.objects.filter(device__user=user).count(),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """Admin action: Mark device as verified/trusted"""
        device = self.get_object()
        device.is_verified = True
        device.verified_at = timezone.now()
        device.verified_by = request.user
        device.save(update_fields=['is_verified', 'verified_at', 'verified_by'])
        
        return Response({
            'message': f'Device {device.name} has been verified',
            'device': self.get_serializer(device).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def unverify(self, request, pk=None):
        """Admin action: Remove verification"""
        device = self.get_object()
        device.is_verified = False
        device.verified_at = None
        device.verified_by = None
        device.save(update_fields=['is_verified', 'verified_at', 'verified_by'])
        
        return Response({'message': f'Verification removed from {device.name}'})


class PublicDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """View public devices and their data (no authentication required)"""
    serializer_class = UserDeviceSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        return UserDevice.objects.filter(
            is_public=True,
            status='active'
        ).select_related('user').prefetch_related('readings')
    
    @action(detail=True, methods=['get'])
    def readings(self, request, pk=None):
        """Get readings for a public device"""
        device = self.get_object()
        
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        readings = DeviceData.objects.filter(
            device=device,
            timestamp__gte=since
        ).order_by('-timestamp')
        
        limit = int(request.query_params.get('limit', 100))
        readings = readings[:limit]
        
        serializer = DeviceDataSerializer(readings, many=True)
        return Response(serializer.data)
