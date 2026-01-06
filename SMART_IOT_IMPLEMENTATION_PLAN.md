# Smart IoT Hydroponics Dashboard - Implementation Plan

## Overview
Transform the Greeva template into a production-ready Smart IoT Hydroponics frontend with multi-device support, real-time sensor monitoring, analytics, and mapping.

## Base Rules Compliance
✅ Using ONLY Greeva Admin Template as frontend base
✅ Preserving sidebar, navbar, card, table, and grid components
✅ Dark/light theme depends on Greeva's theme toggle
✅ All improvements native to Greeva

## Implementation Checklist

### 1. Sidebar Navigation ✅ (Already Complete)
- [x] Dashboard
- [x] Analytics
- [x] Map
- Located in: `greeva/templates/partials/sidenav.html`

### 2. User Roles & Data Visibility
- [x] Admin Dashboard - Views all devices
- [x] User Dashboard - Views only own devices
- Located in: `greeva/hydroponics/views.py`
- Session-based authentication via `get_current_user()`

### 3. Dashboard Page Layout

#### 3.1 Header Section
**Current Status:** Partially implemented
**Location:** `greeva/templates/pages/index.html` (lines 20-44)
**Tasks:**
- [ ] Update header to show "Smart IoT" (currently shows "Smart I O T")
- [ ] Add dynamic "Live Sensor Data (Device ID: XXXX)" below header
- [ ] Make device ID update when device selection changes

#### 3.2 Live Sensor Monitor (Draggable Grid)
**Current Status:** Static grid implemented
**Location:** `greeva/templates/pages/index.html` (lines 100-146)
**Tasks:**
- [ ] Add drag-and-drop functionality using SortableJS or GridStack
- [ ] Implement user-specific layout persistence (localStorage or backend)
- [ ] Add "Add Sensor" functionality
- [ ] Add "Remove Sensor" functionality
- [ ] Implement auto-refresh every 5-7 seconds
- [ ] Add additional sensors:
  - [x] Water Temperature
  - [x] pH
  - [x] EC
  - [ ] Water Flow
  - [ ] Water Level
  - [x] Air Temperature (Humidity exists)
  - [x] Air Humidity
  - [ ] CO₂
  - [ ] VPD (Vapor Pressure Deficit)

#### 3.3 Multi-Device Selector
**Current Status:** Not implemented
**Tasks:**
- [ ] Create device selector UI below "Live Sensor Data"
- [ ] Display user's devices as clickable cards/buttons
- [ ] Highlight active device
- [ ] Update sensor data when device is clicked
- [ ] Update Device ID in header

#### 3.4 View Analytics Action
**Current Status:** Not implemented
**Location:** `greeva/templates/pages/index.html` (Registered Devices table, lines 148-188)
**Tasks:**
- [ ] Add "Action" column to Registered Devices table
- [ ] Add "View Analytics" button in each row
- [ ] Link to Analytics page with device_id parameter
- [ ] Ensure role-based visibility

### 4. Analytics Page

#### 4.1 Add Device Option
**Current Status:** Modal exists in `dashboard-interactions.js`
**Location:** `greeva/static/js/dashboard-interactions.js` (lines 214-328)
**Tasks:**
- [ ] Move "Add Device" button to Analytics page top-right
- [ ] Update modal to include User ID field (admin only)
- [ ] Create backend endpoint `/api/devices/add-device/`
- [ ] Implement device attachment logic

#### 4.2 Analytics Content
**Current Status:** Basic chart implemented
**Location:** `greeva/templates/pages/analytics.html`
**Tasks:**
- [ ] Enhance time-series graphs
- [ ] Add multiple sensor lines with legends
- [ ] Implement time filters (1h, 6h, 24h, full)
- [ ] Show device-specific analytics clearly
- [ ] Add color indicators

### 5. Environment Trends (Weather Integration)
**Current Status:** Not implemented
**Tasks:**
- [ ] Add "Environment Trends" section to Dashboard
- [ ] Integrate Google Weather API or equivalent
- [ ] Fetch weather based on device lat/long
- [ ] Display graphs for:
  - [ ] Temperature
  - [ ] Wind speed
  - [ ] Humidity
- [ ] Add clear labels and markers

### 6. Device Health Section
**Current Status:** Not implemented
**Tasks:**
- [ ] Create rectangular flow-style visualization
- [ ] Add health indicators:
  - [ ] Online/Offline status
  - [ ] Sensor fault detection
  - [ ] Data delay warnings
