"""
Serializers for custom database models
Updated to use UserDevice, Device, SensorValue
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


class SensorValueDTO(serializers.Serializer):
    """DTO for Sensor Values"""
    S_No = serializers.IntegerField(read_only=True)
    Device_ID = serializers.CharField()
    Temperature = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    pH = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    EC = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    Humidity = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    Nitrogen = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    Phosphorus = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    Potassium = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    Light_Hours = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    Moisture = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    Reading_Date = serializers.DateField()
    Reading_Time = serializers.TimeField()


class DeviceDTO(serializers.Serializer):
    """DTO for Device Information"""
    S_No = serializers.IntegerField(read_only=True)
    User_ID = serializers.CharField()
    Device_ID = serializers.CharField()
    Latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    Longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    Created_At = serializers.DateTimeField(read_only=True)


class AnalyticsDTO(serializers.Serializer):
    """DTO for Analytics Response"""
    device_id = serializers.CharField()
    period = serializers.CharField()
    timestamps = serializers.ListField(child=serializers.DateTimeField())
    values = serializers.DictField(child=serializers.ListField(child=serializers.FloatField()))


class MapPointDTO(serializers.Serializer):
    """DTO for a single point on the map"""
    device_id = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    status = serializers.CharField()
    owner_name = serializers.CharField(required=False)


class MapResponseDTO(serializers.Serializer):
    """DTO for Map Response"""
    points = MapPointDTO(many=True)
    center_lat = serializers.FloatField()
    center_lon = serializers.FloatField()
