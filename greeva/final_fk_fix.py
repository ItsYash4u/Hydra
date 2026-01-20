
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def final_fix():
    with connection.cursor() as cursor:
        print("=== STEP 1: Check current constraints ===")
        cursor.execute("""
            SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'device' 
            AND TABLE_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        constraints = cursor.fetchall()
        print(f"Current constraints: {constraints}")
        
        print("\n=== STEP 2: Drop existing FK constraint ===")
        try:
            cursor.execute("ALTER TABLE device DROP FOREIGN KEY fk_device_user")
            print("✓ Dropped fk_device_user")
        except Exception as e:
            print(f"✗ Failed to drop: {e}")
            
        print("\n=== STEP 3: Add correct FK constraint ===")
        try:
            cursor.execute("""
                ALTER TABLE device 
                ADD CONSTRAINT fk_device_user 
                FOREIGN KEY (User_ID) 
                REFERENCES userdevice (User_ID) 
                ON DELETE CASCADE
            """)
            print("✓ Added fk_device_user pointing to userdevice")
        except Exception as e:
            print(f"✗ Failed to add: {e}")
            
        print("\n=== STEP 4: Verify new constraints ===")
        cursor.execute("""
            SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'device' 
            AND TABLE_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        new_constraints = cursor.fetchall()
        print(f"New constraints: {new_constraints}")
        
        print("\n=== COMPLETE ===")

if __name__ == "__main__":
    final_fix()
