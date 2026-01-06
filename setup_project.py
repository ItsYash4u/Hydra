
import os
import sys
import django
from django.utils import timezone
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from greeva.hydroponics.models import Device, SensorData

def setup():
    print("Running migrations...")
    call_command('makemigrations', 'hydroponics')
    call_command('migrate')

    User = get_user_model()
    email = 'admin@example.com'
    password = 'admin'
    
    print(f"Creating/Checking user {email}...")
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_superuser(email, password)
        print("Superuser created.")
    else:
        user = User.objects.get(email=email)
        print("Superuser already exists.")

    print("Creating/Checking device...")
    device_id = 'DEV-001'
    device, created = Device.objects.get_or_create(user=user, device_id=device_id)
    if created:
        print(f"Device {device_id} created.")
        device.latitude = 20.5937
        device.longitude = 78.9629
        device.save()
    else:
        print(f"Device {device_id} already exists.")

    print("Checking initial sensor data...")
    if not SensorData.objects.filter(device=device).exists():
        print("Creating initial sensor data...")
        SensorData.objects.create(
            device=device,
            temperature=24.0,
            ph=6.5,
            ec=1.5,
            humidity=60.0,
            nitrogen=150,
            phosphorus=50,
            potassium=200,
            light_hours=12,
            conductivity=2.0,
            ammonia=0.0,
            dissolved_oxygen=8.0,
            salinity=1.0,
            turbidity=1.0,
            water_level=80.0,
            water_flow=10.0,
            moisture=60.0,
            timestamp=timezone.now()
        )
        print("Initial sensor data created.")
    else:
        print("Sensor data already exists.")

    print("Setup complete.")

if __name__ == '__main__':
    setup()
