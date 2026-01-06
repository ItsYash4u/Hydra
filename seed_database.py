"""
Database Seeding Script for Custom Tables
Creates test data: 5-7 users, 7-10 devices per user, multiple sensor readings per device
"""

import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.utils import timezone
# Import custom models
from greeva.hydroponics.models_custom import UserDevice, Device, SensorValue


def seed_database():
    """Seed the database with test data"""
    
    print("🌱 Starting database seeding...")
    
    # Clear existing data
    print("🗑️  Clearing existing data...")
    SensorValue.objects.all().delete()
    Device.objects.all().delete()
    UserDevice.objects.all().delete()
    
    # Create users (1 admin + 5-6 normal users)
    print("👥 Creating users...")
    users = []
    
    # Admin user
    admin = UserDevice(
        User_ID="ADMIN001",
        Email_ID="admin@hydroponics.com",
        Phone="9876543210",
        Age=35,
        Role="admin"
    )
    admin.set_password("admin123")
    admin.save()
    users.append(admin)
    print(f"   ✅ Created admin: {admin.Email_ID}")
    
    # Normal users
    user_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    for i, name in enumerate(user_names, 1):
        user = UserDevice(
            User_ID=f"USER{i:03d}",
            Email_ID=f"{name.lower()}@example.com",
            Phone=f"98765432{10+i:02d}",
            Age=random.randint(25, 55),
            Role="user"
        )
        user.set_password(f"{name.lower()}123")
        user.save()
        users.append(user)
        print(f"   ✅ Created user: {user.Email_ID}")
    
    print(f"\n📱 Creating devices (7-10 per user)...")
    devices = []
    device_counter = 1
    
    for user in users:
        num_devices = random.randint(7, 10)
        for i in range(num_devices):
            device = Device(
                User_ID=user.User_ID,
                Device_ID=f"DEV-{device_counter:04d}",
                Latitude=Decimal(str(round(random.uniform(18.0, 28.0), 6))),
                Longitude=Decimal(str(round(random.uniform(72.0, 88.0), 6)))
            )
            device.save()
            devices.append(device)
            device_counter += 1
        print(f"   ✅ Created {num_devices} devices for {user.User_ID}")
    
    print(f"\n📊 Creating sensor readings (multiple per device)...")
    total_readings = 0
    
    for device in devices:
        # Create 10-20 sensor readings per device
        num_readings = random.randint(10, 20)
        
        for i in range(num_readings):
            # Generate timestamp going back in time
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            reading_datetime = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
            
            sensor_reading = SensorValue(
                Device_ID=device.Device_ID,
                Temperature=Decimal(str(round(random.uniform(18.0, 32.0), 2))),
                pH=Decimal(str(round(random.uniform(5.5, 7.5), 2))),
                EC=Decimal(str(round(random.uniform(1.0, 3.5), 2))),
                Humidity=Decimal(str(round(random.uniform(40.0, 80.0), 2))),
                Nitrogen=Decimal(str(round(random.uniform(50.0, 200.0), 2))),
                Phosphorus=Decimal(str(round(random.uniform(20.0, 80.0), 2))),
                Potassium=Decimal(str(round(random.uniform(100.0, 300.0), 2))),
                Light_Hours=Decimal(str(round(random.uniform(8.0, 16.0), 2))),
                Moisture=Decimal(str(round(random.uniform(30.0, 70.0), 2))),
                Reading_Date=reading_datetime.date(),
                Reading_Time=reading_datetime.time()
            )
            sensor_reading.save()
            total_readings += 1
    
    print(f"   ✅ Created {total_readings} sensor readings")
    
    # Print summary
    print("\n" + "="*60)
    print("✅ DATABASE SEEDING COMPLETE!")
    print("="*60)
    print(f"📊 Summary:")
    print(f"   Users: {UserDevice.objects.count()} (1 admin, {UserDevice.objects.filter(Role='user').count()} users)")
    print(f"   Devices: {Device.objects.count()}")
    print(f"   Sensor Readings: {SensorValue.objects.count()}")
    print("\n🔐 Login Credentials:")
    print(f"   Admin: admin@hydroponics.com / admin123")
    for user in UserDevice.objects.filter(Role='user'):
        username = user.Email_ID.split('@')[0]
        print(f"   User: {user.Email_ID} / {username}123")
    print("="*60)


def verify_relationships():
    """Verify foreign key relationships"""
    print("\n🔍 Verifying Relationships...")
    
    # Check User -> Device relationship
    for user in UserDevice.objects.all():
        device_count = Device.objects.filter(User_ID=user.User_ID).count()
        print(f"   {user.User_ID}: {device_count} devices")
    
    # Check Device -> SensorValue relationship
    sample_devices = Device.objects.all()[:3]
    for device in sample_devices:
        reading_count = SensorValue.objects.filter(Device_ID=device.Device_ID).count()
        print(f"   {device.Device_ID}: {reading_count} sensor readings")
    
    print("✅ Relationship verification complete!")


if __name__ == "__main__":
    seed_database()
    verify_relationships()
