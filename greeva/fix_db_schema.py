
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def fix_and_verify():
    with connection.cursor() as cursor:
        # 1. Check Tables
        print("Checking tables...")
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables found: {tables}")
        
        user_table = None
        if 'userdevice' in tables:
            user_table = 'userdevice'
        elif 'user_device' in tables:
            user_table = 'user_device'
            
        print(f"Target User Table: {user_table}")
        
        if not user_table:
            print("CRITICAL: User table not found!")
            return

        # 2. Drop Bad Constraints on Device
        print("Inspecting device table constraints...")
        cursor.execute("SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'device' AND REFERENCED_TABLE_NAME IS NOT NULL AND TABLE_SCHEMA = DATABASE()")
        constraints = cursor.fetchall()
        for c in constraints:
            print(f"Constraint: {c[0]} -> Refs: {c[3]}")
            if c[3] != user_table:
                print(f"DROPPING BAD CONSTRAINT: {c[0]}")
                try:
                    cursor.execute(f"ALTER TABLE device DROP FOREIGN KEY {c[0]}")
                    print("Dropped.")
                except Exception as e:
                    print(f"Error dropping: {e}")

        # 3. Add Correct Constraint (if missing)
        # We try to add it. If it exists, it might fail, which is fine, but we just cleared bad ones.
        print(f"Ensuring FK points to {user_table}...")
        try:
             # Check if we already have a constraint pointing to the right table
             valid_exists = False
             cursor.execute("SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'device' AND REFERENCED_TABLE_NAME = %s AND TABLE_SCHEMA = DATABASE()", [user_table])
             if cursor.fetchone():
                 valid_exists = True
                 print("Valid constraint already exists.")
             
             if not valid_exists:
                 cursor.execute(f"""
                    ALTER TABLE device 
                    ADD CONSTRAINT fk_device_user_fixed 
                    FOREIGN KEY (User_ID) REFERENCES {user_table} (User_ID) 
                    ON DELETE CASCADE
                 """)
                 print("Created new correct FK.")
        except Exception as e:
            print(f"Error adding FK: {e}")

if __name__ == "__main__":
    fix_and_verify()
