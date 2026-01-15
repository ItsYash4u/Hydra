"""
Admin configuration for custom database models
Note: Django admin is bypassed for custom authentication
This is for development/debugging purposes only
"""

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

    readonly_fields = (
        'Created_At',
        'Updated_At',
    )

    ordering = ('-Created_At',)


# =========================
# Device Admin
# =========================
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'Device_ID',
        'User_ID',
        'Latitude',
        'Longitude',
        'Created_At',
    )

    search_fields = ('Device_ID', 'User_ID')
    list_filter = ('Created_At',)

    readonly_fields = (
        'Created_At',
        'Updated_At',
    )

    ordering = ('-Created_At',)


# =========================
# SensorValue Admin
# =========================
@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = (
        'Device_ID',
        'temperature',
        'pH',
        'EC',
        'humidity',
        'date',
    )

    search_fields = ('Device_ID',)
    list_filter = ('date',)

    ordering = ('-date',)

    # No readonly fields because this table is unmanaged / legacy
    readonly_fields = ()
