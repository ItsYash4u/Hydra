
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def inspect_schema():
    with open('schema_info.txt', 'w') as f:
        with connection.cursor() as cursor:
            f.write("--- UserDevice Table ---\n")
            cursor.execute("DESCRIBE userdevice;")
            for row in cursor.fetchall():
                f.write(str(row) + "\n")
            
            f.write("\n--- Device Table ---\n")
            cursor.execute("DESCRIBE device;")
            for row in cursor.fetchall():
                f.write(str(row) + "\n")

            f.write("\n--- Device Constraints ---\n")
            cursor.execute("SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'device' AND TABLE_SCHEMA = 'greeva';")
            for row in cursor.fetchall():
                # Print Constraint Name, Column, Referenced Table, Referenced Column
                f.write(f"Constraint: {row[2]}, Column: {row[6]}, Ref Table: {row[10]}, Ref Column: {row[11]}\n")

            f.write("\n--- UserDevice Data ---\n")
            cursor.execute("SELECT S_No, User_ID, Email_ID FROM userdevice LIMIT 20;")
            for row in cursor.fetchall():
                f.write(str(row) + "\n")
    print("Written to schema_info.txt")

if __name__ == "__main__":
    inspect_schema()
