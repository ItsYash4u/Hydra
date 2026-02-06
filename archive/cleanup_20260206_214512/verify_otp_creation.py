
import os
import django
import sys
import random
import string

# Setup Django Environment
sys.path.append('c:/Users/AYUSH/Downloads/admin/Greeva')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth import get_user_model
from greeva.users.models import OTP

User = get_user_model()

def test_otp_creation_flow():
    print("🚀 Starting OTP creation signal verification...")
    
    # Generate unique email
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    email = f"test_creation_{random_suffix}@example.com"
    
    print(f"1. Creating new user: {email}")
    user = User.objects.create_user(
        username=email, # Assuming username is required or defaults to email, but let's be safe if username field removed
        email=email, 
        password="password123",
        name="Test Creation User"
    )
    
    # 2. Verify OTP was created
    otp_count = OTP.objects.filter(user=user).count()
    print(f"📊 OTP count for {email}: {otp_count}")
    
    if otp_count > 0:
        latest_otp = OTP.objects.filter(user=user).last()
        print(f"✅ SUCCESS: OTP created for new user! Code: {latest_otp.code}")
    else:
        print("❌ FAILURE: No OTP was created for the new user.")
        
    # Cleanup
    # user.delete()

if __name__ == "__main__":
    try:
        test_otp_creation_flow()
    except Exception as e:
        print(f"❌ ERROR: {e}")
