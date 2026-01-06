
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

try:
    django.setup()
    with open("debug_settings_output.txt", "w") as f:
        f.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}\n")
        f.write(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}\n")
    print("DONE")
except Exception as e:
    with open("debug_settings_output.txt", "w") as f:
        f.write(f"ERROR: {e}")
    print(f"ERROR: {e}")
