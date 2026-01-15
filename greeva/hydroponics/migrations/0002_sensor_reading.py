# Generated manually by Agent

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device_id', models.CharField(db_index=True, max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('ph', models.FloatField(blank=True, null=True)),
                ('ec', models.FloatField(blank=True, null=True)),
                ('tds', models.FloatField(blank=True, null=True)),
                ('co2', models.FloatField(blank=True, null=True)),
                ('light', models.FloatField(blank=True, null=True)),
                ('water_temp', models.FloatField(blank=True, null=True)),
                ('dissolved_oxygen', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sensor_reading',
                'ordering': ['-timestamp'],
                'indexes': [
                    models.Index(fields=['device_id', '-timestamp'], name='sensor_read_device__d5c8e2_idx'),
                ],
            },
        ),
    ]
