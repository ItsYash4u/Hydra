import pymysql
import sys

def get_server_info():
    print("Checking the MySQL server where 'greeva' was created...")
    try:
        # Connecting exactly as we did for the migration
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            # Get version and port info if possible (though port is known from connect)
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            
            cursor.execute("SELECT @@port")
            port = cursor.fetchone()
            
            cursor.execute("SELECT CURRENT_USER()")
            user = cursor.fetchone()
            
            cursor.execute("SHOW DATABASES LIKE 'greeva'")
            db_exists = cursor.fetchone()
            
            print("\n---------- CONNECTION DETAILS ----------")
            print(f"Status:      SUCCESSFUL CONNECTION")
            print(f"Server Host: 127.0.0.1 (Localhost)")
            print(f"Server Port: {port[0]}")
            print(f"User:        {user[0]}")
            print(f"Version:     {version[0]}")
            print(f"DB 'greeva': {'EXISTS ✅' if db_exists else 'NOT FOUND ❌'}")
            print("----------------------------------------")
            
            if db_exists:
                print("\nNOTE: The database definitely exists on THIS server.")
                print("If you don't see it in Workbench, you might be connected to a DIFFERENT MySQL server.")
            
    except pymysql.err.OperationalError as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    get_server_info()
