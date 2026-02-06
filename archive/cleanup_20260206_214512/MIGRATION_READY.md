# ✅ FIXES APPLIED - READY FOR MIGRATION

## 🔧 What I Fixed:

1. **admin.py** - Updated to use `UserDevice`, `Device`, `SensorValue`
2. **serializers.py** - Updated all DTOs for custom models
3. **views.py** - Simplified to allow migrations (will implement fully after DB setup)

## 🚀 NEXT STEPS - Execute These Commands:

### Step 1: Delete Old Migration Files
```bash
del greeva\hydroponics\migrations\0*.py
del greeva\users\migrations\0*.py
```

### Step 2: Create Fresh Migrations
```bash
python manage.py makemigrations hydroponics
python manage.py makemigrations users
```

### Step 3: Apply Migrations
```bash
python manage.py migrate
```

### Step 4: Verify Tables Created
```bash
python manage.py dbshell
```

In SQLite shell:
```sql
.tables
-- You should see: UserDevice, Device, SensorValue

.schema UserDevice
.schema Device  
.schema SensorValue

.quit
```

### Step 5: Seed the Database
```bash
python manage.py shell
```

In Python shell:
```python
exec(open('seed_database.py').read())
```

### Step 6: Verify Data
Still in Python shell:
```python
from greeva.hydroponics.models import UserDevice, Device, SensorValue

print(f"Users: {UserDevice.objects.count()}")
print(f"Devices: {Device.objects.count()}")
print(f"Readings: {SensorValue.objects.count()}")

# Check admin exists
admin = UserDevice.objects.filter(Role='admin').first()
print(f"Admin: {admin.Email_ID if admin else 'NOT FOUND'}")

# Check relationships
user = UserDevice.objects.first()
user_devices = Device.objects.filter(User_ID=user.User_ID)
print(f"{user.User_ID} has {user_devices.count()} devices")

device = Device.objects.first()
device_readings = SensorValue.objects.filter(Device_ID=device.Device_ID)
print(f"{device.Device_ID} has {device_readings.count()} readings")

exit()
```

### Step 7: Start Server
```bash
python manage.py runserver
```

## 📊 Expected Results:

After seeding, you should have:
- **7 users** (1 admin + 6 normal users)
- **49-70 devices** (7-10 per user)
- **490-1400 sensor readings** (10-20 per device)

## 🔐 Test Login Credentials:

**Admin:**
- Email: admin@hydroponics.com
- Password: admin123

**Users:**
- alice@example.com / alice123
- bob@example.com / bob123
- charlie@example.com / charlie123
- diana@example.com / diana123
- eve@example.com / eve123
- frank@example.com / frank123

## ⚠️ Important Notes:

1. **All old models removed** - Using custom UserDevice, Device, SensorValue
2. **Django auth bypassed** - Custom authentication required
3. **Serial numbers (S_No)** - Explicit AutoField primary keys
4. **Foreign keys** - CharField references (manual relationships)
5. **Views simplified** - Will need full implementation after DB setup

## 🆘 If You Get Errors:

**"No module named X":**
- Make sure you're in the virtual environment: `.venv312\Scripts\activate`

**"Table already exists":**
- Delete db.sqlite3 and try again

**"Cannot import SensorData":**
- Make sure all files are saved and server is restarted

**Migration conflicts:**
- Delete all migration files except `__init__.py` in migrations folders

---

**Status:** ✅ All import errors fixed, ready for migration
**Next:** Execute Step 1-7 above to complete database setup
