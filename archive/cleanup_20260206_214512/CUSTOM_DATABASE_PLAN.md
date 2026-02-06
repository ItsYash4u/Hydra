# CUSTOM DATABASE IMPLEMENTATION PLAN

## ✅ COMPLETED STEPS

### 1. Custom Models Created
- **File**: `greeva/hydroponics/models_custom.py`
- **Tables Defined**:
  1. **UserDevice** - Custom user table with S_No, User_ID, Email_ID, Password, Phone, Age, Role
  2. **Device** - Device table with S_No, User_ID (FK), Device_ID, Latitude, Longitude
  3. **SensorValue** - Sensor readings with S_No, Device_ID (FK), sensor fields, Reading_Date, Reading_Time

### 2. Models Integration
- **File**: `greeva/hydroponics/models.py` - Updated to import custom models

## 🔄 NEXT STEPS (MANUAL EXECUTION REQUIRED)

### Step 1: Stop Running Server
```bash
# Press Ctrl+C in the terminal running the server
```

### Step 2: Delete Existing Database (Fresh Start)
```bash
# Delete the SQLite database file
del db.sqlite3

# Delete all migration files except __init__.py
del greeva\hydroponics\migrations\0*.py
del greeva\users\migrations\0*.py
```

### Step 3: Create New Migrations
```bash
python manage.py makemigrations hydroponics
python manage.py makemigrations users
python manage.py migrate
```

### Step 4: Verify Tables Created
```bash
python manage.py dbshell
```

Then in SQLite:
```sql
.tables
.schema UserDevice
.schema Device
.schema SensorValue
```

### Step 5: Seed Database with Test Data
```bash
python manage.py shell
```

Then run the seeding script (see SEED_DATABASE.py)

## 📋 DATABASE SCHEMA

### UserDevice Table
```
S_No (PK, AutoIncrement)
User_ID (Unique, VARCHAR)
Email_ID (Unique, Email)
Password (Hashed, VARCHAR)
Phone (VARCHAR, Optional)
Age (Integer, Optional)
Role (admin/user, Default: user)
Created_At (DateTime)
Updated_At (DateTime)
```

### Device Table
```
S_No (PK, AutoIncrement)
User_ID (FK → UserDevice.User_ID)
Device_ID (Unique, VARCHAR)
Latitude (Decimal)
Longitude (Decimal)
Created_At (DateTime)
Updated_At (DateTime)
```

### SensorValue Table
```
S_No (PK, AutoIncrement)
Device_ID (FK → Device.Device_ID)
Temperature (Decimal)
pH (Decimal)
EC (Decimal)
Humidity (Decimal)
Nitrogen (Decimal)
Phosphorus (Decimal)
Potassium (Decimal)
Light_Hours (Decimal)
Moisture (Decimal)
Reading_Date (Date)
Reading_Time (Time)
Created_At (DateTime)
```

## 🎯 AUTHENTICATION REQUIREMENTS

1. **Signup**: Requires OTP verification
2. **Login**: Email + Password (no OTP)
3. **Session**: 1 week validity via secure cookies
4. **Role-Based Access**:
   - Admin: Full backend access
   - User: Limited to user-level APIs
5. **Admin Promotion**: Only existing admin can promote users

## 📊 SEEDING REQUIREMENTS

- **Users**: 5-7 users (1 admin, rest normal users)
- **Devices**: 7-10 devices per user
- **Sensor Data**: Multiple readings per device

## ⚠️ IMPORTANT NOTES

1. **Django's User Model**: Completely bypassed - using UserDevice instead
2. **Foreign Keys**: Implemented as CharField references (not Django ForeignKey) for explicit control
3. **Serial Numbers**: Explicit S_No fields as AutoField primary keys
4. **Authentication**: Custom implementation required (no Django auth)
