import os
import sys

print("Setting up env...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
import django
try:
    django.setup()
    print("Django Setup Complete")
except Exception as e:
    print(f"Setup Failed: {e}")
    sys.exit(1)

print("Importing hydroponics models...")
try:
    from greeva.hydroponics import models
    print("Hydroponics models imported")
except Exception as e:
    print(f"Hydroponics models failed: {e}")

print("Importing pages views...")
try:
    from greeva.pages import views
    print("Pages views imported")
except Exception as e:
    print(f"Pages views failed: {e}")

print("Importing urls...")
try:
    from config import urls
    print("URLs imported")
except Exception as e:
    print(f"URLs failed: {e}")

print("Test Done")
