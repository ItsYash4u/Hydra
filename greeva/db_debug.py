
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def debug_schema():
    with connection.cursor() as cursor:
        print("\n=== TABLES ===")
        cursor.execute("SHOW TABLES")
        for row in cursor.fetchall():
            print(row[0])
            
        print("\n=== CREATE TABLE device ===")
        try:
            cursor.execute("SHOW CREATE TABLE device")
            print(cursor.fetchone()[1])
        except Exception as e:
            print(f"Error: {e}")

        print("\n=== CREATE TABLE userdevice ===")
        try:
            cursor.execute("SHOW CREATE TABLE userdevice")
            print(cursor.fetchone()[1])
        except Exception as e:
            print(f"Error: {e}")
            # Try alternate name
            try:
                cursor.execute("SHOW CREATE TABLE UserDevice")
                print(cursor.fetchone()[1])
            except:
                pass

if __name__ == "__main__":
    debug_schema()
