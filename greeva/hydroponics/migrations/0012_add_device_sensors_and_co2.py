from django.db import migrations, models


def add_missing_columns(apps, schema_editor):
    conn = schema_editor.connection
    vendor = conn.vendor

    def column_exists(table, column):
        with conn.cursor() as cursor:
            if vendor == "sqlite":
                cursor.execute(f"PRAGMA table_info({table});")
                return column in [row[1] for row in cursor.fetchall()]
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                  AND COLUMN_NAME = %s
                """,
                [table, column],
            )
            return cursor.fetchone()[0] > 0

    def index_exists(table, index_name):
        with conn.cursor() as cursor:
            if vendor == "sqlite":
                cursor.execute(f"PRAGMA index_list({table});")
                return index_name in [row[1] for row in cursor.fetchall()]
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                  AND INDEX_NAME = %s
                """,
                [table, index_name],
            )
            return cursor.fetchone()[0] > 0

    # Device table columns
    if not column_exists("device", "Device_Name"):
        schema_editor.execute("ALTER TABLE device ADD COLUMN Device_Name VARCHAR(100) NULL")
    if not column_exists("device", "Device_Sensors"):
        schema_editor.execute("ALTER TABLE device ADD COLUMN Device_Sensors TEXT NULL")
    if not column_exists("device", "Device_Type"):
        schema_editor.execute("ALTER TABLE device ADD COLUMN Device_Type VARCHAR(10) NOT NULL DEFAULT 'AIR'")
    if not column_exists("device", "Registration_Status"):
        schema_editor.execute(
            "ALTER TABLE device ADD COLUMN Registration_Status VARCHAR(20) NOT NULL DEFAULT 'REGISTERED'"
        )
    if not column_exists("device", "Registered_At"):
        schema_editor.execute("ALTER TABLE device ADD COLUMN Registered_At DATETIME NULL")

    if not index_exists("device", "idx_device_type"):
        if vendor == "sqlite":
            schema_editor.execute("CREATE INDEX IF NOT EXISTS idx_device_type ON device (Device_Type)")
        else:
            schema_editor.execute("CREATE INDEX idx_device_type ON device (Device_Type)")

    # Sensor value columns
    if not column_exists("sensor_value", "CO2"):
        schema_editor.execute("ALTER TABLE sensor_value ADD COLUMN CO2 FLOAT NULL")
    if not column_exists("sensor_value", "timestamp"):
        schema_editor.execute(
            "ALTER TABLE sensor_value ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
        )

    if not index_exists("sensor_value", "idx_device_timestamp"):
        if vendor == "sqlite":
            schema_editor.execute(
                "CREATE INDEX IF NOT EXISTS idx_device_timestamp ON sensor_value (Device_ID, timestamp)"
            )
        else:
            schema_editor.execute(
                "CREATE INDEX idx_device_timestamp ON sensor_value (Device_ID, timestamp)"
            )

    if not index_exists("sensor_value", "idx_sensor_date"):
        if vendor == "sqlite":
            schema_editor.execute("CREATE INDEX IF NOT EXISTS idx_sensor_date ON sensor_value (date)")
        else:
            schema_editor.execute("CREATE INDEX idx_sensor_date ON sensor_value (date)")


class Migration(migrations.Migration):

    dependencies = [
        ("hydroponics", "0011_device_type_and_global_device_id"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_missing_columns, reverse_code=migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="device",
                    name="Device_Sensors",
                    field=models.TextField(blank=True, null=True, verbose_name="Device Sensors"),
                ),
                migrations.AddField(
                    model_name="sensorvalue",
                    name="CO2",
                    field=models.FloatField(blank=True, null=True, db_column="CO2"),
                ),
            ],
        ),
    ]
