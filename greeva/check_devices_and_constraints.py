"""
Check devices and database constraints
"""

import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models_custom import Device, UserDevice

print("=" * 70)
print("CHECKING DEVICES AND CONSTRAINTS")
print("=" * 70)

# Check if there are any devices
print("\n[1] Checking Devices:")
device_count = Device.objects.count()
print(f"   Total devices: {device_count}")

if device_count > 0:
    print("\n   Available devices:")
    for device in Device.objects.all():
        print(f"   - Device_ID: '{device.Device_ID}' (Owner: {device.user.User_ID})")
else:
    print("\n   ⚠ NO DEVICES FOUND!")
    print("   You need to add at least one device before adding sensor values.")
    
    # Check if there are users
    user_count = UserDevice.objects.count()
    print(f"\n[2] Checking Users:")
    print(f"   Total users: {user_count}")
    
    if user_count > 0:
        print("\n   Available users:")
        for user in UserDevice.objects.all():
            print(f"   - User_ID: '{user.User_ID}' (Email: {user.Email_ID})")
    else:
        print("\n   ⚠ NO USERS FOUND!")
        print("   You need to create a user first, then add devices.")

# Check database constraints
print("\n[3] Checking Database Constraints:")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT 
            CONSTRAINT_NAME,
            TABLE_NAME,
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'greeva'
        AND TABLE_NAME = 'sensor_value'
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    
    constraints = cursor.fetchall()
    if constraints:
        print("   Foreign key constraints on sensor_value:")
        for constraint in constraints:
            print(f"   - {constraint[0]}: {constraint[1]}.{constraint[2]} -> {constraint[3]}.{constraint[4]}")
    else:
        print("   No foreign key constraints found")

print("\n" + "=" * 70)
print("\n📌 SOLUTION:")
if device_count == 0:
    print("   1. Go to Django Admin -> Devices")
    print("   2. Add at least one device")
    print("   3. Then you can add sensor values for that device")
else:
    print("   Devices are available. Make sure you're selecting from the dropdown.")
print("\n" + "=" * 70)
