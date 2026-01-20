import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from hydroponics.models import Device
from django.db import connection

# Check count
count = Device.objects.count()
print(f"Current devices: {count}")

# Delete all
if count > 0:
    Device.objects.all().delete()
    print("Deleted all devices")
    
# Verify
print(f"Remaining: {Device.objects.count()}")

# Also check via SQL
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM device")
    print(f"SQL count: {cursor.fetchone()[0]}")
