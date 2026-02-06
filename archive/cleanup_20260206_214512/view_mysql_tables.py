import pymysql
import os
import sys

# Configure pymysql to act as MySQLdb for Django if needed, 
# but here we just use it directly to inspect.

def show_database_structure():
    print("Connecting to MySQL database 'greeva'...")
    try:
        # Based on your .env settings: output=mysql://root:@localhost:3306/greeva
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='greeva',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\nSuccessfully connected! Found {len(tables)} tables in 'greeva':")
            print("-" * 50)
            
            for table in tables:
                # The key in the dict depends on the column name, usually "Tables_in_greeva"
                # We'll just print the first value
                table_name = list(table.values())[0]
                
                # specific check for our key tables
                count_str = ""
                if table_name in ['users_user', 'hydroponics_device', 'hydroponics_sensorvalue']:
                    cursor.execute(f"SELECT COUNT(*) as c FROM {table_name}")
                    count = cursor.fetchone()['c']
                    count_str = f" ({count} rows)"
                
                print(f"• {table_name}{count_str}")
                
            print("-" * 50)
            print("\nYou can view this data using:")
            print("1. Django Admin (http://127.0.0.1:8000/admin)")
            print("2. MySQL Workbench")
            print("3. VS Code Database Extensions")
            
    except pymysql.err.OperationalError as e:
        print(f"Error connecting: {e}")
        print("Make sure your MySQL server is running!")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    show_database_structure()
