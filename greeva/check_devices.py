
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models import Device, UserDevice

print("=" * 60)
print("CHECKING DATABASE STATE")
print("=" * 60)

# Check using Django ORM
print("\n1. Django ORM Query:")
print(f"   Device.objects.count() = {Device.objects.count()}")
print(f"   UserDevice.objects.count() = {UserDevice.objects.count()}")

if Device.objects.exists():
    print("\n   Devices found via ORM:")
    for device in Device.objects.all():
        print(f"   - S_No: {device.S_No}, Device_ID: {device.Device_ID}, User: {device.user_id}")

# Check using raw SQL
print("\n2. Raw SQL Query:")
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM device")
    count = cursor.fetchone()[0]
    print(f"   SELECT COUNT(*) FROM device = {count}")
    
    if count > 0:
        cursor.execute("SELECT S_No, Device_ID, User_ID FROM device")
        rows = cursor.fetchall()
        print(f"\n   Devices found via SQL:")
        for row in rows:
            print(f"   - S_No: {row[0]}, Device_ID: {row[1]}, User_ID: {row[2]}")

# Check table structure
print("\n3. Table Structure:")
with connection.cursor() as cursor:
    cursor.execute("DESCRIBE device")
    columns = cursor.fetchall()
    print("   Columns in 'device' table:")
    for col in columns:
        print(f"   - {col[0]} ({col[1]})")

print("\n" + "=" * 60)
