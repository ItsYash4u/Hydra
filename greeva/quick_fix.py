import mysql.connector
conn = mysql.connector.connect(host='localhost', port=3306, database='greeva', user='root', password='dpa1xw3mw7')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM device")
print(f"Devices: {c.fetchone()[0]}")
c.execute("SELECT COUNT(*) FROM userdevice")
print(f"Users: {c.fetchone()[0]}")
if c.execute("SELECT COUNT(*) FROM userdevice") or True:
    c.execute("SELECT User_ID FROM userdevice LIMIT 1")
    r = c.fetchone()
    if r:
        uid = r[0]
        print(f"Using user: {uid}")
        c.execute("INSERT INTO device (User_ID, Device_ID, Created_At, Updated_At) VALUES (%s, 'DEV_TEST_001', NOW(), NOW())", (uid,))
        conn.commit()
        print("✓ Device created!")
    else:
        print("Creating user...")
        c.execute("INSERT INTO userdevice (User_ID, Email_ID, Password, Role, Created_At, Updated_At) VALUES ('testuser', 'test@test.com', 'pass', 'user', NOW(), NOW())")
        conn.commit()
        c.execute("INSERT INTO device (User_ID, Device_ID, Created_At, Updated_At) VALUES ('testuser', 'DEV_TEST_001', NOW(), NOW())")
        conn.commit()
        print("✓ User and device created!")
conn.close()
