
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def fix_fk_final():
    with connection.cursor() as cursor:
        print("Starting FK Repair...")
        
        # 1. Verify 'userdevice' table exists (Django model target)
        cursor.execute("SHOW TABLES LIKE 'userdevice'")
        if not cursor.fetchone():
            print("ERROR: Table 'userdevice' does not exist. Cannot link FK.")
            return

        # 2. Drop the problematic foreign key (pointing to 'user_device')
        fk_name = 'fk_device_user'
        try:
            print(f"Attempting to drop {fk_name}...")
            cursor.execute(f"ALTER TABLE device DROP FOREIGN KEY {fk_name}")
            print(f"SUCCESS: Dropped {fk_name}")
        except Exception as e:
            print(f"INFO: Could not drop {fk_name} (might not exist): {e}")

        # 3. Add the CORRECT foreign key (pointing to 'userdevice')
        new_fk_name = 'fk_device_user_fixed'
        # Drop it first if it exists to be safe
        try:
             cursor.execute(f"ALTER TABLE device DROP FOREIGN KEY {new_fk_name}")
        except:
             pass

        print(f"Adding {new_fk_name} referencing 'userdevice'...")
        try:
            cursor.execute(f"""
                ALTER TABLE device 
                ADD CONSTRAINT {new_fk_name} 
                FOREIGN KEY (User_ID) REFERENCES userdevice (User_ID) 
                ON DELETE CASCADE
            """)
            print(f"SUCCESS: Foreign Key Fixed! Device now links to 'userdevice'.")
        except Exception as e:
            print(f"CRITICAL ERROR adding FK: {e}")

if __name__ == "__main__":
    fix_fk_final()
