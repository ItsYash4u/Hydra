from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
from greeva.hydroponics.models_custom import UserDevice
import random
import uuid

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {otp}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)

class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')

        if not email or not password:
            return Response({'error': 'Email and Password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check existing user in Custom Table
        if UserDevice.objects.filter(Email_ID=email).exists():
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
            'age': request.data.get('age', 25), # Default age
            'phone': request.data.get('phone', '')
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
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not email and not phone:
            return Response({'error': 'Email or Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to find user by email or phone
            if email:
                user = UserDevice.objects.get(Email_ID=email)
            elif phone:
                user = UserDevice.objects.get(Phone=phone)
        except UserDevice.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify Password
        if not user.check_password(password):
             return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create Session for Custom Auth
        request.session['user_id'] = user.User_ID
        request.session['email'] = user.Email_ID
        request.session['role'] = user.Role
        request.session.save()
        
        return Response({'message': 'Login successful', 'redirect_url': '/loading/'}, status=status.HTTP_200_OK)



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

        # OTP Verified - Create UserDevice
        try:
            # Generate generic User ID if not provided
            new_user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"
            
            user = UserDevice(
                User_ID=new_user_id,
                Email_ID=signup_data['email'],
                Age=signup_data.get('age'),
                Phone=signup_data.get('phone'),
                Role='user' # Default role
            )
            user.set_password(signup_data['password'])
            user.save()
            
            # Auto Login
            request.session['user_id'] = user.User_ID
            request.session['email'] = user.Email_ID
            request.session['role'] = user.Role
            
            # Cleanup session
            del request.session['signup_otp']
            del request.session['signup_data']

            return Response({'message': 'Account verified.', 'redirect_url': '/loading/'}, status=status.HTTP_200_OK)
            
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
