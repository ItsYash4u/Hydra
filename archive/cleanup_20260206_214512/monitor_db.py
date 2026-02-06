import pymysql
import time

def monitor_tables():
    print("Monitoring table creation...")
    pw = 'dpa1xw3mw7'
    for i in range(10):
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password=pw, database='greeva')
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"Attempt {i+1}: Found {len(tables)} tables")
                if len(tables) > 10:
                    print("Creation seems complete (or mostly complete)!")
                    return
            conn.close()
        except:
            print(f"Attempt {i+1}: creating or error connecting...")
        time.sleep(2)

if __name__ == "__main__":
    monitor_tables()
