
"""
Admin configuration for custom database models
"""

from django import forms
from django.contrib import admin
from .models import UserDevice, Device, SensorValue


# =========================
# UserDevice Admin
# =========================
@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'User_ID',
        'Email_ID',
        'Role',
        'Phone',
        'Age',
        'Created_At',
    )
    search_fields = ('User_ID', 'Email_ID')
    list_filter = ('Role', 'Created_At')
    readonly_fields = ('Created_At', 'Updated_At')
    ordering = ('-Created_At',)


# =========================
# Device Admin
# =========================
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'Device_ID',
        'Device_Name',
        'Device_Type',
        'user',
        'Registration_Status',
        'Registered_At',
        'Latitude',
        'Longitude',
        'Created_At',
    )
    search_fields = ('Device_ID', 'Device_Name', 'user__User_ID')
    list_filter = ('Device_Type', 'Registration_Status', 'Created_At')
    readonly_fields = ('Created_At', 'Updated_At', 'Registered_At')
    ordering = ('-Created_At',)


@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = (
        'device_id',
        'date',
        'temperature',
        'humidity',
        'pH',
        'EC',
        'CO2',
    )
    search_fields = ("device_id",)
    list_filter = ("date",)
    ordering = ('-date',)

    fieldsets = (
        ('Device Information', {
            'fields': ('device_id', 'date')
        }),
        ('Sensor Readings', {
            'fields': ('temperature', 'humidity', 'pH', 'EC', 'CO2')
        }),
    )
