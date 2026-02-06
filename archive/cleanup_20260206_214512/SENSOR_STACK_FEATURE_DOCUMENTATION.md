# Sensor Value Stack Feature Implementation

## Overview
This feature allows admins to add multiple sensor readings to devices while preserving historical data. New readings are displayed at the top in a stack format (LIFO - Last In First Out).

## What's Changed

### 1. Database Model Changes (`models_custom.py`)
**Before:**
- `SensorValue` used `date` as the primary key
- Only one reading per device per day was possible
- New readings would overwrite old ones

**After:**
- `SensorValue` now has `S_No` as the primary key
- Added `timestamp` field (DateTimeField) for automatic recording of read time
- `date` field is now a regular field (not primary key)
- Support for multiple readings per device per day
- Database indexes on `(device_id, -timestamp)` for efficient queries
- Default ordering: `-timestamp` (newest first)

```python
class SensorValue(models.Model):
    S_No = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=50)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pH = models.FloatField()
    EC = models.FloatField()
```

### 2. Admin Panel Changes (`admin.py`)
**New Features:**
- Added `timestamp_formatted` method to display time in readable format (HH:MM:SS)
- Changed ordering to show newest readings first (`-timestamp`)
- Made timestamp field read-only
- Updated fieldsets to organize fields better
- Added filter by device_id
- Timestamp field is now collapsible for cleaner view

**Usage in Admin:**
- Admin can add new sensor readings using the standard Django admin "Add Sensor Value" button
- Each new reading automatically gets the current timestamp
- Old readings remain in the database

### 3. Backend API Changes (`api_views.py`)

#### Updated: `SensorDataView`
- Returns the latest (most recent) sensor reading
- Uses `-timestamp` ordering to fetch newest reading first
- Returns ISO format timestamps

**Endpoint:** `GET /hydroponics/api/sensors/latest/?device_id=<device_id>`

**Response:**
```json
{
    "temperature": 25.5,
    "humidity": 65.0,
    "ph": 7.0,
    "ec": 2.5,
    "timestamp": "2024-02-02T14:30:45.123456"
}
```

#### New: `SensorHistoryView`
- Returns all sensor readings for a device in stack format (newest first)
- Returns total count of readings
- Includes both date and timestamp for each reading

**Endpoint:** `GET /hydroponics/api/sensors/history/?device_id=<device_id>`

**Response:**
```json
{
    "device_id": "ys01",
    "total_readings": 5,
    "readings": [
        {
            "id": 15,
            "date": "2024-02-02",
            "timestamp": "2024-02-02T14:30:45.123456",
            "temperature": 25.5,
            "humidity": 65.0,
            "ph": 7.0,
            "ec": 2.5
        },
        {
            "id": 14,
            "date": "2024-02-02",
            "timestamp": "2024-02-02T13:20:30.654321",
            "temperature": 24.8,
            "humidity": 64.5,
            "ph": 6.95,
            "ec": 2.4
        }
        // ... more readings
    ]
}
```

#### Updated: `SensorIngestView`
- Now creates new readings with auto-generated timestamps
- Returns the created reading object with all details
- Changed device_id storage to use Device_ID (string) instead of S_No

**Endpoint:** `POST /hydroponics/api/sensors/ingest/`

**Request:**
```json
{
    "device_id": "ys01",
    "temperature": 25.5,
    "humidity": 65.0,
    "ph": 7.0,
    "ec": 2.5
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Data saved to SensorValue",
    "reading": {
        "id": 15,
        "device_id": "ys01",
        "date": "2024-02-02",
        "timestamp": "2024-02-02T14:30:45.123456",
        "temperature": 25.5,
        "humidity": 65.0,
        "ph": 7.0,
        "ec": 2.5
    }
}
```

### 4. Frontend Changes

#### New JavaScript Module: `sensor-history.js`
**Purpose:** Manage fetching and displaying sensor reading history

