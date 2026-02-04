# Fix: 403 Forbidden Error on "View All Devices" Page

## Problem
When a regular user logged into the dashboard and clicked on "View All Devices", they received a **403 Forbidden** error stating:
```
403 Forbidden
You do not have permission to access this page.
This page is restricted to administrators only.
```

## Root Cause
The `devices_list_view` in `greeva/pages/views.py` was decorated with `@admin_required`, which blocked all non-admin users from accessing the page. This was inconsistent with the user's requirement that regular users should be able to view all their devices in one place.

## Solution
Modified the `devices_list_view` to implement **role-based access control (RBAC)** similar to the dashboard view:

### Changes Made

#### 1. **Updated `greeva/pages/views.py`** (lines 179-221)
- **Changed decorator**: `@admin_required` → `@custom_login_required`
- **Added role-based filtering**:
  - **Admin users**: See ALL devices across all users
  - **Regular users**: See ONLY their own devices
- **Added owner information**: Admins can see which user owns each device
- **Added `is_admin` flag** to context for template conditional rendering

```python
@custom_login_required
def devices_list_view(request):
    """
    View for displaying the full list of registered devices.
    USER: Shows only their own devices
    ADMIN: Shows all devices across all users
    """
    # Get current user and role
    current_user = get_current_user(request)
    role = request.session.get('role', 'user')
    is_admin = (role == 'admin')
    
    # Filter devices based on role (same logic as dashboard)
    if is_admin:
        devices_qs = Device.objects.all().order_by('Device_ID')
    else:
        devices_qs = Device.objects.filter(user=current_user).order_by('Device_ID')
    
    # ... rest of the implementation
```

#### 2. **Updated `greeva/templates/pages/devices_list.html`**
- **Dynamic page title**: Shows "All Devices" for admins, "My Devices" for users
- **Added owner column**: Visible only to admins, shows device owner with a badge
- **Added navigation**: "Back to Dashboard" button for easy navigation
- **Added "Add Device" button**: For regular users to link new devices
- **Improved empty state**: Different messages for admins vs users
- **Added device linking modal**: Users can link new devices directly from this page

### Key Features

✅ **Role-Based Visibility**
- Admins see all devices from all users
- Users see only their own devices

✅ **Owner Information**
- Admin view includes an "Owner" column showing which user owns each device
- Regular users don't see this column (not relevant to them)

✅ **Consistent UX**
- Same RBAC pattern as dashboard view
- Clear messaging about what the user is viewing
- Easy navigation back to dashboard

✅ **Device Management**
- Users can add devices directly from the "View All Devices" page
- Same device linking functionality as the dashboard

## Testing

### As a Regular User:
1. Login with any user account (e.g., `user1@greeva.com` / `user123`)
2. Go to Dashboard
3. Click "View All Devices" button
4. ✅ Should see only your own devices
5. ✅ Should see "My Devices" as the page title
6. ✅ Should see "Add Device" button
7. ✅ Should NOT see owner column

### As an Admin:
1. Login with admin account (`yashsinghkushwaha345@gmail.com` / `1234567890`)
2. Go to Dashboard
3. Click "View All Devices" button
4. ✅ Should see ALL devices from ALL users
5. ✅ Should see "All Registered Devices" as the page title
6. ✅ Should see owner column with user badges
7. ✅ Should NOT see "Add Device" button (admins don't link devices)

## Files Modified

1. `greeva/pages/views.py` - Updated `devices_list_view` function
2. `greeva/templates/pages/devices_list.html` - Enhanced template with RBAC support

## Impact

- ✅ **No breaking changes** to existing functionality
- ✅ **Consistent with existing RBAC** implementation
- ✅ **Improved user experience** for both users and admins
- ✅ **Resolves the 403 Forbidden error** for regular users
