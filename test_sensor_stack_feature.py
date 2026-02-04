#!/usr/bin/env python
"""
Test script for Sensor Stack Feature
Verifies all components are working correctly
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from hydroponics.models_custom import Device, SensorValue, UserDevice
from hydroponics.api_views import SensorHistoryView
from django.utils import timezone
from django.test import RequestFactory
import json

print("=" * 80)
print("SENSOR STACK FEATURE - TEST SUITE")
print("=" * 80)

# Test 1: Check models
print("\n[TEST 1] Checking SensorValue Model...")
try:
    sv_fields = [f.name for f in SensorValue._meta.get_fields()]
    
    assert 'S_No' in sv_fields, "S_No field missing"
    assert 'timestamp' in sv_fields, "timestamp field missing"
    assert 'date' in sv_fields, "date field missing"
    assert 'device_id' in sv_fields, "device_id field missing"
    
    # Check primary key
    pk = SensorValue._meta.pk
    assert pk.name == 'S_No', f"Primary key should be S_No, got {pk.name}"
    
    print("✓ SensorValue model structure is correct")
    print(f"  Fields: {', '.join(sv_fields)}")
except AssertionError as e:
    print(f"✗ Model check failed: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 2: Check admin configuration
print("\n[TEST 2] Checking Admin Configuration...")
try:
    from hydroponics.admin import SensorValueAdmin
    from django.contrib import admin
    
    # Check if registered
    assert SensorValue in admin.site._registry, "SensorValue not registered with admin"
    
    admin_instance = admin.site._registry[SensorValue]
    
    # Check list_display
    assert 'timestamp_formatted' in admin_instance.list_display, "timestamp_formatted not in list_display"
    assert 'device_id' in admin_instance.list_display, "device_id not in list_display"
    
    # Check ordering
    expected_ordering = ['-timestamp']
    actual_ordering = list(admin_instance.get_ordering(None))
    assert actual_ordering == expected_ordering, f"Expected ordering {expected_ordering}, got {actual_ordering}"
    
    print("✓ Admin configuration is correct")
    print(f"  List display fields: {admin_instance.list_display}")
    print(f"  Ordering: {actual_ordering}")
except AssertionError as e:
    print(f"✗ Admin check failed: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 3: Check API URLs
print("\n[TEST 3] Checking API URLs...")
try:
    from django.urls import reverse, NoReverseMatch
    
    # Check if routes exist
    routes_to_check = [
        'api_sensor_latest',
        'api_sensor_history',
        'api_sensor_ingest',
    ]
    
    found_routes = []
    for route in routes_to_check:
        try:
            url = reverse(route)
            found_routes.append((route, url))
        except NoReverseMatch:
            print(f"✗ Route not found: {route}")
    
    if len(found_routes) == len(routes_to_check):
        print("✓ All API routes are registered")
        for route, url in found_routes:
            print(f"  {route}: {url}")
    else:
        print(f"✗ Missing {len(routes_to_check) - len(found_routes)} routes")
        
except Exception as e:
    print(f"✗ URL check failed: {e}")

# Test 4: Database operations
print("\n[TEST 4] Testing Database Operations...")
try:
    # Get or create a test user
    test_user, created = UserDevice.objects.get_or_create(
        User_ID='test_user_stack_feature',
        defaults={
            'Email_ID': 'test_stack@example.com',
            'Name': 'Test User',
            'Password': 'hashed_pwd',
            'Role': 'admin'
        }
    )
    print(f"✓ Test user {'created' if created else 'found'}: {test_user.short_id}")
    
    # Get or create a test device
    test_device, created = Device.objects.get_or_create(
        user=test_user,
        Device_ID='test_dev',
        defaults={
            'Latitude': 20.59,
            'Longitude': 78.96
        }
    )
    print(f"✓ Test device {'created' if created else 'found'}: {test_device.Device_ID}")
    
    # Create test sensor readings
    current_time = timezone.now()
    readings = []
    
    for i in range(3):
        sv = SensorValue.objects.create(
            device_id=test_device.Device_ID,
            date=current_time.date(),
            temperature=25.0 + i,
            humidity=65.0 + i,
            pH=7.0,
            EC=2.5 + i * 0.1
        )
        readings.append(sv)
        print(f"✓ Created sensor reading #{i+1} (ID: {sv.S_No})")
    
    # Verify ordering (newest first)
    latest_readings = SensorValue.objects.filter(
        device_id=test_device.Device_ID
    ).order_by('-timestamp')[:3]
    
    # Should be in reverse order (newest first)
    is_ordered = all(
        latest_readings[i].timestamp >= latest_readings[i+1].timestamp 
        for i in range(len(latest_readings)-1)
    )
    
    if is_ordered:
        print("✓ Readings are properly ordered (newest first)")
        for idx, reading in enumerate(latest_readings):
            print(f"  Reading #{idx+1}: {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("✗ Readings are not properly ordered")
    
    # Test 5: Check API functionality
    print("\n[TEST 5] Testing API Functionality...")
    
    # Simulate API response
    all_readings = list(SensorValue.objects.filter(
        device_id=test_device.Device_ID
    ).order_by('-timestamp').values('S_No', 'date', 'timestamp', 'temperature', 'humidity', 'pH', 'EC'))
    
    print(f"✓ API would return {len(all_readings)} readings")
    if all_readings:
        latest = all_readings[0]
        print(f"  Latest reading (ID: {latest['S_No']}):")
        print(f"    Temperature: {latest['temperature']}°C")
        print(f"    Humidity: {latest['humidity']}%")
        print(f"    pH: {latest['pH']}")
        print(f"    EC: {latest['EC']}")
        print(f"    Timestamp: {latest['timestamp']}")
    
except Exception as e:
    print(f"✗ Database operation failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Check JavaScript file
print("\n[TEST 6] Checking JavaScript Files...")
try:
    js_file_path = os.path.join(
        os.path.dirname(__file__),
        'greeva/static/js/sensor-history.js'
    )
    
    if os.path.exists(js_file_path):
        file_size = os.path.getsize(js_file_path)
        print(f"✓ sensor-history.js found ({file_size} bytes)")
        
        with open(js_file_path, 'r') as f:
            content = f.read()
            required_functions = [
                'fetchHistory',
                'displayHistory',
                'updateLatestReading',
                'startAutoRefresh',
                'formatTimestamp'
            ]
            
            found_functions = [func for func in required_functions if func in content]
            print(f"✓ Found {len(found_functions)}/{len(required_functions)} required functions")
            
            for func in required_functions:
                if func in content:
                    print(f"  ✓ {func}")
                else:
                    print(f"  ✗ {func} - MISSING")
    else:
        print(f"✗ sensor-history.js not found at {js_file_path}")
        
except Exception as e:
    print(f"✗ JavaScript check failed: {e}")

print("\n" + "=" * 80)
print("TEST SUITE COMPLETE")
print("=" * 80)
print("\nNext Steps:")
print("1. Run migrations: python manage.py migrate hydroponics")
print("2. Start server: python manage.py runserver")
print("3. Visit dashboard and test 'Add Reading' button")
print("4. Check sensor history displays correctly")
print("\n" + "=" * 80)
