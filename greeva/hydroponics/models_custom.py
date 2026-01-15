"""
Custom Database Models - Independent of Django's Default User Model
This module defines three custom tables with explicit serial numbers and foreign keys.
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class UserDevice(models.Model):
    """
    Custom User table - completely independent of Django's auth.User
    Represents user identity and device ownership.
    """
    S_No = models.AutoField(primary_key=True, verbose_name="Serial Number")
    User_ID = models.CharField(max_length=50, unique=True, verbose_name="User ID")
    Email_ID = models.EmailField(unique=True, verbose_name="Email ID")
    Password = models.CharField(max_length=255, verbose_name="Hashed Password")
    Phone = models.CharField(max_length=15, blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Role = models.CharField(
        max_length=10,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='user',
        verbose_name="User Role"
    )
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'userdevice'   # ✅ matches MySQL
        verbose_name = 'User Device'
        verbose_name_plural = 'User Devices'

    def __str__(self):
        return f"{self.User_ID} ({self.Email_ID})"

    def set_password(self, raw_password):
        self.Password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.Password)


class Device(models.Model):
    """
    Device table - stores device information
    One user can own multiple devices (one-to-many relationship)
    """
    S_No = models.AutoField(primary_key=True, verbose_name="Serial Number")
    User_ID = models.CharField(max_length=50, verbose_name="User ID")
    Device_ID = models.CharField(max_length=50, unique=True, verbose_name="Device ID")
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'device'   # ✅ matches MySQL
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        indexes = [
            models.Index(fields=['User_ID']),
            models.Index(fields=['Device_ID']),
        ]

    def __str__(self):
        return f"{self.Device_ID} (Owner: {self.User_ID})"


class SensorValue(models.Model):
    """
    Maps to existing MySQL table sensor_value
    WITHOUT an auto id column
    """

    Device_ID = models.CharField(max_length=50)
    date = models.DateField(primary_key=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pH = models.FloatField(null=True, blank=True)
    EC = models.FloatField(null=True, blank=True)

    # THIS IS THE CRITICAL LINE


    class Meta:
        managed = False
        db_table = 'sensor_value'


class SensorReading(models.Model):
    """
    High-frequency sensor data storage for IoT.
    Supports 5-second updates and historical tracking.
    """
    id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=50, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Sensor Values (Float for precision)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    ec = models.FloatField(null=True, blank=True)
    tds = models.FloatField(null=True, blank=True)
    co2 = models.FloatField(null=True, blank=True)
    light = models.FloatField(null=True, blank=True) # Light Hours or Intensity
    water_temp = models.FloatField(null=True, blank=True)
    dissolved_oxygen = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'sensor_reading'
        app_label = 'hydroponics'
        indexes = [
            models.Index(fields=['device_id', '-timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device_id} @ {self.timestamp}"