**Main Functions:**
- `fetchHistory(deviceId)` - Fetch all readings for a device
- `displayHistory(deviceId, containerId)` - Display readings in stack format
- `updateLatestReading(deviceId)` - Get just the latest reading
- `startAutoRefresh(deviceId, containerId, intervalMs)` - Auto-refresh history
- `stopAutoRefresh(intervalId)` - Stop auto-refresh
- `formatTimestamp(timestamp)` - Format timestamp for display
- `formatDate(dateStr)` - Format date for display

**Features:**
- Displays readings in stack format (newest on top, marked as "Latest")
- Shows each reading's details in a card with 4 sensor values
- Color-coded: green border for latest, gray for older
- Shows total reading count
- Handles loading state and empty state
- Auto-refresh capability

#### Updated: Dashboard (`index.html`)

**New Components:**

1. **"Add Reading" Button** (Admin only)
   - Located next to "Customize Sensors" button
   - Only visible to admin users
   - Opens the "Add Sensor Reading" modal

2. **"Add Sensor Reading" Modal** (`#addSensorValuesModal`)
   - Allows admin to add new readings
   - Fields: Device (dropdown), Temperature, Humidity, pH, EC
   - Auto-populates device list from API
   - Shows confirmation messages
   - Auto-refreshes history after successful submission

3. **Sensor Reading History Section**
   - New card between sensor monitor and device list
   - Displays all readings in stack format
   - Shows latest reading first
   - Auto-loads for first device on page load
   - Can be manually updated

**Usage Flow:**
1. Admin clicks "Add Reading" button
2. Modal opens with device list
3. Admin selects device and enters sensor values
4. Clicks "Add Reading"
5. API saves the reading with current timestamp
6. History section auto-refreshes to show new reading at the top
7. Old readings remain visible below

## Database Migration

To apply these changes to an existing installation:

```bash
# Run migrations
python manage.py migrate hydroponics

# If you have existing data, Django may ask about preserving the default value
# for the timestamp field. Choose option 2 (provide a one-off default)
```

**Note:** If the `S_No` field already exists in your table, the migration will handle it gracefully.

## API Endpoints Summary

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/hydroponics/api/sensors/latest/` | GET | Get latest sensor reading | Required |
| `/hydroponics/api/sensors/history/` | GET | Get all readings (stack format) | Required |
| `/hydroponics/api/sensors/ingest/` | POST | Add new sensor reading | Required |

**Authorization:** All endpoints require user authentication. Users can only access their own devices, admins can access all devices.

## Example Workflow

### Admin adds sensor readings:
1. Dashboard loads, showing live sensor data
2. Admin clicks "Add Reading" button
3. Modal shows device dropdown (auto-populated from API)
4. Admin selects device and enters readings:
   - Temperature: 25.5°C
   - Humidity: 65%
   - pH: 7.0
   - EC: 2.5
5. Clicks "Add Reading"
6. API creates new SensorValue record with auto timestamp
7. History section refreshes automatically
8. New reading appears at the top with "Latest" badge
9. Previous reading moves down with "#1" badge
10. Users can see full historical stack

### Frontend displays history:
- Latest reading: Shows "Latest" badge with green border
- Previous readings: Show "#1", "#2", etc. with gray borders
- Each reading shows full date/time and all sensor values
- Readings are ordered newest → oldest
- Total reading count displayed

## Benefits

1. **Data Preservation:** No more overwriting of sensor readings
2. **Historical Analysis:** Can track how sensor values change over time
3. **Audit Trail:** Each reading has a timestamp for verification
4. **User-Friendly:** Stack format shows latest data prominently
5. **Scalable:** Supports unlimited readings per device
6. **Real-time Updates:** Auto-refresh capability on frontend

## Testing Checklist

- [ ] Add migration and run it successfully
- [ ] Access Django admin and view SensorValue list (should show newest first)
- [ ] Add a sensor reading from admin panel
- [ ] Verify timestamp is auto-filled
- [ ] Open dashboard and see "Add Reading" button (if admin)
- [ ] Click "Add Reading" and verify device list loads
- [ ] Add a reading via modal
- [ ] Verify history section shows new reading at top
- [ ] Verify old readings are still visible below
- [ ] Verify API endpoints work via curl/Postman
- [ ] Check that users can only see their own device data
- [ ] Check that admins can see all devices
