#!/usr/bin/env python
"""
Complete Database Setup and Initialization Script for Greeva Hydroponics
This script ensures all database tables, migrations, and initial data are properly created.
"""
import os
import sys
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.insert(0, str(Path(__file__).parent / 'greeva'))

try:
    django.setup()
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

from django.core.management import call_command
from django.contrib.auth import get_user_model
from greeva.hydroponics.models import Device, SensorData
from django.utils import timezone
import random

def main():
    print("=" * 60)
    print("  Greeva Hydroponics - Complete Database Setup")
    print("=" * 60)
    
    # Step 1: Create migrations for hydroponics app
    print("\n[1/6] Creating migrations for hydroponics app...")
    try:
        call_command('makemigrations', 'hydroponics', interactive=False)
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"! Migration creation warning: {e}")
        # Continue anyway as migrations might already exist
    
    # Step 2: Apply all migrations
    print("\n[2/6] Applying all database migrations...")
    try:
        call_command('migrate', interactive=False, verbosity=1)
        print("✓ All migrations applied successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        sys.exit(1)
    
    # Step 3: Create superuser
    print("\n[3/6] Creating admin user...")
    User = get_user_model()
    email = 'admin@example.com'
    password = 'admin'
    
    try:
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(f"✓ Admin user '{email}' already exists")
        else:
            user = User.objects.create_superuser(email, password)
            print(f"✓ Admin user '{email}' created successfully")
    except Exception as e:
        print(f"✗ User creation failed: {e}")
        sys.exit(1)
    
    # Step 4: Create device
    print("\n[4/6] Setting up IoT device...")
    device_id = 'HYDRO-DEV-001'
    
    try:
        device, created = Device.objects.get_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'latitude': 20.5937,
                'longitude': 78.9629
            }
        )
        if created:
            print(f"✓ Device '{device_id}' created successfully")
        else:
            print(f"✓ Device '{device_id}' already exists")
    except Exception as e:
        print(f"✗ Device creation failed: {e}")
        sys.exit(1)
    
    # Step 5: Create initial sensor data
    print("\n[5/6] Initializing sensor data...")
    try:
        count = SensorData.objects.filter(device=device).count()
        if count == 0:
            # Create initial data point
            SensorData.objects.create(
                device=device,
                temperature=24.5,
                ph=6.8,
                ec=1.8,
                humidity=65.0,
                nitrogen=160.0,
                phosphorus=55.0,
                potassium=210.0,
                light_hours=14.5,
                conductivity=2.2,
                ammonia=0.02,
                dissolved_oxygen=8.5,
                salinity=1.2,
                turbidity=1.5,
                water_level=85.0,
                water_flow=12.0,
                moisture=68.0,
                timestamp=timezone.now()
            )
            print("✓ Initial sensor data created")
        else:
            print(f"✓ Sensor data already exists ({count} records)")
    except Exception as e:
        print(f"! Sensor data warning: {e}")
        # Non-critical, continue
    
    # Step 6: Verify setup
    print("\n[6/6] Verifying setup...")
    try:
        user_count = User.objects.count()
        device_count = Device.objects.count()
        sensor_count = SensorData.objects.count()
        
        print(f"✓ Users: {user_count}")
        print(f"✓ Devices: {device_count}")
        print(f"✓ Sensor Records: {sensor_count}")
        
        print("\n" + "=" * 60)
        print("  Setup Complete!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print(f"  Email:    {email}")
        print(f"  Password: {password}")
        print("\nAccess the dashboard at:")
        print("  http://127.0.0.1:8000/hydroponics/dashboard/")
        print("=" * 60)
        
        return True
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
