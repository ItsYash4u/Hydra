
import sys
try:
    from greeva.hydroponics.models_custom import SensorValue, Device, UserDevice
    print("Deleting SensorValues...")
    SensorValue.objects.all().delete()
    print("Deleting Devices...")
    Device.objects.all().delete()
    print("Deleting UserDevices...")
    UserDevice.objects.all().delete()
    print("DATABASE_WIPED_CLEAN")
except Exception as e:
    print(f"Error: {e}")
