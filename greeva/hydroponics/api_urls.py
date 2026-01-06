from django.urls import path
from .api_views import AddDeviceAPIView, GetDevicesAPIView, PromoteToAdminAPIView

urlpatterns = [
    path('add-device/', AddDeviceAPIView.as_view(), name='api_add_device'),
    path('devices/', GetDevicesAPIView.as_view(), name='api_get_devices'),
    path('promote-admin/', PromoteToAdminAPIView.as_view(), name='api_promote_admin'),
]
