
import os
import django
import sys
import logging
import random
import string

# Setup Django Environment
sys.path.append('c:/Users/AYUSH/Downloads/admin/Greeva')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from greeva.users.models import OTP

User = get_user_model()

def test_otp_login_flow():
    print("\n🚀 Testing OTP on LOGIN...")
    
    # 1. Get or Create a Test User
    email = "test_otp_login@example.com"
    user, created = User.objects.get_or_create(email=email, defaults={'name': 'Test OTP Login User'})
    if created:
        user.set_password("password123")
        user.save()
        print(f"✅ Created test user for login: {email}")
    else:
        print(f"ℹ️  Using existing test user for login: {email}")

    # 2. Count existing OTPs
    initial_otp_count = OTP.objects.filter(user=user).count()
    print(f"📊 Initial OTP count: {initial_otp_count}")
    
    # 3. Trigger Login Signal (simulate login)
    print("🔄 Simulating User Login...")
    class MockRequest:
        pass
        
    user_logged_in.send(sender=User, user=user, request=MockRequest())
    
    # 4. Verify OTP was created
    new_otp_count = OTP.objects.filter(user=user).count()
    print(f"📊 New OTP count: {new_otp_count}")
    
    if new_otp_count > initial_otp_count:
        latest_otp = OTP.objects.filter(user=user).last()
        print(f"✅ SUCCESS: New OTP created for LOGIN! Code: {latest_otp.code}")
    else:
        print("❌ FAILURE: No OTP was created for LOGIN.")

def test_otp_creation_flow():
    print("\n🚀 Testing OTP on ACCOUNT CREATION...")
    
    # Generate unique email
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    email = f"test_creation_{random_suffix}@example.com"
    
    print(f"1. Creating new user: {email}")
    user = User.objects.create_user(
        email=email, 
        password="password123",
        name="Test Creation User"
    )
    
    # 2. Verify OTP was created
    otp_count = OTP.objects.filter(user=user).count()
    print(f"📊 OTP count for {email}: {otp_count}")
    
    if otp_count > 0:
        latest_otp = OTP.objects.filter(user=user).last()
        print(f"✅ SUCCESS: OTP created for CREATION! Code: {latest_otp.code}")
    else:
        print("❌ FAILURE: No OTP was created for CREATION.")

if __name__ == "__main__":
    try:
        test_otp_login_flow()
        test_otp_creation_flow()
    except Exception as e:
        print(f"❌ ERROR: {e}")
