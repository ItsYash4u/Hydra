from django.urls import path
from .api_views import (
    AddDeviceAPIView, GetDevicesAPIView, PromoteToAdminAPIView,
    SensorDataView, SensorIngestView
)

urlpatterns = [
    path('add-device/', AddDeviceAPIView.as_view(), name='api_add_device'),
    path('devices/', GetDevicesAPIView.as_view(), name='api_get_devices'),
    path('promote-admin/', PromoteToAdminAPIView.as_view(), name='api_promote_admin'),
    
    # New IoT Endpoints
    path('sensors/latest/', SensorDataView.as_view(), name='api_sensor_latest'),
    path('sensors/ingest/', SensorIngestView.as_view(), name='api_sensor_ingest'),
]
