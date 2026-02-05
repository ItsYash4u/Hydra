
"""
Custom Database Models - Independent of Django's Default User Model
This module defines custom tables with explicit serial numbers and foreign keys.
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db import transaction


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
    Name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Full Name")
    profile_image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Profile Image")
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
        verbose_name = 'User'
        verbose_name_plural = 'Users'

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
    Device_Name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Device Name")
    Device_Sensors = models.TextField(blank=True, null=True, verbose_name="Device Sensors", db_column='device_sensors')
    Device_Type = models.CharField(
        max_length=10,
        choices=[('AIR', 'Air Device'), ('WATER', 'Water Device')],
        default='AIR',
        verbose_name="Device Type",
        db_column='device_type'
    )
    Registration_Status = models.CharField(
        max_length=20,
        choices=[('REGISTERED', 'Registered'), ('PENDING', 'Pending')],
        default='REGISTERED',
        verbose_name="Registration Status",
        db_column='registration_status'
    )
    Registered_At = models.DateTimeField(null=True, blank=True, verbose_name="Registered At", db_column='registered_at')
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True, db_column='created_at')
    Updated_At = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        app_label = 'hydroponics'
        db_table = 'device'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['Device_ID']),
            models.Index(fields=['Device_Type']),
        ]

    @classmethod
    def generate_device_id(cls, device_type):
        prefix = "A" if device_type == "AIR" else "W"
        with transaction.atomic():
            last_device = (
                cls.objects
                .select_for_update()
                .filter(Device_Type=device_type)
                .order_by('-Device_ID')
                .first()
            )
            if last_device and last_device.Device_ID:
                try:
                    last_num = int(last_device.Device_ID.split('-')[1])
                except (IndexError, ValueError):
                    last_num = 0
            else:
                last_num = 0

            next_num = last_num + 1
            device_id = f"{prefix}-{next_num:03d}"

            while cls.objects.filter(Device_ID=device_id).exists():
                next_num += 1
                device_id = f"{prefix}-{next_num:03d}"

        return device_id

    def save(self, *args, **kwargs):
        if not self.Device_ID:
            self.Device_ID = self.generate_device_id(self.Device_Type)
        if not self.Registered_At:
            self.Registered_At = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Device_ID} (Owner: {self.user_id})"

class SensorValue(models.Model):
    """
    Sensor readings table - supports multiple readings per device per day
    """
    S_No = models.AutoField(primary_key=True, db_column="S_No")
    device_id = models.CharField(max_length=50, db_column="Device_ID", null=True, blank=True)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pH = models.FloatField(null=True, blank=True)
    EC = models.FloatField(null=True, blank=True)
    CO2 = models.FloatField(null=True, blank=True, db_column="CO2")

    class Meta:
        managed = False
        db_table = 'sensor_value'
        indexes = [
            models.Index(fields=['device_id', '-timestamp']),
            models.Index(fields=['date']),
        ]
        ordering = ['-timestamp']
