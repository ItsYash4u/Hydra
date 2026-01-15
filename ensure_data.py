import pymysql
import sys
import os
import django
from django.core.management import call_command

def check_and_fill_db():
    print("Checking database content...")
    db_password = 'dpa1xw3mw7'
    
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=db_password,
            database='greeva',
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Current table count: {len(tables)}")
            
            if len(tables) == 0:
                print("Database is empty. Running migrations now...")
                conn.close() # Close raw connection before Django starts
                
                # Setup Django
                os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
                django.setup()
                
                print("Starting Migration...")
                try:
                    call_command('migrate', interactive=False)
                    print("✅ Migration Complete.")
                    
                    print("Loading Data...")
                    call_command('loaddata', 'datadump.json')
                    print("✅ Data Loaded.")
                except Exception as e:
                    print(f"❌ Django Command Failed: {e}")
            else:
                print("✅ Database already has tables!")
                for t in tables[:5]:
                    print(f" - {t[0]}")
                if len(tables) > 5: print(" ... and more")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_and_fill_db()
