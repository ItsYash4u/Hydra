-- Safe MySQL migration for device + sensor_value fields
-- Runs idempotently using information_schema checks.

-- device.Device_Name
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND COLUMN_NAME = 'Device_Name'
);
SET @sql := IF(@col = 0,
    'ALTER TABLE device ADD COLUMN Device_Name VARCHAR(100) NULL',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- device.Device_Sensors
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND COLUMN_NAME = 'Device_Sensors'
);
SET @sql := IF(@col = 0,
    'ALTER TABLE device ADD COLUMN Device_Sensors TEXT NULL',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- device.Device_Type
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND COLUMN_NAME = 'Device_Type'
);
SET @sql := IF(@col = 0,
    "ALTER TABLE device ADD COLUMN Device_Type VARCHAR(10) NOT NULL DEFAULT 'AIR'",
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- device.Registration_Status
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND COLUMN_NAME = 'Registration_Status'
);
SET @sql := IF(@col = 0,
    "ALTER TABLE device ADD COLUMN Registration_Status VARCHAR(20) NOT NULL DEFAULT 'REGISTERED'",
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- device.Registered_At
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND COLUMN_NAME = 'Registered_At'
);
SET @sql := IF(@col = 0,
    "ALTER TABLE device ADD COLUMN Registered_At DATETIME NULL",
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- device.Device_Type index
SET @idx := (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'device'
      AND INDEX_NAME = 'idx_device_type'
);
SET @sql := IF(@idx = 0,
    'CREATE INDEX idx_device_type ON device (Device_Type)',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- sensor_value.CO2
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'sensor_value'
      AND COLUMN_NAME = 'CO2'
);
SET @sql := IF(@col = 0,
    'ALTER TABLE sensor_value ADD COLUMN CO2 FLOAT NULL',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- sensor_value.timestamp
SET @col := (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'sensor_value'
      AND COLUMN_NAME = 'timestamp'
);
SET @sql := IF(@col = 0,
    'ALTER TABLE sensor_value ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- sensor_value index on (Device_ID, timestamp)
SET @idx := (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'sensor_value'
      AND INDEX_NAME = 'idx_device_timestamp'
);
SET @sql := IF(@idx = 0,
    'CREATE INDEX idx_device_timestamp ON sensor_value (Device_ID, timestamp)',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- sensor_value index on date
SET @idx := (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'sensor_value'
      AND INDEX_NAME = 'idx_sensor_date'
);
SET @sql := IF(@idx = 0,
    'CREATE INDEX idx_sensor_date ON sensor_value (date)',
    'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
