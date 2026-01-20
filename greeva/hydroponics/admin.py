
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
        'user',
        'Latitude',
        'Longitude',
        'Created_At',
    )
    search_fields = ('Device_ID', 'user__User_ID')
    list_filter = ('Created_At',)
    readonly_fields = ('Created_At', 'Updated_At')
    ordering = ('-Created_At',)


@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = (
        'device',
        'date',
        'temperature',
        'humidity',
        'pH',
        'EC',
    )
    search_fields = ("device__Device_ID",)
    list_filter = ("device", "date")
    ordering = ('-date',)

    fieldsets = (
        ('Device Information', {
            'fields': ('device', 'date')
        }),
        ('Sensor Readings', {
            'fields': ('temperature', 'humidity', 'pH', 'EC')
        }),
    )
