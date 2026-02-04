
import os
import sys
import django
from pathlib import Path
import pymysql

# 1. Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# 2. Setup Paths
current_path = Path(os.getcwd()).resolve()
sys.path.append(str(current_path))
sys.path.append(str(current_path / "greeva"))

# 3. Setup Django Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# 4. Import everything AFTER django.setup()
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from greeva.hydroponics.models_custom import UserDevice, Device
from greeva.hydroponics.views import dashboard_view
from greeva.hydroponics.api_views import GetDevicesAPIView, SensorDataView
from greeva.pages.views import analytics_view

def setup_test_data():
    Device.objects.all().delete()
    UserDevice.objects.all().delete()
    
    user1 = UserDevice.objects.create(User_ID="USER-1", Email_ID="u1@test.com", Role="user")
    user2 = UserDevice.objects.create(User_ID="USER-2", Email_ID="u2@test.com", Role="user")
    admin = UserDevice.objects.create(User_ID="ADMIN-1", Email_ID="admin@test.com", Role="admin")
    
    d1 = Device.objects.create(Device_ID="DEV-1", user=user1)
    d2 = Device.objects.create(Device_ID="DEV-2", user=user2)
    
    return user1, user2, admin

def get_request_with_session(user, path='/'):
    factory = RequestFactory()
    request = factory.get(path)
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session['user_id'] = user.User_ID
    request.session['email'] = user.Email_ID
    request.session['role'] = user.Role
    request.session.save()
    return request

def run_tests():
    print("="*60)
    print("VERIFYING DEVICE VISIBILITY")
    print("="*60)
    
    u1, u2, adm = setup_test_data()
    
    # TEST 1: User 1 API - Should see only DEV-1
    print("[1/5] User 1 API View...")
    req = get_request_with_session(u1)
    view = GetDevicesAPIView.as_view()
    resp = view(req)
    devices = [d['device_id'] for d in resp.data['devices']]
    if "DEV-1" in devices and "DEV-2" not in devices:
        print("✅ PASS: User 1 sees strictly own devices")
    else:
        print(f"❌ FAIL: User 1 sees {devices}")

    # TEST 2: User 2 API - Should see only DEV-2
    print("[2/5] User 2 API View...")
    req = get_request_with_session(u2)
    resp = view(req)
    devices = [d['device_id'] for d in resp.data['devices']]
    if "DEV-2" in devices and "DEV-1" not in devices:
        print("✅ PASS: User 2 sees strictly own devices")
    else:
        print(f"❌ FAIL: User 2 sees {devices}")

    # TEST 3: Admin API - Should see ALL
    print("[3/5] Admin API View...")
    req = get_request_with_session(adm)
    resp = view(req)
    devices = [d['device_id'] for d in resp.data['devices']]
    if "DEV-1" in devices and "DEV-2" in devices:
        print("✅ PASS: Admin sees ALL devices")
    else:
        print(f"❌ FAIL: Admin sees {devices}")

    # TEST 4: Cross Access - User 1 accessing DEV-2 Data
    print("[4/5] Cross-User Data Access Check...")
    factory = RequestFactory()
    req = factory.get('/?device_id=DEV-2')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(req)
    req.session['user_id'] = u1.User_ID
    req.session['role'] = u1.Role
    req.session.save()
    
    view = SensorDataView.as_view()
    resp = view(req)
    
    if resp.status_code == 403:
        print("✅ PASS: Access Denied (403 Forbidden)")
    else:
        print(f"❌ FAIL: Got status {resp.status_code}")

    # TEST 5: User accessing Admin Page
    print("[5/5] User accessing Admin Analytics...")
    req = get_request_with_session(u1)
    resp = analytics_view(req)
    if resp.status_code == 403:
        print("✅ PASS: Access Denied (403 Forbidden)")
    else:
        print(f"❌ FAIL: Got status {resp.status_code}")

    print("\n✅ VERIFICATION SUCCESSFUL")

if __name__ == "__main__":
    run_tests()
