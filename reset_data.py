
from greeva.hydroponics.models_custom import SensorValue, Device, UserDevice

print("Starting data deletion...")

# 1. Delete Sensor Values (No cascade support due to managed=False and CharField content)
sv_count = SensorValue.objects.count()
SensorValue.objects.all().delete()
print(f"Deleted {sv_count} SensorValue records.")

# 2. Delete Devices
d_count = Device.objects.count()
Device.objects.all().delete()
print(f"Deleted {d_count} Device records.")

# 3. Delete Users
u_count = UserDevice.objects.count()
UserDevice.objects.all().delete()
print(f"Deleted {u_count} UserDevice records.")

print("All application data has been cleared.")
