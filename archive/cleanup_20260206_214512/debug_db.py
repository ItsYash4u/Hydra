
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

from greeva.hydroponics.models_custom import UserDevice, Device
from django.db import connection

def check_db():
    print("Checking Database state...")
    
    # 1. Check Table Names
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
    
    # 2. Check UserDevice Data
    users = UserDevice.objects.all()
    print(f"\nFound {users.count()} users in UserDevice table:")
    for u in users:
        print(f" - PK: {u.pk}, User_ID: '{u.User_ID}', Email: {u.Email_ID}")

    # 3. Check Device Data
    devices = Device.objects.all()
    print(f"\nFound {devices.count()} devices in Device table:")
    for d in devices:
        # handle potential attribute error if user isn't resolved
        try:
            user_val = d.user
            user_id_val = d.user_id # Accessing the underlying FK value
        except Exception as e:
            user_val = f"ERROR: {e}"
            user_id_val = "Unknown"
            
        print(f" - Device_ID: {d.Device_ID}, User: {user_val} (Raw Value: {user_id_val})")

if __name__ == "__main__":
    check_db()
