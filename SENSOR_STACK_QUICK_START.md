# Sensor Stack Feature - Quick Setup Guide

## Installation Steps

### 1. Apply Database Migration
```bash
cd c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva

# Run the migration
python manage.py migrate hydroponics
```

### 2. No Additional Dependencies
The feature uses existing dependencies. No pip install required.

### 3. Restart Django Server
```bash
# Stop the running server
python manage.py runserver

# You'll see the new features immediately
```

## What's New in UI

### Dashboard Changes:
1. **"Add Reading" Button** (next to "Customize Sensors")
   - Only visible to admin users
   - Opens modal to add new sensor readings

2. **"Add Sensor Reading" Modal**
   - Select a device
   - Enter sensor values (Temperature, Humidity, pH, EC)
   - Click "Add Reading"

3. **Sensor Reading History Section** (NEW)
   - Shows all readings in stack format
   - Newest reading marked as "Latest" (green border)
   - Previous readings numbered (#1, #2, etc.)
   - Displays date, time, and all sensor values

## How to Use

### Add a New Sensor Reading (Admin):
1. Log in as admin
2. Go to Dashboard
3. Click "Add Reading" button (blue button next to settings)
4. Select device from dropdown
5. Enter sensor values:
   - Temperature (°C)
   - Humidity (%)
   - pH (0-14)
   - EC (mS/cm)
6. Click "Add Reading"
7. Confirmation message shows
8. History section auto-refreshes with new reading

### View Sensor History:
1. Go to Dashboard
2. Scroll down to "Sensor Reading History" section
3. See all readings in stack format (newest first)
4. Each reading shows:
   - Date and Time
   - Status badge (Latest / #1 / #2 / etc.)
   - All 4 sensor values in cards

## Admin Panel Changes

### To Add Reading via Admin:
1. Go to Admin Panel → Hydroponics → Sensor Values
2. Click "Add Sensor Value" button
3. Enter:
   - Device ID (e.g., "ys01")
   - Date
   - Temperature
   - Humidity
   - pH
   - EC
4. Timestamp is auto-filled (read-only)
5. Click "Save"

### Viewing Readings in Admin:
- Sort by "Time" column to see newest readings first
- Filter by device_id to see readings for specific device
- Timestamp column shows HH:MM:SS format

## API Endpoints

### Get Latest Reading:
```bash
curl "http://localhost:8000/hydroponics/api/sensors/latest/?device_id=ys01" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Get Reading History:
```bash
curl "http://localhost:8000/hydroponics/api/sensors/history/?device_id=ys01" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Add New Reading:
```bash
curl -X POST "http://localhost:8000/hydroponics/api/sensors/ingest/" \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -H "X-CSRFToken=YOUR_CSRF_TOKEN" \
  -d '{
    "device_id": "ys01",
    "temperature": 25.5,
    "humidity": 65.0,
    "ph": 7.0,
    "ec": 2.5
  }'
```

## Database Structure

### SensorValue Table (sensor_value):
```
S_No (PK)      - Auto-generated unique ID
device_id      - Device ID (string)
date           - Date of reading
timestamp      - Exact time of reading (auto-filled)
temperature    - Temperature value
humidity       - Humidity value
pH             - pH value
EC             - EC value
```

**Key Points:**
- Multiple readings per device per day: ✓ Supported
- Automatic timestamp: ✓ Yes
- Chronological ordering: ✓ Newest first
- Data preservation: ✓ Old readings never deleted

## Troubleshooting

### Button not showing?
- Make sure you're logged in as admin
- Reload the page (Ctrl + R / Cmd + R)
- Check browser console (F12) for errors

### History section showing "No readings"?
- Make sure the device has readings in the database
- Try adding a new reading using the "Add Reading" button
- Check admin panel to verify data exists

### Modal not opening?
- Clear browser cache (Ctrl + Shift + Delete)
- Check if Bootstrap is loaded (run in console: `typeof bootstrap`)
- Check browser console for JavaScript errors

### API returning 401?
- Make sure you're authenticated
- Check session cookie exists
- Try logging out and back in

### Timestamp not showing?
- Check if migration ran successfully: `python manage.py showmigrations`
- Verify database changes: Check the sensor_value table structure

## File Changes Summary

### Modified Files:
1. `greeva/hydroponics/models_custom.py` - Added timestamp field and S_No primary key
2. `greeva/hydroponics/admin.py` - Updated SensorValueAdmin for new UI
3. `greeva/hydroponics/api_views.py` - Updated APIs and added SensorHistoryView
4. `greeva/hydroponics/api_urls.py` - Added new endpoint route
5. `greeva/templates/pages/index.html` - Added modal and history section

### New Files:
1. `greeva/static/js/sensor-history.js` - History display manager
2. `greeva/hydroponics/migrations/0003_add_sensorvalue_timestamp.py` - Migration file
3. `SENSOR_STACK_FEATURE_DOCUMENTATION.md` - Full documentation

## Next Steps

1. ✓ Review the changes
2. ✓ Run the migration
3. ✓ Test adding readings from admin panel
4. ✓ Test adding readings from dashboard modal
5. ✓ Verify history displays correctly
6. ✓ Check API endpoints work
7. ✓ Deploy to production

## Support

For issues or questions, refer to:
- Full documentation: `SENSOR_STACK_FEATURE_DOCUMENTATION.md`
- API documentation in admin panel
- Browser console for error messages
