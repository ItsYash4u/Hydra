
import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

try:
    from greeva.hydroponics.models_custom import SensorValue, Device, UserDevice
    print(f"Deleting {SensorValue.objects.count()} SensorValues...")
    SensorValue.objects.all().delete()
    print(f"Deleting {Device.objects.count()} Devices...")
    Device.objects.all().delete()
    print(f"Deleting {UserDevice.objects.count()} UserDevices...")
    UserDevice.objects.all().delete()
    print("ALL DATA DELETED SUCCESSFULLY")
except Exception as e:
    print(f"Error: {e}")
