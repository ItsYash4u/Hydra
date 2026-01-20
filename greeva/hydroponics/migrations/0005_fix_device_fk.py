
from django.db import migrations

def fix_foreign_key(apps, schema_editor):
    """
    Drop the incorrect FK constraint and add the correct one
    """
    with schema_editor.connection.cursor() as cursor:
        # Drop old constraint
        try:
            cursor.execute("ALTER TABLE device DROP FOREIGN KEY fk_device_user")
        except Exception:
            pass  # Might not exist
            
        # Add correct constraint
        cursor.execute("""
            ALTER TABLE device 
            ADD CONSTRAINT fk_device_user 
            FOREIGN KEY (User_ID) 
            REFERENCES userdevice (User_ID) 
            ON DELETE CASCADE
        """)

class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0004_alter_sensorvalue_options_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_foreign_key, reverse_code=migrations.RunPython.noop),
    ]
