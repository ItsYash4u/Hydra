
import os
import django
import sys
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

from hydroponics.models_custom import UserDevice, Device, SensorReading, SensorValue

def verify_system():
    print("Verifying system...")
    try:
        # 1. Create/Get User
        u, created = UserDevice.objects.get_or_create(
            User_ID="TESTUSER01",
            Email_ID="test@example.com",
            defaults={'Password': 'pbkdf2_...'}
        )
        print(f"User OK: {u.User_ID}")

        # 2. Create/Get Device
        d, created = Device.objects.get_or_create(
            Device_ID="TESTDEV01",
            defaults={
                'user': u,
                'Latitude': 0, 
                'Longitude': 0
            }
        )
        # Ensure relation works
        print(f"Device OK: {d.Device_ID} owned by {d.user.User_ID}")

        # 3. Create Sensor Reading
        sr = SensorReading.objects.create(
            device=d,
            temperature=25.5,
            humidity=60
        )
        print(f"SensorReading OK: ID={sr.id} for Device={sr.device.Device_ID}")
        
        # 4. Verify Backward Relation
        readings = d.readings.all()
        print(f"Device readings count: {readings.count()}")

        print("SUCCESS")
        
    except Exception as e:
        print(f"FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_system()
