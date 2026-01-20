
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

def inspect_db():
    output = []
    with connection.cursor() as cursor:
        output.append("--- DEVICE TABLE ---")
        try:
            cursor.execute("SHOW CREATE TABLE Device")
            row = cursor.fetchone()
            output.append(row[1])
        except Exception as e:
            output.append(str(e))

        output.append("\n--- SENSORREADING TABLE ---")
        try:
            cursor.execute("SHOW CREATE TABLE sensor_reading")
            row = cursor.fetchone()
            output.append(row[1])
        except Exception as e:
            output.append(str(e))
            
    with open("schema_dump.txt", "w") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    inspect_db()
