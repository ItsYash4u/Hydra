"""
Admin configuration for custom database models
Note: Django admin is bypassed for custom authentication
This is for development/debugging purposes only
"""

from django.contrib import admin
from .models import UserDevice, Device, SensorValue


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('S_No', 'User_ID', 'Email_ID', 'Role', 'Phone', 'Age', 'Created_At')
    search_fields = ('User_ID', 'Email_ID')
    list_filter = ('Role', 'Created_At')
    readonly_fields = ('S_No', 'Created_At', 'Updated_At')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('S_No', 'Device_ID', 'User_ID', 'Latitude', 'Longitude', 'Created_At')
    search_fields = ('Device_ID', 'User_ID')
    list_filter = ('Created_At',)
    readonly_fields = ('S_No', 'Created_At', 'Updated_At')


@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = ('S_No', 'Device_ID', 'Temperature', 'pH', 'Humidity', 'Reading_Date', 'Reading_Time')
    search_fields = ('Device_ID',)
    list_filter = ('Reading_Date',)
    readonly_fields = ('S_No', 'Created_At')