import pymysql
import sys

def create_database():
    print("Attempting to connect to MySQL...")
    # Try connecting with root and empty password first (common local dev default)
    configs = [
        {"host": "localhost", "user": "root", "password": ""},
        {"host": "localhost", "user": "root", "password": "root"},
        {"host": "localhost", "user": "root", "password": "password"},
        {"host": "127.0.0.1", "user": "root", "password": ""},
    ]

    conn = None
    for config in configs:
        try:
            print(f"Trying user='{config['user']}' password='{ '*' * len(config['password']) }'...")
            conn = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected successfully!")
            break
        except pymysql.err.OperationalError as e:
            print(f"Connection failed: {e}")
            continue
    
    if not conn:
        print("Could not connect to MySQL with common default credentials.")
        return False

    try:
        with conn.cursor() as cursor:
            # Check if database exists
            cursor.execute("SHOW DATABASES LIKE 'greeva'")
            result = cursor.fetchone()
            if result:
                print("Database 'greeva' already exists.")
            else:
                print("Creating database 'greeva'...")
                cursor.execute("CREATE DATABASE greeva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print("Database created successfully.")
            
            # Grant privileges if we can (though if we are root we usually don't need to grant to ourselves, 
            # but creating a dedicated user is good practice - sticking to root for now for simplicity of migration unless requested)
    finally:
        conn.close()
    return True

if __name__ == "__main__":
    if create_database():
        print("Database setup complete.")
    else:
        sys.exit(1)
