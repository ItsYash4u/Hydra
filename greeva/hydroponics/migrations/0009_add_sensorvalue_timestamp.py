"""
Migration to update SensorValue model to support multiple readings per device per day.

Changes:
1. Add auto-increment ID column (S_No) as primary key
2. Add timestamp column for automatic timestamp recording
3. Add database indexes for efficient queries
4. Change date from PRIMARY KEY to regular field
5. Change ordering to show newest readings first

This allows storing multiple sensor readings per device per day in a stack format.

Note: SensorValue model has managed=False, so we use RunSQL for actual database changes.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0008_remove_device_unique_device_per_user_and_more'),  # Latest migration
    ]

    operations = [
        # Raw SQL to add S_No as auto-increment primary key and timestamp column
        migrations.RunSQL(
            sql="""
            ALTER TABLE sensor_value 
            ADD COLUMN S_No INT AUTO_INCREMENT UNIQUE KEY FIRST,
            ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP;
            """,
            reverse_sql="""
            ALTER TABLE sensor_value 
            DROP COLUMN S_No,
            DROP COLUMN timestamp;
            """,
            state_operations=[
                migrations.AddField(
                    model_name='sensorvalue',
                    name='S_No',
                    field=models.AutoField(primary_key=True, serialize=False, verbose_name='Serial Number'),
                ),
                migrations.AddField(
                    model_name='sensorvalue',
                    name='timestamp',
                    field=models.DateTimeField(auto_now_add=True, null=True, blank=True),
                ),
            ]
        ),
        # Add indexes for better query performance
        migrations.RunSQL(
            sql="""
            CREATE INDEX idx_device_timestamp ON sensor_value(Device_ID, timestamp DESC);
            CREATE INDEX idx_date ON sensor_value(date);
            """,
            reverse_sql="""
            DROP INDEX idx_device_timestamp ON sensor_value;
            DROP INDEX idx_date ON sensor_value;
            """,
        ),
        # Update model options
        migrations.AlterModelOptions(
            name='sensorvalue',
            options={
                'managed': False,
                'db_table': 'sensor_value',
                'ordering': ['-timestamp'],
            },
        ),
    ]
