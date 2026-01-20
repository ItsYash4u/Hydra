
import os
import django
import sys
from django.db import connection

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def list_tables():
    print("Listing all tables in the database:")
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")

if __name__ == "__main__":
    list_tables()
