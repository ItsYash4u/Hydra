# 🔧 TROUBLESHOOTING GUIDE - Custom Database Migration

## ✅ FIXES APPLIED

1. **admin.py** - Updated ✅
2. **serializers.py** - Updated ✅  
3. **views.py** - Simplified ✅
4. **urls.py** - Fixed (removed search_view) ✅

## 🚀 TRY THESE COMMANDS NOW

### Option 1: Skip System Checks (Fastest)
```bash
python manage.py makemigrations hydroponics --skip-checks
python manage.py makemigrations users --skip-checks
python manage.py migrate --skip-checks
```

### Option 2: Create Empty Migration Manually
```bash
python manage.py makemigrations --empty hydroponics
```

Then edit the generated migration file and add:

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='UserDevice',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False, verbose_name='Serial Number')),
                ('User_ID', models.CharField(max_length=50, unique=True, verbose_name='User ID')),
                ('Email_ID', models.EmailField(max_length=254, unique=True, verbose_name='Email ID')),
                ('Password', models.CharField(max_length=255, verbose_name='Hashed Password')),
                ('Phone', models.CharField(blank=True, max_length=15, null=True)),
                ('Age', models.IntegerField(blank=True, null=True)),
                ('Role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=10, verbose_name='User Role')),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
                ('Updated_At', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User Device',
                'verbose_name_plural': 'User Devices',
                'db_table': 'UserDevice',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False, verbose_name='Serial Number')),
                ('User_ID', models.CharField(max_length=50, verbose_name='User ID')),
                ('Device_ID', models.CharField(max_length=50, unique=True, verbose_name='Device ID')),
                ('Latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('Longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
                ('Updated_At', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
                'db_table': 'Device',
            },
        ),
        migrations.CreateModel(
            name='SensorValue',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False, verbose_name='Serial Number')),
                ('Device_ID', models.CharField(max_length=50, verbose_name='Device ID')),
                ('Temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pH', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('EC', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Electrical Conductivity')),
                ('Humidity', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Nitrogen', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('Phosphorus', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('Potassium', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('Light_Hours', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('Moisture', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Reading_Date', models.DateField()),
                ('Reading_Time', models.TimeField()),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sensor Value',
                'verbose_name_plural': 'Sensor Values',
                'db_table': 'SensorValue',
            },
        ),
    ]
```

Then run:
```bash
python manage.py migrate
```

### Option 3: Use SQLite Directly
```bash
python manage.py dbshell
```

Then paste this SQL:
```sql
CREATE TABLE UserDevice (
    S_No INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID VARCHAR(50) UNIQUE NOT NULL,
    Email_ID VARCHAR(254) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(15),
    Age INTEGER,
    Role VARCHAR(10) DEFAULT 'user',
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_At DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Device (
    S_No INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID VARCHAR(50) NOT NULL,
    Device_ID VARCHAR(50) UNIQUE NOT NULL,
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_At DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SensorValue (
    S_No INTEGER PRIMARY KEY AUTOINCREMENT,
    Device_ID VARCHAR(50) NOT NULL,
    Temperature DECIMAL(5,2),
    pH DECIMAL(4,2),
    EC DECIMAL(6,2),
    Humidity DECIMAL(5,2),
    Nitrogen DECIMAL(6,2),
    Phosphorus DECIMAL(6,2),
    Potassium DECIMAL(6,2),
    Light_Hours DECIMAL(4,2),
    Moisture DECIMAL(5,2),
    Reading_Date DATE NOT NULL,
    Reading_Time TIME NOT NULL,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_device_user ON Device(User_ID);
CREATE INDEX idx_device_id ON Device(Device_ID);
CREATE INDEX idx_sensor_device ON SensorValue(Device_ID);
CREATE INDEX idx_sensor_date ON SensorValue(Reading_Date);

.tables
.quit
```

Then create fake migration:
```bash
python manage.py makemigrations --empty hydroponics
```

Edit to just have:
```python
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = []
```

Then:
```bash
python manage.py migrate --fake
```

## 🆘 IF STILL STUCK

Try this nuclear option:

```bash
# 1. Comment out hydroponics from INSTALLED_APPS
# Edit config/settings/base.py and comment out:
# "greeva.hydroponics",

# 2. Run migrations for users only
python manage.py makemigrations users
python manage.py migrate

# 3. Uncomment hydroponics

# 4. Try again
python manage.py makemigrations hydroponics
python manage.py migrate
```

## ✅ AFTER SUCCESSFUL MIGRATION

```bash
# Verify tables
python manage.py dbshell
>>> .tables
>>> .schema UserDevice
>>> .quit

# Seed database
python manage.py shell
>>> exec(open('seed_database.py').read())
>>> exit()

# Start server
python manage.py runserver
```

---

**Current Status:** URLs fixed, waiting for migration to complete
**Next:** Try Option 1 (--skip-checks) if current command hangs
