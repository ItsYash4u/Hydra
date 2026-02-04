import os
import sys
import django
import pymysql

# Use pymysql as MySQLdb replacement
pymysql.install_as_MySQLdb()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Now run the command
from django.core.management import call_command

print("Creating test users and devices...")
call_command('seed_test_users')
print("\nDone!")
