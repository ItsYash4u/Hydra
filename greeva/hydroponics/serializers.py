
"""
Serializers for custom database models
"""

import json
from rest_framework import serializers
from django.db import IntegrityError, transaction
from django.utils import timezone
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


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='Device_Name', required=True)
    device_type = serializers.ChoiceField(choices=['AIR', 'WATER'], source='Device_Type')
    device_sensors = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True, source='Latitude')
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True, source='Longitude')

    class Meta:
        model = Device
        fields = [
            'device_name',
            'device_type',
            'device_sensors',
            'latitude',
            'longitude',
        ]

    def validate_device_sensors(self, value):
        if not value:
            raise serializers.ValidationError('At least one sensor must be selected.')
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError('User context is required.')

        device_sensors = validated_data.pop('device_sensors', [])
        allowed = {'temperature', 'humidity', 'ph', 'ec', 'co2'}
        normalized = []
        for sensor in device_sensors:
            if not sensor:
                continue
            key = sensor.strip().lower()
            if key in allowed and key not in normalized:
                normalized.append(key)

        latitude = validated_data.get('Latitude')
        longitude = validated_data.get('Longitude')

        if latitude is None or longitude is None:
            raise serializers.ValidationError('Latitude and longitude are required.')

        device_type = validated_data.get('Device_Type')
        attempts = 0

        while attempts < 5:
            attempts += 1
            device_id = Device.generate_device_id(device_type)
            try:
                with transaction.atomic():
                    device = Device.objects.create(
                        user=user,
                        Device_ID=device_id,
                        Device_Sensors=json.dumps(normalized) if normalized else None,
                        **validated_data,
                    )
                    # Create initial sensor row with selected sensors at 0, others null
                    sensor_payload = {
                        'device_id': str(device.Device_ID),
                        'date': timezone.now().date(),
                        'temperature': 0 if 'temperature' in normalized else None,
                        'humidity': 0 if 'humidity' in normalized else None,
                        'pH': 0 if 'ph' in normalized else None,
                        'EC': 0 if 'ec' in normalized else None,
                        'CO2': 0 if 'co2' in normalized else None,
                    }
                    SensorValue.objects.create(**sensor_payload)
                return device
            except IntegrityError:
                continue

        raise serializers.ValidationError('Unable to generate a unique device id. Please try again.')
