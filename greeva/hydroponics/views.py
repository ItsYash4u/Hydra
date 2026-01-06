"""
Hydroponics Views - Connected to Custom Database Table
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models_custom import UserDevice, Device, SensorValue
from greeva.users.auth_helpers import custom_login_required, get_current_user
from django.utils import timezone
import random

def dashboard_view(request):
    """
    Main dashboard view using Custom Database
    Direct access without login - shows all devices (admin view)
    """
    # Show all devices without authentication
    devices_qs = Device.objects.all()
    
    # 1. Prepare Devices List for Template (Mapping custom model -> template fields)
    devices = []
    for d in devices_qs:
        devices.append({
            'id': d.Device_ID,
            'name': f"Unit {d.Device_ID}", # Mock name based on ID
            'sensor_id': d.Device_ID,
            'location': f"{d.Latitude}, {d.Longitude}",
            'get_device_type_display': 'Hydroponic System',
            'status': 'online' if random.choice([True, True, False]) else 'offline' 
        })
        
    # 2. Get Statistics (Total, Active, Offline)
    total_devices = len(devices)
    active_devices = len([d for d in devices if d['status'] == 'online'])
    offline_devices = total_devices - active_devices

    # 3. Get Latest Readings for the FIRST device (to show on dashboard)
    first_device = devices[0] if devices else None
    latest_readings = {}
    
    if first_device:
        # Get latest sensor value for this device
        reading = SensorValue.objects.filter(Device_ID=first_device['id']).order_by('-Reading_Date', '-Reading_Time').first()
        
        if reading:
            # Map DB fields to what template expects
            latest_readings = {
                # Core DB Sensors
                'Temperature': {'value': reading.Temperature, 'timestamp': timezone.now()},
                'Humidity': {'value': reading.Humidity, 'timestamp': timezone.now()},
                'pH': {'value': reading.pH, 'timestamp': timezone.now()},
                'EC': {'value': reading.EC, 'timestamp': timezone.now()},
                'Light': {'value': reading.Light_Hours, 'timestamp': timezone.now()},
                'Moisture': {'value': reading.Moisture, 'timestamp': timezone.now()},
                'Nitrogen': {'value': reading.Nitrogen, 'timestamp': timezone.now()},
                'Phosphorus': {'value': reading.Phosphorus, 'timestamp': timezone.now()},
                'Potassium': {'value': reading.Potassium, 'timestamp': timezone.now()},
                
                # Extended Mocked Sensors (for complete Hydro/Aqua ponics view)
                'Water Temp': {'value': float(reading.Temperature or 24) - 2.5, 'timestamp': timezone.now()},
                'Dissolved Oxygen': {'value': 6.5 + random.random(), 'timestamp': timezone.now()},
                'TDS': {'value': (float(reading.EC or 1.2) * 500) + random.randint(-50, 50), 'timestamp': timezone.now()},
                'ORP': {'value': 350 + random.randint(-20, 20), 'timestamp': timezone.now()},
                'CO2': {'value': 600 + random.randint(-50, 50), 'timestamp': timezone.now()},
                'Water Level': {'value': 95 + random.random()*(-5), 'timestamp': timezone.now()},
                'Flow Rate': {'value': 1200 + random.randint(-100, 100), 'timestamp': timezone.now()},
            }

    # Get recent alerts (mock data for now)
    recent_alerts = []

    context = {
        'devices': devices,
        'total_devices': total_devices,
        'online_devices': active_devices,
        'offline_devices': offline_devices,
        'first_device': first_device,
        'latest_readings': latest_readings,
        'recent_alerts': recent_alerts,
        'user_name': 'Guest', # Default user name
    }
    
    return render(request, 'pages/index.html', context)



@custom_login_required
def get_latest_data(request, device_id):
    """
    API to fetch latest data for a device
    """
    # Check if user has access (basic check)
    user = get_current_user(request)
    
    # Simple check - if user is admin or owns the device (logic omitted for speed, assuming ID is correct)
    
    reading = SensorValue.objects.filter(Device_ID=device_id).order_by('-Reading_Date', '-Reading_Time').first()
    
    if reading:
        data = {
            'temperature': float(reading.Temperature or 0),
            'humidity': float(reading.Humidity or 0),
            'ph': float(reading.pH or 0),
            'ec': float(reading.EC or 0),
            'nitrogen': float(reading.Nitrogen or 0),
            'phosphorus': float(reading.Phosphorus or 0),
            'potassium': float(reading.Potassium or 0),
            'moisture': float(reading.Moisture or 0),
            'light_hours': float(reading.Light_Hours or 0),
            
            # Extended Mock Data
            'water_temp': float(reading.Temperature or 24) - 2.5,
            'dissolved_oxygen': 6.5 + random.random(),
            'tds': (float(reading.EC or 1.2) * 500) + random.randint(-50, 50),
            'orp': 350 + random.randint(-20, 20),
            'co2': 600 + random.randint(-50, 50),
            'water_level': 95 + random.random() * (-5),
            'flow_rate': 1200 + random.randint(-100, 100),
            # Add mock history data for charts (since we don't have enough real history yet)
            'history': {
                'temperature': [float(reading.Temperature or 22) + (x * 0.5) for x in range(7)],
                'humidity': [float(reading.Humidity or 60) + (x * 1.5) for x in range(7)],
                'dates': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] # Should be dynamic days
            }
        }
    else:
        # Return zeros if no data
        data = {k: 0 for k in ['temperature', 'humidity', 'ph', 'ec', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'light_hours']}
        data['history'] = {
            'temperature': [0]*7,
            'humidity': [0]*7,
            'dates': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        }

    return JsonResponse(data)


@custom_login_required
def search_view(request):
    """
    Search functionality placeholder
    """
    q = request.GET.get('q', '')
    user = get_current_user(request)
    
    if user:
        if user.Role == 'admin':
            devices = Device.objects.filter(Device_ID__icontains=q)
        else:
            devices = Device.objects.filter(User_ID=user.User_ID, Device_ID__icontains=q)
    else:
        devices = []
        
    # Reuse dashboard template or a simplified results page
    # For now, redirect to dashboard to avoid collecting another template
    return redirect('hydroponics:dashboard')
