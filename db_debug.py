import pymysql

def get_deep_info():
    print("--- DJANGO/PYTHON CONNECTION INFO ---")
    try:
        # Connect exactly as .env does
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            # Get key identifiers
            cursor.execute("SELECT @@datadir, @@port, @@version, @@hostname, @@socket")
            data = cursor.fetchone()
            
            print(f"Data Directory: {data[0]}")
            print(f"Port:           {data[1]}")
            print(f"Version:        {data[2]}")
            print(f"Hostname:       {data[3]}")
            print(f"Socket:         {data[4]}")
            
            cursor.execute("SELECT DATABASE()")
            print(f"Current DB:     {cursor.fetchone()[0]}")
            
            cursor.execute("SHOW DATABASES")
            dbs = [d[0] for d in cursor.fetchall()]
            print(f"All DBs:        {', '.join(dbs)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_deep_info()
