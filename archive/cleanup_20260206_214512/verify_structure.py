import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from greeva.hydroponics.models import Device, SensorData

def verify_tables():
    print("=== Verifying Database Structure ===\n")
    
    # 1. Verify User Table
    User = get_user_model()
    print(f"[OK] Table 1: User ({User._meta.db_table})")
    print(f"     - PK: {User._meta.pk.name}")
    print(f"     - Fields: {[f.name for f in User._meta.fields]}")
    if 'phone_number' in [f.name for f in User._meta.fields]:
         print("     - [SUCCESS] custom field 'phone_number' found.")
    else:
         print("     - [FAIL] custom field 'phone_number' MISSING.")

    print("\n")

    # 2. Verify Device Table
    print(f"[OK] Table 2: Device ({Device._meta.db_table})")
    print(f"     - PK: {Device._meta.pk.name}")
    fk = Device._meta.get_field('user')
    print(f"     - FK to User: {fk.related_model.__name__} (Column: {fk.column})")
    print(f"     - Fields: {[f.name for f in Device._meta.fields]}")
    
    print("\n")

    # 3. Verify SensorData Table
    print(f"[OK] Table 3: SensorData ({SensorData._meta.db_table})")
    fk_dev = SensorData._meta.get_field('device')
    print(f"     - FK to Device: {fk_dev.related_model.__name__} (Column: {fk_dev.column})")
    print(f"     - Fields: {[f.name for f in SensorData._meta.fields]}")

    print("\n=== Data Integrity Test ===")
    
    # Create Dummy Data
    try:
        # Create User
        u, created = User.objects.get_or_create(email="test@example.com", defaults={'username': 'testuser'})
        if created:
            u.set_password("argon2_protected_password")
            u.save()
            print("[OK] Created Test User")
        else:
            print("[OK] Found Test User")

        # Create Device
        d, created = Device.objects.get_or_create(device_id="TEST-DEV-001", user=u, defaults={'latitude': 12.0, 'longitude': 77.0})
        if created:
            print("[OK] Created Test Device linked to User")
        else:
            print("[OK] Found Test Device linked to User")

        # Create Sensor Data
        s = SensorData.objects.create(device=d, temperature=25.5, ph=6.5, ec=1.2, humidity=60)
        print(f"[OK] Created Sensor Reading linked to Device: {s}")

    except Exception as e:
        print(f"[FAIL] Data Integrity Error: {e}")

if __name__ == "__main__":
    verify_tables()
