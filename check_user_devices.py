
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

from greeva.hydroponics.models_custom import UserDevice, Device

try:
    user = UserDevice.objects.get(Email_ID='user1@greeva.com')
    print(f"User Found: {user.Email_ID} (Role: {user.Role})")
    
    devices = Device.objects.filter(user=user)
    print(f"Total Devices: {devices.count()}")
    
    for d in devices:
        print(f" - Device: {d.Device_ID}, Lat: {d.Latitude}, Lon: {d.Longitude}")
        
except UserDevice.DoesNotExist:
    print("User user1@greeva.com NOT FOUND")
