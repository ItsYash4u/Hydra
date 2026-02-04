
from greeva.hydroponics.models_custom import UserDevice, Device

# Clean up
Device.objects.all().delete()
UserDevice.objects.all().delete()

# Create Users
u1 = UserDevice.objects.create(User_ID="U1", Email_ID="yash.singh@test.com", Role='user')
u2 = UserDevice.objects.create(User_ID="U2", Email_ID="rohit.verma@test.com", Role='user')
u3 = UserDevice.objects.create(User_ID="U3", Email_ID="yash.singh.dup@test.com", Role='user') # Same initials

# Create Devices for U1
d1 = Device.objects.create(user=u1)
d2 = Device.objects.create(user=u1)

# Create Devices for U2
d3 = Device.objects.create(user=u2)
d4 = Device.objects.create(user=u2)

# Create Device for U3 (Should collide with U1 if global unique was enforced)
d5 = Device.objects.create(user=u3)

print("="*40)
print(f"User 1 (Yash Singh): {d1.Device_ID}, {d2.Device_ID}")
print(f"User 2 (Rohit Verma): {d3.Device_ID}, {d4.Device_ID}")
print(f"User 3 (Yash Dup):   {d5.Device_ID}")
print("="*40)

if d1.Device_ID == 'ys01' and d2.Device_ID == 'ys02':
    print("✅ User 1 ID Generation: PASS")
else:
    print(f"❌ User 1 ID Generation: FAIL ({d1.Device_ID}, {d2.Device_ID})")

if d3.Device_ID == 'rv01' and d4.Device_ID == 'rv02':
    print("✅ User 2 ID Generation: PASS")
else:
    print(f"❌ User 2 ID Generation: FAIL ({d3.Device_ID}, {d4.Device_ID})")

if d5.Device_ID == 'ys01':
    print("✅ User 3 ID Generation (Duplicate Safe): PASS")
    print("✅ Non-Unique Global ID Verified")
else:
    print(f"❌ User 3 ID Generation: FAIL ({d5.Device_ID}) - Expected ys01")
