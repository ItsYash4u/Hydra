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
]
