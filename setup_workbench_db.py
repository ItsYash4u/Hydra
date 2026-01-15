import pymysql

def setup_workbench_db():
    print("Attempting to connect to the Workbench MySQL Server...")
    password = 'dpa1xw3mw7'
    
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=password,
            charset='utf8mb4'
        )
        print("✅ Connected successfully using the provided password!")
        
        with conn.cursor() as cursor:
            # Create the database
            cursor.execute("CREATE DATABASE IF NOT EXISTS greeva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'greeva' verified/created on the Workbench server.")
            
            # Check if it's empty
            cursor.execute("USE greeva")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"ℹ️  Current tables in 'greeva' on this server: {len(tables)}")
            
    except pymysql.err.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("Double check the password or if the username is 'root'.")
        return False
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return True

if __name__ == "__main__":
    setup_workbench_db()
