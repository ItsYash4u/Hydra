# 🚀 QUICK START GUIDE - Custom Database Implementation

## ⚡ IMMEDIATE ACTIONS REQUIRED

### 1. Stop the Running Server
Press `Ctrl+C` in your terminal to stop the Django server.

### 2. Fresh Database Setup
```bash
# Delete old database
del db.sqlite3

# Delete old migrations (keep __init__.py)
del greeva\hydroponics\migrations\0*.py
del greeva\users\migrations\0*.py
```

### 3. Create New Migrations
```bash
python manage.py makemigrations hydroponics
python manage.py migrate
```

### 4. Seed the Database
```bash
python manage.py shell
```

Then in the Python shell:
```python
exec(open('seed_database.py').read())
```

Or alternatively:
```bash
python seed_database.py
```

### 5. Verify Tables Created
```bash
python manage.py dbshell
```

In SQLite shell:
```sql
.tables
SELECT * FROM UserDevice;
SELECT * FROM Device LIMIT 5;
SELECT * FROM SensorValue LIMIT 5;
.quit
```

### 6. Start Server
```bash
python manage.py runserver
```

## 📋 WHAT WAS CREATED

### Files Created:
1. **`greeva/hydroponics/models_custom.py`** - Three custom tables
2. **`seed_database.py`** - Database seeding script
3. **`CUSTOM_DATABASE_PLAN.md`** - Implementation plan
4. **`QUICK_START.md`** - This file

### Database Tables:
1. **UserDevice** - Custom user table (replaces Django's User)
2. **Device** - Device ownership table
3. **SensorValue** - Sensor readings table

## 🔐 Test Credentials (After Seeding)

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

## ✅ VERIFICATION CHECKLIST

- [ ] Old database deleted
- [ ] Old migrations deleted
- [ ] New migrations created
- [ ] Migrations applied successfully
- [ ] Database seeded
- [ ] Tables verified in dbshell
- [ ] 7 users created (1 admin, 6 users)
- [ ] 49-70 devices created (7-10 per user)
- [ ] 490-1400 sensor readings created
- [ ] Foreign key relationships working

## 🎯 NEXT STEPS (After Database Setup)

1. **Update Authentication System** - Replace Django auth with custom UserDevice auth
2. **Update API Views** - Use UserDevice instead of User model
3. **Update Dashboard Views** - Query from custom tables
4. **Implement OTP System** - For signup only
5. **Implement Session Management** - 1-week cookie validity
6. **Role-Based Access Control** - Admin vs User permissions

## ⚠️ IMPORTANT NOTES

- **Django's User model is BYPASSED** - All auth uses UserDevice
- **Foreign keys are CharField** - Manual relationship management
- **Serial numbers (S_No)** - Explicit AutoField primary keys
- **No Django admin** - Custom admin interface required
- **Custom authentication** - No django.contrib.auth

## 🆘 TROUBLESHOOTING

**If migrations fail:**
```bash
python manage.py makemigrations --empty hydroponics
# Then manually edit the migration file
```

**If seeding fails:**
```bash
python manage.py shell
>>> from greeva.hydroponics.models_custom import *
>>> UserDevice.objects.all().delete()
>>> Device.objects.all().delete()
>>> SensorValue.objects.all().delete()
>>> exec(open('seed_database.py').read())
```

**To check table structure:**
```bash
python manage.py dbshell
.schema UserDevice
.schema Device
.schema SensorValue
```

## 📞 VERIFICATION COMMANDS

```bash
# Count records
python manage.py shell
>>> from greeva.hydroponics.models_custom import *
>>> print(f"Users: {UserDevice.objects.count()}")
>>> print(f"Devices: {Device.objects.count()}")
>>> print(f"Readings: {SensorValue.objects.count()}")
>>> print(f"Admin count: {UserDevice.objects.filter(Role='admin').count()}")
```

---

**Status:** ✅ Custom models created, ready for migration and seeding
**Next:** Execute steps 1-6 above to complete database setup
