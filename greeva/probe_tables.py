
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def probe():
    with connection.cursor() as cursor:
        print("--- TABLES ---")
        cursor.execute("SHOW TABLES")
        tables = [r[0] for r in cursor.fetchall()]
        print(tables)
        
        if 'userdevice' in tables:
            try:
                cursor.execute("SELECT count(*) FROM userdevice")
                print(f"userdevice count: {cursor.fetchone()[0]}")
            except Exception as e:
                print(f"userdevice error: {e}")
        else:
            print("userdevice: MISSING")

        if 'user_device' in tables:
            try:
                cursor.execute("SELECT count(*) FROM user_device")
                print(f"user_device count: {cursor.fetchone()[0]}")
            except Exception as e:
                print(f"user_device error: {e}")
        else:
            print("user_device: MISSING")

if __name__ == "__main__":
    probe()
