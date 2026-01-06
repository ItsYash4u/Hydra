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
        db_table = 'UserDevice'
        verbose_name = 'User Device'
        verbose_name_plural = 'User Devices'

    def __str__(self):
        return f"{self.User_ID} ({self.Email_ID})"

    def set_password(self, raw_password):
        """Hash and set password"""
        self.Password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify password"""
        return check_password(raw_password, self.Password)


class Device(models.Model):
    """
    Device table - stores device information
    One user can own multiple devices (one-to-many relationship)
    """
    S_No = models.AutoField(primary_key=True, verbose_name="Serial Number")
    User_ID = models.CharField(max_length=50, verbose_name="User ID")  # Foreign key to UserDevice.User_ID
    Device_ID = models.CharField(max_length=50, unique=True, verbose_name="Device ID")
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Device'
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
    Sensor Value table - stores sensor readings for each device
    Each device can have multiple sensor readings (one-to-many relationship)
    """
    S_No = models.AutoField(primary_key=True, verbose_name="Serial Number")
    Device_ID = models.CharField(max_length=50, verbose_name="Device ID")  # Foreign key to Device.Device_ID
    
    # Sensor readings
    Temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pH = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    EC = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Electrical Conductivity")
    Humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    Nitrogen = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    Phosphorus = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    Potassium = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    Light_Hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    Moisture = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Separate date and time fields as specified
    Reading_Date = models.DateField(default=timezone.now)
    Reading_Time = models.TimeField(default=timezone.now)
    
    Created_At = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SensorValue'
        verbose_name = 'Sensor Value'
        verbose_name_plural = 'Sensor Values'
        indexes = [
            models.Index(fields=['Device_ID']),
            models.Index(fields=['Reading_Date']),
        ]

    def __str__(self):
        return f"Sensor reading for {self.Device_ID} on {self.Reading_Date} at {self.Reading_Time}"
