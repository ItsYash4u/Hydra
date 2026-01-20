
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def test_raw_insert():
    # 1. Create a dummy user physically
    uid = "TEST-USER-RAW-001"
    email = "rawtest@example.com"
    
    with connection.cursor() as cursor:
        try:
            print(f"Inserting User {uid}...")
            cursor.execute(
                "INSERT INTO userdevice (User_ID, Email_ID, Password, Role, Created_At, Updated_At) VALUES (%s, %s, 'pass', 'user', NOW(), NOW())",
                [uid, email]
            )
            print("User Inserted.")
        except Exception as e:
            print(f"User Insert failed (maybe exists): {e}")

        # 2. Try inserting device referencing it
        did = "TEST-DEV-RAW-001"
        try:
            print(f"Inserting Device {did} executing raw SQL...")
            cursor.execute(
                "INSERT INTO device (User_ID, Device_ID, Created_At, Updated_At) VALUES (%s, %s, NOW(), NOW())",
                [uid, did]
            )
            print("Device Inserted Successfully via Raw SQL!")
        except Exception as e:
            print(f"Raw Device Insert failed: {e}")
            
if __name__ == "__main__":
    test_raw_insert()
