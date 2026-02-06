
import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from greeva.hydroponics.models_custom import UserDevice, Device

def inspect():
    with open('users_dump.txt', 'w') as f:
        f.write("Inspecting UserDevice table...\n")
        users = UserDevice.objects.all()
        for u in users:
            f.write(f"User: PK={u.pk}, User_ID='{u.User_ID}', Email='{u.Email_ID}'\n")

        f.write("\nInspecting Device table...\n")
        devices = Device.objects.all()
        for d in devices:
            f.write(f"Device: ID={d.Device_ID}, Owner_ID='{d.user_id}'\n") # d.user_id is the raw FK value
    print("Done writing to users_dump.txt")

if __name__ == "__main__":
    inspect()
