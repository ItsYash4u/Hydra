"""
Hydroponics Views - Connected to Custom Database Table
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
import random
import json

from .models_custom import Device, SensorValue
from greeva.users.auth_helpers import custom_login_required, get_current_user


def dashboard_view(request):
    """
    Main dashboard view using Custom Database
    Public dashboard (no login required)
    """

    devices_qs = Device.objects.all().order_by('Device_ID')

    devices = []
    for d in devices_qs:
        devices.append({
            'id': d.Device_ID,
            'name': f"Unit {d.Device_ID}",
            'sensor_id': d.Device_ID,
            'location': f"{d.Latitude}, {d.Longitude}",
            'get_device_type_display': 'Hydroponic System',
            'status': 'online' if random.choice([True, True, False]) else 'offline',
        })

    total_devices = len(devices)
    online_devices = len([d for d in devices if d['status'] == 'online'])
    offline_devices = total_devices - online_devices

    first_device = devices[0] if devices else None
    latest_readings = {}

    if first_device:
        reading = (
            SensorValue.objects
            .filter(Device_ID=first_device['id'])
            .order_by('-date')   # ✅ ONLY REAL COLUMN
            .first()
        )

        if reading:
            latest_readings = {
                'Temperature': {'value': reading.temperature, 'timestamp': timezone.now()},
                'Humidity': {'value': reading.humidity, 'timestamp': timezone.now()},
                'pH': {'value': reading.pH, 'timestamp': timezone.now()},
                'EC': {'value': reading.EC, 'timestamp': timezone.now()},
                'Water Temp': {
                    'value': float(reading.temperature or 24) - 2.5,
                    'timestamp': timezone.now()
                },
                'Dissolved Oxygen': {
                    'value': 6.5 + random.random(),
                    'timestamp': timezone.now()
                },
                'TDS': {
                    'value': float(reading.EC or 1.2) * 500,
                    'timestamp': timezone.now()
                },
                'CO2': {
                    'value': 600 + random.randint(-50, 50),
                    'timestamp': timezone.now()
                },
            }

    default_sensors = {
        'Temperature': True,
        'Humidity': True,
        'pH': True,
        'EC': True,
        'Water Temp': False,
        'Dissolved Oxygen': False,
        'TDS': False,
        'CO2': False,
    }

    enabled_sensors = request.session.get('sensor_preferences', default_sensors)

    context = {
        'devices': devices,
        'total_devices': total_devices,
        'online_devices': online_devices,
        'offline_devices': offline_devices,
        'first_device': first_device,
        'latest_readings': latest_readings,
        'recent_alerts': [],
        'user_name': 'Guest',
        'enabled_sensors': enabled_sensors,
    }

    return render(request, 'pages/index.html', context)


def get_latest_data(request, device_id):
    """
    API: Fetch latest sensor data
    """

    reading = (
        SensorValue.objects
        .filter(Device_ID=device_id)
        .order_by('-date')   # ✅ ONLY REAL COLUMN
        .first()
    )

    if reading:
        data = {
            'temperature': float(reading.temperature or 0),
            'humidity': float(reading.humidity or 0),
            'ph': float(reading.pH or 0),
            'ec': float(reading.EC or 0),
        }
    else:
        data = {
            'temperature': 0,
            'humidity': 0,
            'ph': 0,
            'ec': 0,
        }

    return JsonResponse(data)


@custom_login_required
def search_view(request):
    """
    Device search
    """
    q = request.GET.get('q', '')
    user = get_current_user(request)

    if user and user.Role == 'admin':
        Device.objects.filter(Device_ID__icontains=q)

    return redirect('hydroponics:dashboard')


def save_sensor_preferences(request):
    """
    Save sensor visibility preferences (AJAX)
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    try:
        payload = json.loads(request.body)
        sensor_name = payload.get('sensor_name')
        enabled = payload.get('enabled', True)

        prefs = request.session.get('sensor_preferences', {})
        prefs[sensor_name] = enabled

        request.session['sensor_preferences'] = prefs
        request.session.modified = True

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
