from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.http import Http404

# -------------------------
# Public / Landing Pages
# -------------------------

def root_page_view(request):
    """
    Root page - Show landing page for logged-out users,
    redirect to dashboard for logged-in users
    """
    if request.session.get('user_id'):
        return redirect('hydroponics:dashboard')
    return render(request, 'pages/landing.html')


def loading_view(request):
    """Loading animation page shown after login/signup"""
    return render(request, 'pages/loading.html')




# -------------------------
# Authenticated Pages
# -------------------------

@login_required
def measurement_view(request):
    return render(request, 'pages/measurement.html')


@login_required
def services_view(request):
    return render(request, 'pages/services.html')


# -------------------------
# Placeholder Pages
# (Device-based logic disabled
# until models are implemented)
# -------------------------

def analytics_view(request):
    """
    Analytics page - Direct access without login
    Shows all devices (admin view)
    """
    from greeva.hydroponics.models_custom import Device, SensorValue, UserDevice
    from django.utils import timezone
    from datetime import timedelta
    
    # Show all devices without authentication
    devices_qs = Device.objects.all()
    
    # Convert to list format expected by template
    devices = []
    for d in devices_qs:
        devices.append({
            'id': d.Device_ID,
            'device_id': d.Device_ID,
            'name': d.Device_Name or f"Unit {d.Device_ID}",
            'latitude': d.Latitude,
            'longitude': d.Longitude,
        })
    
    # Get selected device from query parameter or use first device
    device_id_param = request.GET.get('device_id')
    selected_device = None
    
    if device_id_param:
        # Find the selected device
        for d in devices:
            if d['device_id'] == device_id_param:
                selected_device = d
                break
    elif devices:
        selected_device = devices[0]
    
    context = {
        'devices': devices,
        'selected_device': selected_device,
        'is_admin': True  # Always admin view
    }
    return render(request, 'pages/analytics.html', context)




def map_view(request):
    """
    Map page - Direct access without login
    Shows all device locations
    """
    from greeva.hydroponics.models_custom import Device, UserDevice
    import json
    import random
    
    # Show all devices without authentication
    devices_qs = Device.objects.all()
    
    # Prepare map data
    map_points = []
    for device in devices_qs:
        # Get owner info
        try:
            owner = UserDevice.objects.get(User_ID=device.user_id)
            owner_name = owner.Email_ID.split('@')[0].title()
        except UserDevice.DoesNotExist:
            owner_name = device.user_id
        
        map_points.append({
            'device_id': device.Device_ID,
            'latitude': float(device.Latitude) if device.Latitude else 20.59,
            'longitude': float(device.Longitude) if device.Longitude else 78.96,
            'owner_name': owner_name,
            'status': 'Online' if random.choice([True, True, False]) else 'Offline'
        })
    
    # Calculate center point (average of all devices or default to India center)
    if map_points:
        avg_lat = sum(p['latitude'] for p in map_points) / len(map_points)
        avg_lon = sum(p['longitude'] for p in map_points) / len(map_points)
    else:
        avg_lat, avg_lon = 20.59, 78.96
    
    map_data = {
        'points': map_points,
        'center_lat': avg_lat,
        'center_lon': avg_lon,
    }
    
    context = {
        'map_data_json': json.dumps(map_data),
        'is_admin': True  # Always admin view
    }
    return render(request, 'pages/map.html', context)


def info_view(request):
    """
    Info page - Educational content about hydroponics
    No backend logic required - static informational page
    """
    return render(request, 'pages/info.html')





def devices_list_view(request):
    """
    View for displaying the full list of all registered devices.
    """
    from greeva.hydroponics.models_custom import Device
    import json
    
    # Fetch all devices
    devices_qs = Device.objects.all()
    
    devices = []
    for d in devices_qs:
        try:
            selected_sensors = json.loads(d.Device_Sensors) if d.Device_Sensors else []
        except (TypeError, ValueError):
            selected_sensors = []
        devices.append({
            'id': d.Device_ID,
            'name': d.Device_Name or d.Device_ID,
            'device_name': d.Device_Name or d.Device_ID,
            'sensor_id': d.Device_ID,
            'location': f"{d.Latitude}, {d.Longitude}",
            'device_type': d.Device_Type,
            'device_type_label': d.get_Device_Type_display(),
            'device_sensors': selected_sensors,
            'status': 'online'
        })
        
    context = {
        'devices': devices,
        'air_devices': [d for d in devices if d.get('device_type') == 'AIR'],
        'water_devices': [d for d in devices if d.get('device_type') == 'WATER'],
        'total_devices': len(devices),
        'online_devices': len([d for d in devices if d['status'] == 'online']),
        'offline_devices': len([d for d in devices if d['status'] == 'offline']),
    }
    return render(request, 'pages/devices_list.html', context)


# -------------------------
# Dynamic Pages
# -------------------------

def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        try:
            return render(request, f'pages/{template_name}')
        except TemplateDoesNotExist:
            raise Http404("Page not found")
