import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

try:
    django.setup()
    from greeva.users.models import User
    print(f"Connected to database: {django.db.connection.settings_dict['NAME']}")
    print(f"Engine: {django.db.connection.settings_dict['ENGINE']}")
    count = User.objects.count()
    print(f"User count: {count}")
except Exception as e:
    print(f"Error: {e}")
