"""
URL Configuration for hydroponics app
Simplified for migration compatibility
"""

from django.urls import path
from . import views

app_name = 'hydroponics'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.search_view, name='search'),
    path('api/latest/<str:device_id>/', views.get_latest_data, name='get_latest_data'),
    path('api/save-sensor-preferences/', views.save_sensor_preferences, name='save_sensor_preferences'),
    path('add-device/', views.add_device_view, name='add_device'),
]
