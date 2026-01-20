"""
Direct MySQL fix - Create test device
"""
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'greeva',
    'user': 'root',
    'password': 'dpa1xw3mw7'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("CREATING TEST DEVICE DIRECTLY IN DATABASE")
    print("=" * 70)
    
    # Check if user exists
    cursor.execute("SELECT COUNT(*) FROM userdevice")
    user_count = cursor.fetchone()[0]
    print(f"\n[1] Users in database: {user_count}")
    
    if user_count == 0:
        print("   Creating test user...")
        cursor.execute("""
            INSERT INTO userdevice (User_ID, Email_ID, Password, Phone, Age, Role, Created_At, Updated_At)
            VALUES ('test_user', 'test@example.com', 'pbkdf2_sha256$600000$test$hash', '1234567890', 25, 'user', NOW(), NOW())
        """)
        conn.commit()
        print("   ✓ Created user: test_user")
        user_id = 'test_user'
    else:
        cursor.execute("SELECT User_ID FROM userdevice LIMIT 1")
        user_id = cursor.fetchone()[0]
        print(f"   ✓ Using existing user: {user_id}")
    
    # Check devices
    cursor.execute("SELECT COUNT(*) FROM device")
    device_count = cursor.fetchone()[0]
    print(f"\n[2] Devices in database: {device_count}")
    
    if device_count == 0:
        print("   Creating test device...")
        cursor.execute("""
            INSERT INTO device (User_ID, Device_ID, Latitude, Longitude, Created_At, Updated_At)
            VALUES (%s, 'DEVICE_TEST_001', 28.6139, 77.2090, NOW(), NOW())
        """, (user_id,))
        conn.commit()
        print("   ✓ Created device: DEVICE_TEST_001")
    else:
        cursor.execute("SELECT Device_ID FROM device")
        devices = cursor.fetchall()
        print("   ✓ Existing devices:")
        for dev in devices:
            print(f"      - {dev[0]}")
    
    # Final check
    cursor.execute("SELECT COUNT(*) FROM device")
    final_count = cursor.fetchone()[0]
    
    print(f"\n[3] Final device count: {final_count}")
    print("\n✅ SUCCESS! You can now add sensor values!")
    print("   Go to: http://127.0.0.1:8000/admin/hydroponics/sensorvalue/add/")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    
print("\n" + "=" * 70)
