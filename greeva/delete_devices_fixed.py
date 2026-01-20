"""
Simple Django ORM Device Deletion Script
Now that models are fixed with app_label
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from hydroponics.models_custom import Device

print("=" * 60)
print("DEVICE DELETION VIA DJANGO ORM")
print("=" * 60)

# Check count
count = Device.objects.count()
print(f"\n[1] Current device count: {count}")

if count > 0:
    # Show devices
    print(f"\n[2] Listing devices:")
    for device in Device.objects.all():
        print(f"    - {device.Device_ID} (User: {device.user_id})")
    
    # Delete
    print(f"\n[3] Deleting all {count} device(s)...")
    deleted, _ = Device.objects.all().delete()
    print(f"    ✓ Deleted {deleted} device(s)")
    
    # Verify
    final = Device.objects.count()
    print(f"\n[4] Final count: {final}")
    
    if final == 0:
        print("\n✅ SUCCESS! All devices deleted.")
        print("\n📌 Next: Refresh Django admin (Ctrl+F5)")
    else:
        print(f"\n⚠ Still showing {final} devices")
else:
    print("\n✅ No devices found!")
    print("\n📌 If admin still shows devices:")
    print("   - Hard refresh: Ctrl+F5")
    print("   - Restart Django server")

print("\n" + "=" * 60)
