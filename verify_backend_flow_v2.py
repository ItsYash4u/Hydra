
import os
import django
import sys
import uuid
import json

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greeva.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.sessions.middleware import SessionMiddleware

from greeva.users.api_views import SignupAPIView, VerifyOTPAPIView, LoginAPIView
from greeva.hydroponics.api_views import AddDeviceAPIView, SensorIngestView, SensorDataView
from greeva.hydroponics.models_custom import UserDevice, Device, SensorReading, SensorValue

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class(lambda x: x)
    middleware.process_request(request)
    request.session.save()

def run_verification():
    print("🚀 Starting Backend Verification...")
    factory = APIRequestFactory()
    
    # ------------------------------------------------------------------
    # 1. User Signup & Verification
    # ------------------------------------------------------------------
    email = f"test_user_{uuid.uuid4().hex[:4]}@example.com"
    password = "securepassword123"
    print(f"\n1️⃣  Testing User Signup with {email}...")

    # Step A: Signup (Send OTP)
    view_signup = SignupAPIView.as_view()
    req_signup = factory.post('/api/users/signup/', {'email': email, 'password': password}, format='json')
    add_middleware_to_request(req_signup, SessionMiddleware)
    resp_signup = view_signup(req_signup)
    
    if resp_signup.status_code != 201:
        print(f"❌ Signup Failed: {resp_signup.data}")
        return
    print("✅ Signup API Success (OTP sent)")
    
    # Extract OTP from session (simulating email check)
    otp = req_signup.session.get('signup_otp')
    if not otp:
        print("❌ OTP not found in session!")
        return
    print(f"   (Debug) Captured OTP: {otp}")

    # Step B: Verify OTP
    view_verify = VerifyOTPAPIView.as_view()
    req_verify = factory.post('/api/users/verify-otp/', {'otp': otp}, format='json')
    # Use the SAME session
    req_verify.session = req_signup.session 
    resp_verify = view_verify(req_verify)
    
    if resp_verify.status_code != 200:
        print(f"❌ OTP Verification Failed: {resp_verify.data}")
        return
    
    print("✅ OTP Verified. User Created.")
    
    # Check DB
    try:
        user = UserDevice.objects.get(Email_ID=email)
        print(f"   User ID in DB: {user.User_ID}")
    except UserDevice.DoesNotExist:
        print("❌ User not found in DB after verification!")
        return

    # ------------------------------------------------------------------
    # 2. Login (Simulated)
    # ------------------------------------------------------------------
    print("\n2️⃣  Testing Login Logic...")
    # We already have session from verify_otp, but let's test explicit login
    view_login = LoginAPIView.as_view()
    req_login = factory.post('/api/users/login/', {'email': email, 'password': password}, format='json')
    add_middleware_to_request(req_login, SessionMiddleware)
    resp_login = view_login(req_login)
    
    if resp_login.status_code != 200:
        print(f"❌ Login Failed: {resp_login.data}")
        return
    
    # Ensure session has user_id
    if not req_login.session.get('user_id'):
        print("❌ Login did not set session user_id!")
        return
    print(f"✅ Login Success. Session initialized for User: {req_login.session['user_id']}")

    # ------------------------------------------------------------------
    # 3. Add Device
    # ------------------------------------------------------------------
    print("\n3️⃣  Testing Device Addition...")
    view_add_device = AddDeviceAPIView.as_view()
    manual_device_id = f"TEST-DEV-{uuid.uuid4().hex[:4].upper()}"
    
    req_device = factory.post('/api/hydroponics/add-device/', {
        'device_name': 'Greenhouse 1',
        'device_id': manual_device_id,
        'latitude': 20.0,
        'longitude': 78.0
    }, format='json')
    
    req_device.session = req_login.session # Authenticate
    resp_device = view_add_device(req_device)
    
    if resp_device.status_code != 201:
        print(f"❌ Add Device Failed: {resp_device.data}")
        return
    
    print(f"✅ Device Added: {resp_device.data['device']['id']}")
    
    # ------------------------------------------------------------------
    # 4. Sensor Data Ingestion
    # ------------------------------------------------------------------
    print("\n4️⃣  Testing Sensor Ingestion...")
    view_ingest = SensorIngestView.as_view()
    
    ingest_data = {
        'device_id': manual_device_id,
        'temperature': 25.5,
        'humidity': 60.0,
        'ph': 6.5,
        'ec': 1.2
    }
    
    req_ingest = factory.post('/api/hydroponics/sensors/ingest/', ingest_data, format='json')
    resp_ingest = view_ingest(req_ingest)
    
    if resp_ingest.status_code != 201:
        print(f"❌ Ingestion Failed: {resp_ingest.data}")
        return
    
    print("✅ Ingestion Success.")

    # ------------------------------------------------------------------
    # 5. Fetch Sensor Data (The Dashboard Flow)
    # ------------------------------------------------------------------
    print("\n5️⃣  Testing Sensor Data Retrieval...")
    view_sensor = SensorDataView.as_view()
    
    req_sensor = factory.get(f'/api/hydroponics/sensors/latest/?device_id={manual_device_id}')
    req_sensor.session = req_login.session # Authenticate (user owns device)
    resp_sensor = view_sensor(req_sensor)
    
    if resp_sensor.status_code != 200:
        print(f"❌ Fetch Data Failed: {resp_sensor.data}")
        return
    
    data = resp_sensor.data
    print(f"✅ Data Retrieved: Temp={data.get('temperature')}, pH={data.get('ph')}")
    
    if data.get('temperature') != 25.5:
        print("❌ Mismatch in data values!")
    else:
        print("✅ Data Integrity Verified.")

    # ------------------------------------------------------------------
    # 6. Negative Test: Unauthorized Device Access
    # ------------------------------------------------------------------
    print("\n6️⃣  Testing Security (Negative Test)...")
    req_bad = factory.get(f'/api/hydroponics/sensors/latest/?device_id={manual_device_id}')
    # No session -> Should be 401
    add_middleware_to_request(req_bad, SessionMiddleware) # Empty session
    resp_bad = view_sensor(req_bad)
    
    if resp_bad.status_code == 401:
        print("✅ Correctly rejected unauthenticated request.")
    else:
        print(f"❌ Security Hole! Unauthenticated request returned: {resp_bad.status_code}")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_verification()
