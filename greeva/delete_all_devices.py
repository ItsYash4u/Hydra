
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models import Device

# Get current count
current_count = Device.objects.count()
print(f"Current device count: {current_count}")

if current_count > 0:
    print("\nDevices in database:")
    for device in Device.objects.all():
        print(f"  - {device.Device_ID} (Owner: {device.user_id})")
    
    # Delete all devices
    print(f"\nDeleting all {current_count} devices...")
    deleted_count, _ = Device.objects.all().delete()
    print(f"✓ Deleted {deleted_count} devices")
    
    # Verify
    final_count = Device.objects.count()
    print(f"\nFinal device count: {final_count}")
else:
    print("No devices found in database")
