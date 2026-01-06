import os
import django
import sys

print("Setting up Django...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    django.setup()
    print("Django setup successful.")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

print("Importing models...")
try:
    from greeva.hydroponics.models import Device, SensorData
    print("Models imported successfully.")
except Exception as e:
    print(f"Model import failed: {e}")
    sys.exit(1)

print("Checking migrations...")
from django.core.management import call_command
try:
    call_command('check')
    print("Check command passed.")
except Exception as e:
    print(f"Check command failed: {e}")
