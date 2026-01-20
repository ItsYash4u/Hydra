"""
Direct MySQL Connection to Check and Delete Devices
This bypasses Django entirely and connects directly to MySQL
"""

import mysql.connector
from mysql.connector import Error

# Database connection details from your .env file
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'greeva',
    'user': 'root',
    'password': 'dpa1xw3mw7'
}

def main():
    connection = None
    try:
        print("=" * 70)
        print("DIRECT MYSQL CONNECTION - DEVICE FIX")
        print("=" * 70)
        
        # Connect to MySQL
        print("\n[1] Connecting to MySQL...")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✓ Connected to database: {record[0]}")
            
            # Check current device count
            print("\n[2] Checking current device count...")
            cursor.execute("SELECT COUNT(*) FROM device")
            count = cursor.fetchone()[0]
            print(f"   Current device count: {count}")
            
            if count > 0:
                # Show devices
                print(f"\n[3] Listing all {count} device(s):")
                cursor.execute("SELECT S_No, Device_ID, User_ID FROM device")
                devices = cursor.fetchall()
                for device in devices:
                    print(f"   - S_No: {device[0]}, Device_ID: {device[1]}, User_ID: {device[2]}")
                
                # Delete all devices
                print(f"\n[4] Deleting all {count} device(s)...")
                cursor.execute("DELETE FROM device")
                connection.commit()
                print(f"✓ Deleted {cursor.rowcount} device(s)")
                
                # Verify deletion
                print("\n[5] Verifying deletion...")
                cursor.execute("SELECT COUNT(*) FROM device")
                final_count = cursor.fetchone()[0]
                print(f"   Final device count: {final_count}")
                
                if final_count == 0:
                    print("\n✅ SUCCESS! All devices have been deleted from the database.")
                    print("\n📌 NEXT STEPS:")
                    print("   1. Go to your Django admin page")
                    print("   2. Press Ctrl+F5 to hard refresh (clear cache)")
                    print("   3. The device count should now show 0")
                else:
                    print(f"\n⚠ WARNING: Still showing {final_count} devices!")
            else:
                print("\n✅ Database is already clean - no devices found!")
                print("\n📌 If Django admin still shows devices:")
                print("   1. Press Ctrl+F5 to hard refresh the page")
                print("   2. Clear your browser cache")
                print("   3. Restart the Django server")
            
            cursor.close()
            
    except Error as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPossible issues:")
        print("  - MySQL server is not running")
        print("  - Wrong credentials in .env file")
        print("  - Database 'greeva' doesn't exist")
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n[6] MySQL connection closed")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
