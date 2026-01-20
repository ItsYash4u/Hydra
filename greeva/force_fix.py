
import os
import django
from django.db import connection
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def force_fix():
    with connection.cursor() as cursor:
        print("--- DIAGNOSTIC START ---")
        cursor.execute("SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'device' AND TABLE_SCHEMA = DATABASE()")
        rows = cursor.fetchall()
        print(f"Current Constraints on 'device': {rows}")

        # Drop loop
        did_drop = False
        try:
            print("Attempting DROP FOREIGN KEY fk_device_user...")
            cursor.execute("ALTER TABLE device DROP FOREIGN KEY fk_device_user")
            print("DROP SUCCESS.")
            did_drop = True
        except Exception as e:
            print(f"DROP FAILED: {e}")

        # Add loop
        try:
            print("Attempting ADD CONSTRAINT fk_device_user -> userdevice...")
            cursor.execute("ALTER TABLE device ADD CONSTRAINT fk_device_user FOREIGN KEY (User_ID) REFERENCES userdevice (User_ID) ON DELETE CASCADE")
            print("ADD SUCCESS.")
        except Exception as e:
            print(f"ADD FAILED: {e}")
            
        print("--- DIAGNOSTIC END ---")

if __name__ == "__main__":
    force_fix()
