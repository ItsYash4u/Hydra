import pymysql
import sys

def check_for_workbench_db():
    print("Checking if we can see the 'workbench_test_db'...")
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES LIKE 'workbench_test_db'")
            result = cursor.fetchone()
            
            if result:
                print("\n✅ MATCH FOUND!")
                print("Python and Workbench ARE connected to the same server.")
                print("This means 'greeva' is there, just hidden in your UI.")
            else:
                print("\n❌ NO MATCH FOUND.")
                print("Python and Workbench are connected to DIFFERENT servers.")
                print("This explains why you can't see 'greeva'.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_for_workbench_db()
