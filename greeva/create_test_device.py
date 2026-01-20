"""
Create a test device and user for testing sensor values
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models_custom import Device, UserDevice

print("=" * 70)
print("CREATING TEST DEVICE")
print("=" * 70)

# Check if user exists
print("\n[1] Checking for users...")
user = UserDevice.objects.first()

if not user:
    print("   No users found. Creating test user...")
    user = UserDevice.objects.create(
        User_ID='test_user',
        Email_ID='test@example.com',
        Phone='1234567890',
        Age=25,
        Role='user'
    )
    user.set_password('password123')
    user.save()
    print(f"   ✓ Created user: {user.User_ID}")
else:
    print(f"   ✓ Using existing user: {user.User_ID}")

# Check if device exists
print("\n[2] Checking for devices...")
device_count = Device.objects.count()

if device_count == 0:
    print("   No devices found. Creating test device...")
    device = Device.objects.create(
        user=user,
        Device_ID='DEVICE_TEST_001',
        Latitude=28.6139,
        Longitude=77.2090
    )
    print(f"   ✓ Created device: {device.Device_ID}")
    print(f"   ✓ Owner: {device.user.User_ID}")
else:
    print(f"   ✓ {device_count} device(s) already exist:")
    for dev in Device.objects.all():
        print(f"      - {dev.Device_ID} (Owner: {dev.user.User_ID})")

print("\n[3] Summary:")
print(f"   Total Users: {UserDevice.objects.count()}")
print(f"   Total Devices: {Device.objects.count()}")

print("\n✅ You can now add sensor values in the Django admin!")
print("   Go to: http://127.0.0.1:8000/admin/hydroponics/sensorvalue/add/")
print("\n" + "=" * 70)
