# IMMEDIATE ACTION PLAN - Wire Up Functionality

## Files Created ✅
1. `/greeva/static/js/dashboard-interactions.js` - Main JavaScript for all interactions

## Files to Update Now:

### 1. Update `greeva/templates/pages/index.html`
**Add at the end before `{% endblock extra_javascript %}`:**
```html
<script src="{% static 'js/dashboard-interactions.js' %}"></script>
<script>
    // Add user data attributes for welcome message
    document.addEventListener('DOMContentLoaded', function() {
        const userDataDiv = document.createElement('div');
        userDataDiv.setAttribute('data-user-name', '{{ request.user.name|default:request.user.email }}');
        userDataDiv.setAttribute('data-user-role', '{{ request.user.role }}');
        userDataDiv.style.display = 'none';
        document.body.appendChild(userDataDiv);
    });
</script>
```

**Update sensor cards (around line 114-131):**
```html
<div class="col-xl-3 col-md-6">
    <div class="p-3 border rounded bg-light bg-opacity-50 h-100" 
         data-sensor-card
         data-device-id="{{ first_device.id }}"
         data-sensor-type="{{ sensor_type|lower }}"
         data-sensor-name="{{ sensor_type }}"
         data-sensor-value="{{ reading.value }}"
         data-sensor-unit="{% if 'Temperature' in sensor_type %}°C{% elif 'Humidity' in sensor_type %}%{% elif 'pH' in sensor_type %}pH{% elif 'Moisture' in sensor_type %}%{% else %}units{% endif %}"
         style="cursor: pointer; transition: all 0.3s ease;"
         onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 5px 15px rgba(0,0,0,0.1)';"
         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        <!-- existing card content -->
    </div>
</div>
```

### 2. Update `greeva/templates/partials/topbar.html`
**Line 484 - Fix role display:**
```html
<h6 class="my-0 fw-normal">{{ request.user.role|title }}</h6>
```

**Line 504-507 - Replace Wallet with Add Device:**
```html
<a href="javascript:void(0);" class="dropdown-item" onclick="showAddDeviceModal()">
    <i class="ti ti-device-plus me-1 fs-17 align-middle"></i>
    <span class="align-middle">Add Device</span>
</a>
```

### 3. Create Custom Logout View
**File: `greeva/users/auth_views.py`**
```python
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    """Custom logout view that clears session and redirects"""
    logout(request)
    return redirect('/auth/login/')
```

**Update `config/urls.py`:**
```python
from greeva.users.auth_views import custom_login_view, custom_signup_view, custom_logout_view

# Add to urlpatterns:
path("auth/logout/", custom_logout_view, name="custom_logout"),
```

**Update `greeva/templates/auth/modals.html` line 154:**
```html
<form method="post" action="{% url 'custom_logout' %}" class="w-50">
```

### 4. Include Modals in Base Template
**File: `greeva/templates/base.html`**
Add before `</body>`:
```html
{% include 'auth/modals.html' %}
```

### 5. Update Device Table to Show Real Data
**File: `greeva/templates/pages/index.html` (lines 159-175)**
```html
{% for device in devices %}
<tr>
    <td>
        <h5 class="fs-14 my-1">{{ device.name|default:device.device_id }}</h5>
        <span class="text-muted fs-12">{{ device.device_id }}</span>
    </td>
    <td>{{ device.latitude }}, {{ device.longitude }}</td>
    <td>Hydroponic System</td>
    <td>
        {% if device.is_active %}
        <i class="ti ti-circle-filled fs-12 text-success"></i> Active
        {% else %}
        <i class="ti ti-circle-filled fs-12 text-danger"></i> Offline
        {% endif %}
    </td>
</tr>
{% empty %}
<tr>
    <td colspan="4" class="text-center text-muted">No devices found. <a href="javascript:void(0);" onclick="showAddDeviceModal()">Add your first device</a></td>
</tr>
{% endfor %}
```

### 6. Add ApexCharts CDN
**File: `greeva/templates/pages/index.html`**
In `{% block extra_css %}`:
```html
<link href="https://cdn.jsdelivr.net/npm/apexcharts/dist/apexcharts.css" rel="stylesheet">
```

In `{% block extra_javascript %}`:
```html
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
```

### 7. Fix Navigation Links
**File: `greeva/templates/partials/sidenav.html`**
Update menu items:
- Dashboard: `href="/"`
- Analytics: `href="/analytics/"`
- Map: `href="/map/"`
- Profile: `href="{% url 'users:profile' %}"`

## Testing Checklist:
- [ ] Login works and redirects to dashboard
- [ ] Signup creates user and shows OTP
- [ ] OTP verification activates account
- [ ] Dashboard shows real device count
- [ ] Sensor cards are clickable
- [ ] Sensor popup shows and updates every second
- [ ] Add Device button opens modal
- [ ] Add Device saves to DB and refreshes page
- [ ] Logout clears session and redirects
- [ ] Admin sees all devices
- [ ] User sees only own devices
- [ ] Welcome message appears on load
- [ ] Profile dropdown works
- [ ] Analytics page loads
- [ ] Map page loads

## Next Steps After These Updates:
1. Test all functionality
2. Fix any errors
3. Implement draggable blocks (GridStack.js)
4. Implement interactive map (Leaflet.js)
5. Add analytics charts
6. CSS fixes for exact screenshot match
