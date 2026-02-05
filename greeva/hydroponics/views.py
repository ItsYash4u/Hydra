"""
Hydroponics Views - Connected to Custom Database Table
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
import json

from .models_custom import Device, SensorValue, UserDevice
from greeva.users.auth_helpers import custom_login_required, get_current_user
from django.views.decorators.csrf import ensure_csrf_cookie


@custom_login_required
@ensure_csrf_cookie
def dashboard_view(request):
    """
    Main dashboard view using Custom Database
    - ADMIN: Shows all devices
    - USER: Shows only devices owned by the logged-in user
    """
    current_user = get_current_user(request)
    if not current_user:
        return redirect('/auth/login/')

    role = request.session.get('role', 'user')
    is_admin = (role == 'admin')

    if is_admin:
        devices_qs = Device.objects.all().order_by('-Created_At')
    else:
        devices_qs = Device.objects.filter(user=current_user).order_by('-Created_At')

    search_query = request.GET.get('q')
    if search_query:
        devices_qs = devices_qs.filter(Device_ID__icontains=search_query)

    devices = []
    for d in devices_qs:
        try:
            selected_sensors = json.loads(d.Device_Sensors) if d.Device_Sensors else []
        except (TypeError, ValueError):
            selected_sensors = []
        location_text = (
            f"{d.Latitude}, {d.Longitude}"
            if d.Latitude is not None and d.Longitude is not None
            else "-"
        )
        devices.append({
            'id': d.Device_ID,
            's_no': d.S_No,
            'name': d.Device_Name or d.Device_ID,
            'device_name': d.Device_Name or d.Device_ID,
            'sensor_id': d.Device_ID,
            'location': location_text,
            'latitude': float(d.Latitude) if d.Latitude else 20.59,
            'longitude': float(d.Longitude) if d.Longitude else 78.96,
            'device_type': d.Device_Type,
            'device_type_label': d.get_Device_Type_display(),
            'device_sensors': selected_sensors,
            'status': 'online',
        })

    total_devices = len(devices)
    online_devices = total_devices
    offline_devices = 0

    first_device = devices[0] if devices else None
    latest_readings = {}

    base_readings = {
        'Temperature': {'value': 0, 'timestamp': timezone.now()},
        'Humidity': {'value': 0, 'timestamp': timezone.now()},
        'pH': {'value': 0, 'timestamp': timezone.now()},
        'EC': {'value': 0, 'timestamp': timezone.now()},
        'CO2': {'value': 0, 'timestamp': timezone.now()},
    }

    if first_device:
        selected = set(first_device.get('device_sensors') or [])
        if not selected:
            selected = {'temperature', 'humidity', 'ph', 'ec', 'co2'}
        reading = (
            SensorValue.objects
            .filter(device_id=str(first_device['id']))
            .order_by('-date')
            .first()
        )

        if reading:
            latest_readings = dict(base_readings)
            latest_readings['Temperature'] = {'value': reading.temperature if 'temperature' in selected and reading.temperature is not None else 0, 'timestamp': reading.date}
            latest_readings['Humidity'] = {'value': reading.humidity if 'humidity' in selected and reading.humidity is not None else 0, 'timestamp': reading.date}
            latest_readings['pH'] = {'value': reading.pH if 'ph' in selected and reading.pH is not None else 0, 'timestamp': reading.date}
            latest_readings['EC'] = {'value': reading.EC if 'ec' in selected and reading.EC is not None else 0, 'timestamp': reading.date}
            latest_readings['CO2'] = {'value': reading.CO2 if 'co2' in selected and reading.CO2 is not None else 0, 'timestamp': reading.date}
        else:
            latest_readings = dict(base_readings)
    else:
        latest_readings = dict(base_readings)

    default_sensors = {
        'Temperature': True,
        'Humidity': True,
        'pH': True,
        'EC': True,
        'CO2': True,
    }

    enabled_sensors = request.session.get('sensor_preferences', {})
    for k, v in default_sensors.items():
        if k not in enabled_sensors:
            enabled_sensors[k] = v

    display_name = current_user.Email_ID if current_user else 'User'
    total_users_count = UserDevice.objects.count() if is_admin else None

    context = {
        'devices': devices,
        'air_devices': [d for d in devices if d.get('device_type') == 'AIR'],
        'water_devices': [d for d in devices if d.get('device_type') == 'WATER'],
        'total_devices': total_devices,
        'total_users': total_users_count,
        'online_devices': online_devices,
        'offline_devices': offline_devices,
        'first_device': first_device,
        'latest_readings': latest_readings,
        'recent_alerts': [],
        'user_name': display_name,
        'enabled_sensors': enabled_sensors,
        'is_admin': is_admin,
    }

    return render(request, 'pages/index.html', context)


def get_latest_data(request, device_id):
    """
    API: Fetch latest sensor data
    """
    reading = (
        SensorValue.objects
        .filter(device_id=device_id)
        .order_by('-date')
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


def add_device_view(request):
    """
    Legacy Add Device endpoint (kept for compatibility)
    """
    return JsonResponse({'success': False, 'error': 'Use /api/devices/add-device/'}, status=403)
