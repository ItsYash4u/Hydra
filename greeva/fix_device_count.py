#!/usr/bin/env python
"""
Fix Device Count Issue - Comprehensive Database Check and Cleanup
"""

import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models import Device, UserDevice

print("=" * 70)
print("DEVICE COUNT FIX - COMPREHENSIVE CHECK")
print("=" * 70)

# Step 1: Check Django ORM
print("\n[STEP 1] Checking via Django ORM...")
orm_count = Device.objects.count()
print(f"   Device.objects.count() = {orm_count}")

if orm_count > 0:
    print(f"\n   Found {orm_count} device(s) via ORM:")
    for device in Device.objects.all():
        print(f"   - ID: {device.S_No}, Device_ID: {device.Device_ID}, User: {device.user_id}")

# Step 2: Check Raw SQL
print("\n[STEP 2] Checking via Raw SQL...")
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM device")
    sql_count = cursor.fetchone()[0]
    print(f"   SELECT COUNT(*) FROM device = {sql_count}")
    
    if sql_count > 0:
        print(f"\n   Found {sql_count} device(s) via SQL:")
        cursor.execute("SELECT S_No, Device_ID, User_ID FROM device")
        for row in cursor.fetchall():
            print(f"   - S_No: {row[0]}, Device_ID: {row[1]}, User_ID: {row[2]}")

# Step 3: Delete all devices if any exist
if orm_count > 0 or sql_count > 0:
    print("\n[STEP 3] Deleting all devices...")
    
    # Try ORM delete
    print("   Attempting ORM delete...")
    deleted_orm, details = Device.objects.all().delete()
    print(f"   ✓ ORM deleted {deleted_orm} object(s)")
    if details:
        print(f"   Details: {details}")
    
    # Verify with raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM device")
        remaining = cursor.fetchone()[0]
        print(f"   Remaining devices (SQL): {remaining}")
        
        if remaining > 0:
            print("\n   ⚠ ORM delete didn't work, trying raw SQL delete...")
            cursor.execute("DELETE FROM device")
            connection.commit()
            cursor.execute("SELECT COUNT(*) FROM device")
            final_count = cursor.fetchone()[0]
            print(f"   ✓ SQL delete completed. Remaining: {final_count}")
else:
    print("\n[STEP 3] No devices found - database is clean!")

# Step 4: Final verification
print("\n[STEP 4] Final Verification...")
final_orm = Device.objects.count()
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM device")
    final_sql = cursor.fetchone()[0]

print(f"   ORM Count: {final_orm}")
print(f"   SQL Count: {final_sql}")

if final_orm == 0 and final_sql == 0:
    print("\n✅ SUCCESS! All devices have been deleted.")
    print("\n📌 NEXT STEPS:")
    print("   1. Refresh your Django admin page (Ctrl+F5 to clear cache)")
    print("   2. If still showing devices, restart the Django server")
else:
    print(f"\n❌ WARNING! Still showing {max(final_orm, final_sql)} devices")
    print("   This might indicate a database constraint or caching issue")

print("\n" + "=" * 70)
