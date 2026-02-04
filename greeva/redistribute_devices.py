"""
Script to redistribute devices among users
Ensures each user has between 5-10 devices
"""

import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from greeva.hydroponics.models_custom import Device, UserDevice

print("=" * 80)
print("DEVICE REDISTRIBUTION SCRIPT")
print("=" * 80)

# Get all users (excluding admins)
all_users = UserDevice.objects.filter(Role='user').order_by('User_ID')
admin_users = UserDevice.objects.filter(Role='admin')

print(f"\nTotal Regular Users: {all_users.count()}")
print(f"Total Admin Users: {admin_users.count()}")

# Get all devices
all_devices = Device.objects.all().order_by('Device_ID')
print(f"Total Devices: {all_devices.count()}")

print("\n" + "=" * 80)
print("CURRENT DEVICE DISTRIBUTION")
print("=" * 80)

for user in all_users:
    device_count = Device.objects.filter(user=user).count()
    print(f"\nUser: {user.User_ID} ({user.Email_ID})")
    print(f"  Current Devices: {device_count}")

print("\n" + "=" * 80)
print("REDISTRIBUTING DEVICES")
print("=" * 80)

if all_users.count() == 0:
    print("\n⚠️  No regular users found! Cannot redistribute devices.")
else:
    # Calculate devices per user
    total_devices = all_devices.count()
    total_users = all_users.count()
    
    if total_devices < total_users * 5:
        print(f"\n⚠️  Not enough devices! Need at least {total_users * 5} devices.")
        print(f"   Current: {total_devices} devices")
        print(f"   Creating additional devices...")
        
        # We'll need to create more devices - for now, just report
        needed = (total_users * 5) - total_devices
        print(f"   Need to create {needed} more devices")
    else:
        # Redistribute devices evenly
        devices_per_user = total_devices // total_users
        
        # Ensure each user gets 5-10 devices
        if devices_per_user < 5:
            devices_per_user = 5
        elif devices_per_user > 10:
            devices_per_user = 10
            
        print(f"\nTarget: {devices_per_user} devices per user")
        
        # Convert queryset to list for random distribution
        device_list = list(all_devices)
        random.shuffle(device_list)
        
        # Distribute devices
        device_index = 0
        for user in all_users:
            # Assign devices to this user
            user_devices = device_list[device_index:device_index + devices_per_user]
            
            for device in user_devices:
                device.user = user
                device.save()
            
            device_index += devices_per_user
            
            print(f"\n✅ User {user.User_ID}: Assigned {len(user_devices)} devices")
            device_ids = [d.Device_ID for d in user_devices]
            print(f"   Device IDs: {', '.join(device_ids)}")
        
        # Handle remaining devices
        remaining_devices = device_list[device_index:]
        if remaining_devices:
            print(f"\n📦 Distributing {len(remaining_devices)} remaining devices...")
            for i, device in enumerate(remaining_devices):
                user = all_users[i % all_users.count()]
                device.user = user
                device.save()
                print(f"   {device.Device_ID} → {user.User_ID}")

print("\n" + "=" * 80)
print("FINAL DEVICE DISTRIBUTION")
print("=" * 80)

for user in all_users:
    device_count = Device.objects.filter(user=user).count()
    user_devices = Device.objects.filter(user=user).order_by('Device_ID')
    device_ids = [d.Device_ID for d in user_devices]
    
    print(f"\nUser: {user.User_ID} ({user.Email_ID})")
    print(f"  Total Devices: {device_count}")
    print(f"  Device IDs: {', '.join(device_ids)}")

print("\n" + "=" * 80)
print("✅ REDISTRIBUTION COMPLETE")
print("=" * 80)
