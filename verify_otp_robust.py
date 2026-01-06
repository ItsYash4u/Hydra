
import os
import django
import sys
import logging
from smtplib import SMTPAuthenticationError, SMTPException

# Setup Django Environment
sys.path.append('c:/Users/AYUSH/Downloads/admin/Greeva')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from greeva.users.models import OTP

User = get_user_model()

def test_otp_flow():
    print("🚀 Starting OTP verification check...")
    
    # 1. Get or Create a Test User
    email = "test_otp_verify@example.com"
    user, created = User.objects.get_or_create(email=email, defaults={'name': 'Test OTP User'})
    if created:
        user.set_password("password123")
        user.save()
    
    # 2. Count existing OTPs
    initial_otp_count = OTP.objects.filter(user=user).count()
    
    # 3. Trigger Login Signal (simulate login)
    print("🔄 Simulating User Login...")
    class MockRequest:
        pass
        
    try:
        user_logged_in.send(sender=User, user=user, request=MockRequest())
        print("✅ Signal sent successfully.")
    except Exception as e:
        print(f"⚠️  Signal raised exception (Expected if SMTP creds are wrong): {e}")

    # 4. Verify OTP was created in DB regardless of email failure
    # The signal creates OTP *before* trying mail? 
    # Let's check my signals.py... 
    # Yes: OTP.objects.create(...) is called before send_mail.
    
    new_otp_count = OTP.objects.filter(user=user).count()
    print(f"📊 OTP count change: {initial_otp_count} -> {new_otp_count}")
    
    if new_otp_count > initial_otp_count:
        latest_otp = OTP.objects.filter(user=user).last()
        print(f"✅ SUCCESS: New OTP created in DB! Code: {latest_otp.code}")
    else:
        print("❌ FAILURE: No OTP was created in the database.")

if __name__ == "__main__":
    try:
        test_otp_flow()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
