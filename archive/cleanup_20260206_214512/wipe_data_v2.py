
import os
import django
import sys
import pymysql

pymysql.install_as_MySQLdb()

# Add project root to path
sys.path.append(os.getcwd())
# Add greeva app directory to path (just in case imports depend on it being on path)
sys.path.append(os.path.join(os.getcwd(), 'greeva'))

# CORRECT SETTINGS MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

try:
    from greeva.hydroponics.models_custom import SensorValue, Device, UserDevice
    
    print("--- STARTING DELETION ---")
    
    c = SensorValue.objects.count()
    print(f"Deleting {c} SensorValues...")
    # SensorValue is managed=False, so delete() might not work as expected for some backends, 
    # but for MySQL it usually issues DELETE FROM.
    # However, since it is managed=False, Django *tests* prevent table creation, but usage is fine.
    SensorValue.objects.all().delete()
    
    c = Device.objects.count()
    print(f"Deleting {c} Devices...")
    Device.objects.all().delete()
    
    c = UserDevice.objects.count()
    print(f"Deleting {c} UserDevices...")
    UserDevice.objects.all().delete()
    
    print("--- ALL DATA DELETED SUCCESSFULLY ---")
except Exception as e:
    print(f"Error: {e}")
