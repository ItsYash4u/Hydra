from django.urls import path
from .api_views import (
    AddDeviceAPIView, GetDevicesAPIView, PromoteToAdminAPIView,
    SensorDataView, SensorIngestView, SensorHistoryView,
    ReverseGeocodeAPIView, ForwardGeocodeAPIView
)

urlpatterns = [
    path('add-device/', AddDeviceAPIView.as_view(), name='api_add_device'),
    path('devices/', GetDevicesAPIView.as_view(), name='api_get_devices'),
    path('promote-admin/', PromoteToAdminAPIView.as_view(), name='api_promote_admin'),
    
    # New IoT Endpoints
    path('sensors/latest/', SensorDataView.as_view(), name='api_sensor_latest'),
    path('sensors/history/', SensorHistoryView.as_view(), name='api_sensor_history'),
    path('sensors/ingest/', SensorIngestView.as_view(), name='api_sensor_ingest'),
    path('location/reverse/', ReverseGeocodeAPIView.as_view(), name='api_location_reverse'),
    path('location/forward/', ForwardGeocodeAPIView.as_view(), name='api_location_forward'),
]
