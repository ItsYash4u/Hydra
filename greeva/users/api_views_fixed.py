from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from greeva.utils.email_utils import send_templated_email
from greeva.hydroponics.models_custom import UserDevice
from greeva.users.models import User
import random
import re
from django.db import transaction
import time
import hashlib
from greeva.users.auth_helpers import get_current_user

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your Verification Code'
    send_templated_email(
        subject=subject,
        to_emails=email,
        template_name='emails/otp_email.html',
        text_template_name='emails/otp_email.txt',
        context={
            'subject': subject,
            'otp': otp,
            'recipient_name': '',
            'brand_name': 'Smart IOT IITG',
            'brand_tagline': 'Hydroponics Monitoring Platform',
            'footer_note': 'If you did not request this code, you can ignore this email.',
            'otp_valid_minutes': '10',
        },
    )


def generate_short_user_id(role: str) -> str:
    prefix = "ADM" if role == "admin" else "USR"
    pattern = re.compile(rf"^{prefix}(\d+)$")
    max_num = 0

    with transaction.atomic():
        for uid in UserDevice.objects.filter(User_ID__startswith=prefix).values_list('User_ID', flat=True):
            match = pattern.match(uid or "")
            if match:
                try:
                    max_num = max(max_num, int(match.group(1)))
                except ValueError:
                    continue

        next_num = max_num + 1
        width = 3
        if next_num > 999:
            width = 4

        user_id = f"{prefix}{next_num:0{width}d}"
        while UserDevice.objects.filter(User_ID=user_id).exists():
            next_num += 1
            if next_num > 999 and width == 3:
                width = 4
            user_id = f"{prefix}{next_num:0{width}d}"

    return user_id

class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')

        if not email or not password:
            return Response({'error': 'Email and Password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists in Django User table
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP and store in session (temporary stage)
        otp_code = generate_otp()
        
        # Store signup data in session temporarily
        request.session['signup_otp'] = otp_code
        request.session['signup_email'] = email
        request.session['signup_data'] = {
            'email': email,
            'password': password, 
            'name': name,
        }
        
        # For development, print OTP
        print(f"🔥 OTP for {email}: {otp_code}")
        
        try:
            send_otp_email(email, otp_code)
        except Exception as e:
            print(f"Failed to send email: {e}")

        return Response({'message': 'Signup successful. OTP sent to email.', 'email': email}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Django's User model
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify password
        if not user.check_password(password):
             return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create Session
        request.session['user_id'] = user.id
        request.session['email'] = user.email
        request.session['role'] = getattr(user, 'role', 'user')
        request.session['name'] = user.name or user.email
        request.session.save()
        
        return Response({'message': 'Login successful', 'redirect_url': '/hydroponics/dashboard/'}, status=status.HTTP_200_OK)



class VerifyOTPAPIView(APIView):
    permission_classes = []

    def post(self, request):
        otp_code = request.data.get('otp')
        
       # Retrieve from session
        session_otp = request.session.get('signup_otp')
        signup_data = request.session.get('signup_data')

        if not otp_code or not session_otp:
             return Response({'error': 'Invalid request or session expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(otp_code) != str(session_otp):
            return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

        # OTP Verified - Create Django User
        try:
            user = User.objects.create_user(
                email=signup_data['email'],
                password=signup_data['password'],
                name=signup_data.get('name', ''),
            )
            
            # Auto Login
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            request.session['role'] = getattr(user, 'role', 'user')
            request.session['name'] = user.name or user.email
            
            # Cleanup session
            del request.session['signup_otp']
            del request.session['signup_data']

            return Response({'message': 'Account verified.', 'redirect_url': '/hydroponics/dashboard/'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResendOTPAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        otp_code = generate_otp()
        request.session['signup_otp'] = otp_code
        print(f"🔥 Resent OTP: {otp_code}")
        return Response({'message': 'OTP resent.'}, status=status.HTTP_200_OK)

class CloudinarySignatureAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "")
        api_key = getattr(settings, "CLOUDINARY_API_KEY", "")
        api_secret = getattr(settings, "CLOUDINARY_API_SECRET", "")

        if not cloud_name or not api_key or not api_secret:
            return Response({'error': 'Cloudinary is not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        timestamp = int(time.time())
        signature_base = f"timestamp={timestamp}{api_secret}"
        signature = hashlib.sha1(signature_base.encode("utf-8")).hexdigest()

        return Response({
            'timestamp': timestamp,
            'signature': signature,
            'api_key': api_key,
            'cloud_name': cloud_name,
        }, status=status.HTTP_200_OK)
