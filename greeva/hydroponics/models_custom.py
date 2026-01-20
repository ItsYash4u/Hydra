
"""
Custom Database Models - Independent of Django's Default User Model
This module defines custom tables with explicit serial numbers and foreign keys.
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
        app_label = 'hydroponics'
        db_table = 'userdevice'
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
    user = models.ForeignKey(
        UserDevice, 
        on_delete=models.CASCADE, 
        to_field='User_ID', 
        db_column='User_ID',
        verbose_name="User (Owner)",
        related_name='devices'
    )
    Device_ID = models.CharField(max_length=50, unique=True, verbose_name="Device ID")
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'hydroponics'
        db_table = 'device'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['Device_ID']),
        ]

    def __str__(self):
        return f"{self.Device_ID} (Owner: {self.user_id})"

class SensorValue(models.Model):
    device = models.ForeignKey(
        Device,
        to_field="Device_ID",
        db_column="Device_ID",
        on_delete=models.CASCADE
    )
    date = models.DateField(primary_key=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pH = models.FloatField(null=True, blank=True)
    EC = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'sensor_value'