- [ ] Ensure professional, enterprise-grade design

### 7. Map Page
**Current Status:** Implemented with Leaflet
**Location:** `greeva/templates/pages/map.html`
**Tasks:**
- [x] Display device locations using lat/long
- [x] Color-coded badges (status-based)
- [x] Role-based filtering (admin sees all, users see own)
- [ ] Enhance marker popups
- [ ] Add clustering for many devices

### 8. Tables and UI Quality
**Current Status:** Using Greeva components
**Tasks:**
- [ ] Add pagination to Registered Devices table if needed
- [ ] Ensure responsive design
- [ ] Verify professional appearance
- [ ] Test alignment and spacing

### 9. Styling and UX
**Tasks:**
- [ ] Review all CSS for Greeva compliance
- [ ] Ensure good contrast and readability
- [ ] Maintain clean hierarchy
- [ ] Add smooth transitions where appropriate

### 10. Technical Implementation

#### Backend APIs Needed
- [ ] `/api/devices/add-device/` - Add new device
- [ ] `/hydroponics/api/latest/<device_id>/` - Get latest sensor data (exists)
- [ ] `/api/devices/<device_id>/analytics/` - Get analytics data
- [ ] `/api/weather/<lat>/<lon>/` - Get weather data
- [ ] `/api/devices/<device_id>/health/` - Get device health

#### Frontend JavaScript Files
- [x] `dashboard-interactions.js` - Sensor popups, add device modal
- [ ] `dashboard-device-selector.js` - NEW: Multi-device selection
- [ ] `dashboard-draggable-grid.js` - NEW: Drag-and-drop sensor grid
- [ ] `analytics-charts.js` - Enhanced analytics charts
- [ ] `weather-integration.js` - NEW: Weather API integration

#### Database Models (Already Implemented)
- [x] UserDevice - Custom user table
- [x] Device - Device information with lat/long
- [x] SensorValue - Sensor readings

## File Structure

```
greeva/
├── templates/
│   ├── pages/
│   │   ├── index.html (Dashboard) - MODIFY
│   │   ├── analytics.html - MODIFY
│   │   └── map.html - ENHANCE
│   └── partials/
│       └── sidenav.html - ✅ Complete
├── static/
│   └── js/
│       ├── dashboard-interactions.js - MODIFY
│       ├── dashboard-device-selector.js - CREATE
│       ├── dashboard-draggable-grid.js - CREATE
│       ├── analytics-charts.js - CREATE
│       └── weather-integration.js - CREATE
├── hydroponics/
│   ├── views.py - MODIFY
│   ├── api_views.py - MODIFY
│   └── models_custom.py - ✅ Complete
└── pages/
    └── views.py - MODIFY
```

## Priority Order

### Phase 1: Core Dashboard Functionality
1. Fix header to show "Smart IoT" properly
2. Implement multi-device selector
3. Add dynamic Device ID display
4. Add "View Analytics" button to device table

### Phase 2: Enhanced Sensor Monitoring
5. Add missing sensors (Water Flow, Water Level, CO₂, VPD)
6. Implement draggable sensor grid
7. Add sensor add/remove functionality
8. Implement auto-refresh

### Phase 3: Analytics Enhancement
9. Move "Add Device" to Analytics page
10. Enhance analytics charts
11. Add time filters
12. Improve device selection UI

### Phase 4: Additional Features
13. Implement Environment Trends (Weather)
14. Create Device Health section
15. Enhance Map page
16. Add pagination where needed

### Phase 5: Polish & Testing
17. Review all styling for Greeva compliance
18. Test role-based visibility
19. Ensure responsive design
20. Performance optimization

## Success Criteria
- ✅ Sidebar has exactly 3 items: Dashboard, Analytics, Map
- ✅ Admin sees all devices, users see only their own
- ✅ Dashboard shows "Smart IoT" header
- ✅ Live sensor data updates dynamically
- ✅ Multi-device selection works smoothly
- ✅ Draggable sensor grid with persistence
- ✅ "View Analytics" button in device table
- ✅ Analytics page shows device-specific data
- ✅ Map shows devices with role-based filtering
- ✅ All UI matches Greeva design system
- ✅ No external UI libraries (except necessary for drag-drop)
- ✅ Production-ready code quality
