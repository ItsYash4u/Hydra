
"""
Serializers for custom database models
"""

from rest_framework import serializers
from .models import UserDevice, Device, SensorValue


class UserDeviceDTO(serializers.Serializer):
    """DTO for UserDevice"""
    S_No = serializers.IntegerField(read_only=True)
    User_ID = serializers.CharField()
    Email_ID = serializers.EmailField()
    Phone = serializers.CharField(required=False, allow_blank=True)
    Age = serializers.IntegerField(required=False, allow_null=True)
    Role = serializers.ChoiceField(choices=['admin', 'user'])
    Created_At = serializers.DateTimeField(read_only=True)


class SensorValueSerializer(serializers.ModelSerializer):
    """Serializer for SensorValue (RESTORED)"""
    class Meta:
        model = SensorValue
        fields = '__all__'


class DeviceDTO(serializers.Serializer):
    """DTO for Device Information"""
    S_No = serializers.IntegerField(read_only=True)
    User_ID = serializers.CharField(source='user_id')
    Device_ID = serializers.CharField()
    Latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    Longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    Created_At = serializers.DateTimeField(read_only=True)
