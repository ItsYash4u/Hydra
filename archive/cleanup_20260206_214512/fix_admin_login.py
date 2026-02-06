import os
import sys
import django
from pathlib import Path

# Setup paths
current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path))
sys.path.append(str(current_path / "greeva"))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth import get_user_model

def fix_admin():
    User = get_user_model()
    email = "admin@example.com"
    password = "admin"

    try:
        user, created = User.objects.get_or_create(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        action = "Created" if created else "Updated"
        print(f"\nSUCCESS: {action} superuser account.")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("\nPlease try logging in with these credentials.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_admin()
