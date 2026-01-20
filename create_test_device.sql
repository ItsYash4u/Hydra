-- ============================================================================
-- SQL Script to Create Test Device
-- Run this in MySQL Workbench to fix the sensor value error
-- ============================================================================

USE greeva;

-- Check current state
SELECT 'Current Users:' AS Info, COUNT(*) AS Count FROM userdevice;
SELECT 'Current Devices:' AS Info, COUNT(*) AS Count FROM device;

-- Create a test user if none exists
INSERT IGNORE INTO userdevice (User_ID, Email_ID, Password, Phone, Age, Role, Created_At, Updated_At)
VALUES ('test_user', 'test@example.com', 'pbkdf2_sha256$600000$test$hash', '1234567890', 25, 'user', NOW(), NOW());

-- Get the User_ID (in case there's already a user)
SET @user_id = (SELECT User_ID FROM userdevice LIMIT 1);

-- Create a test device
INSERT IGNORE INTO device (User_ID, Device_ID, Latitude, Longitude, Created_At, Updated_At)
VALUES (@user_id, 'DEVICE_TEST_001', 28.6139, 77.2090, NOW(), NOW());

-- Verify creation
SELECT 'Final Users:' AS Info, COUNT(*) AS Count FROM userdevice;
SELECT 'Final Devices:' AS Info, COUNT(*) AS Count FROM device;
SELECT 'Available Devices:' AS Info, Device_ID, User_ID FROM device;

-- ============================================================================
-- SUCCESS! You can now add sensor values in Django admin
-- Go to: http://127.0.0.1:8000/admin/hydroponics/sensorvalue/add/
-- ============================================================================
