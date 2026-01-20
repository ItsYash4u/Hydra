
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

from django.db import connection

def execute_sql_fix():
    """Execute raw SQL to fix the FK constraint"""
    print("=" * 60)
    print("FOREIGN KEY CONSTRAINT FIX")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Step 1: Show current constraints
        print("\n[STEP 1] Checking current constraints on 'device' table...")
        cursor.execute("""
            SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'device'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        constraints = cursor.fetchall()
        print(f"Found {len(constraints)} constraint(s):")
        for c in constraints:
            print(f"  - {c[0]} -> {c[1]}.{c[2]}")
        
        # Step 2: Drop the problematic constraint
        print("\n[STEP 2] Dropping fk_device_user constraint...")
        try:
            cursor.execute("ALTER TABLE device DROP FOREIGN KEY fk_device_user")
            print("  ✓ Successfully dropped fk_device_user")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            if "check that column/key exists" in str(e).lower():
                print("  → Constraint might not exist, continuing...")
            else:
                print("  → This might be a critical error!")
        
        # Step 3: Add the correct constraint
        print("\n[STEP 3] Adding correct fk_device_user constraint...")
        try:
            cursor.execute("""
                ALTER TABLE device 
                ADD CONSTRAINT fk_device_user 
                FOREIGN KEY (User_ID) 
                REFERENCES userdevice (User_ID) 
                ON DELETE CASCADE
            """)
            print("  ✓ Successfully added fk_device_user -> userdevice.User_ID")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
        
        # Step 4: Verify the fix
        print("\n[STEP 4] Verifying new constraints...")
        cursor.execute("""
            SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'device'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        new_constraints = cursor.fetchall()
        print(f"Found {len(new_constraints)} constraint(s):")
        for c in new_constraints:
            print(f"  - {c[0]} -> {c[1]}.{c[2]}")
            if c[1] == 'userdevice':
                print("  ✓ CORRECT: Points to 'userdevice' table")
            else:
                print(f"  ✗ WRONG: Still points to '{c[1]}' table")
        
        print("\n" + "=" * 60)
        print("FIX COMPLETE!")
        print("=" * 60)
        return True

if __name__ == "__main__":
    try:
        success = execute_sql_fix()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n!!! CRITICAL ERROR !!!")
        print(f"{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
