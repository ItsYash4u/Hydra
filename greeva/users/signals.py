from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from greeva.utils.email_utils import send_templated_email
from .models import OTP, User
import random
import logging

logger = logging.getLogger(__name__)

def send_otp_email(user):
    """
    Helper function to generate and send OTP.
    """
    from django.conf import settings
    print(f"DEBUG: EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"DEBUG: EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEBUG: EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}")

    # Generate 6-digit OTP
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Save to DB
    OTP.objects.create(user=user, code=code)

    # Custom Email Content
    subject = "Smart IoT Login Verification"
    
    try:
        send_templated_email(
            subject=subject,
            to_emails=user.email,
            template_name='emails/otp_email.html',
            text_template_name='emails/otp_email.txt',
            context={
                'subject': subject,
                'otp': code,
                'recipient_name': user.name or '',
                'brand_name': 'Smart IOT IITG',
                'brand_tagline': 'Hydroponics Monitoring Platform',
                'footer_note': 'If you did not request this code, you can ignore this email.',
                'otp_valid_minutes': '10',
            },
        )
        print(f"OTP Email Sent to {user.email}: {code}")
        logger.info(f"OTP sent to {user.email}")
    except Exception as e:
        print(f"❌ Failed to send OTP to {user.email}: {e}")
        # Proactive hint for the user
        if "Username and Password not accepted" in str(e) or "Please log in" in str(e) or "authentication required" in str(e).lower():
            print("⚠️  HINT: It looks like your Email Configuration is missing or incorrect.")
            print("👉  Please check your .env file and ensure DJANGO_EMAIL_HOST_USER and DJANGO_EMAIL_HOST_PASSWORD are set correctly.")
            print("👉  If using Gmail, make sure you are using an 'App Password', not your login password.")



@receiver(post_save, sender=User)
def send_otp_on_creation(sender, instance, created, **kwargs):
    """
    Send OTP via email when a new user is created.
    """
    if created:
        print(f"🆕 New user created: {instance.email}. Sending OTP...")
        send_otp_email(instance)
