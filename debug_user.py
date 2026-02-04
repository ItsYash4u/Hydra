import os
import django
import sys
from pathlib import Path
import pymysql

pymysql.install_as_MySQLdb()

# Add project root and greeva app to path
current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path / "greeva"))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User as DjangoUser
from greeva.hydroponics.models_custom import UserDevice
from django.db.models import Q

email_input = "yashsinghkushwaha345@gmail.com"
password_input = "Dpa1xw3mw7"

with open("debug_output.txt", "w") as f:
    f.write(f"--- DEBUGGING USER: {email_input} ---\n")

    # 1. Check Django User
    f.write("\n1. Checking Django Admin User...\n")
    dj_user = DjangoUser.objects.filter(Q(email__iexact=email_input) | Q(username__iexact=email_input)).first()

    if dj_user:
        f.write(f"   [FOUND] Django User: {dj_user.username} (Email: {dj_user.email})\n")
        if dj_user.check_password(password_input):
            f.write("   [SUCCESS] Password MATCHES Django User.\n")
        else:
            f.write("   [FAIL] Password DOES NOT MATCH Django User.\n")
    else:
        f.write("   [NOT FOUND] No Django User found with this email/username.\n")

    # 2. Check UserDevice
    f.write("\n2. Checking UserDevice (Custom DB)...")
    try:
        user_device = UserDevice.objects.get(Email_ID=email_input)
        f.write(f"\n   [FOUND] UserDevice: {user_device.User_ID}\n")
        
        from django.contrib.auth.hashers import check_password
        is_match = check_password(password_input, user_device.Password)
        
        if is_match:
            f.write("   [SUCCESS] Password MATCHES UserDevice.\n")
        else:
            f.write("   [FAIL] Password DOES NOT MATCH UserDevice.\n")
            f.write(f"   Hash stored: {user_device.Password[:20]}...\n")
    except UserDevice.DoesNotExist:
        f.write("\n   [NOT FOUND] No UserDevice found.\n")

    f.write("\n--- END DEBUG ---\n")
