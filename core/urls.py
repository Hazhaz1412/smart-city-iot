from django.urls import path
from .views import ContextView, HealthCheckView

urlpatterns = [
    path('context', ContextView.as_view(), name='context'),
    path('health', HealthCheckView.as_view(), name='health'),
]
