import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from greeva.hydroponics.models import (
    Device, Sensor, SensorReading, AlertRule, PlantProfile, UserRole
)
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates sample data for the hydroponics system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating sample data...')

        # Create Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={'name': 'Admin User', 'is_staff': True, 'is_superuser': True}
        )
        if not admin_user.check_password('password'):
            admin_user.set_password('password')
            admin_user.save()

        operator_user, _ = User.objects.get_or_create(
            email='operator@example.com',
            defaults={'name': 'Operator User'}
        )
        if not operator_user.check_password('password'):
            operator_user.set_password('password')
            operator_user.save()

        # Assign Roles
        UserRole.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})
        UserRole.objects.get_or_create(user=operator_user, defaults={'role': 'farm_operator'})

        # Create Plant Profiles
        lettuce, _ = PlantProfile.objects.get_or_create(
            name='Lettuce (Butterhead)',
            defaults={
                'description': 'Popular hydroponic crop, fast growing.',
                'growth_stage_days': 45,
                'ideal_temperature_min': 18.0,
                'ideal_temperature_max': 24.0,
                'ideal_ph_min': 5.5,
                'ideal_ph_max': 6.5,
                'ideal_humidity_min': 50.0,
                'ideal_humidity_max': 70.0,
                'ideal_moisture_min': 60.0,
                'ideal_moisture_max': 80.0,
                'ideal_light_hours': 14,
                'nitrogen_ppm': 150.0,
                'phosphorus_ppm': 50.0,
                'potassium_ppm': 200.0,
            }
        )

        tomato, _ = PlantProfile.objects.get_or_create(
            name='Tomato (Cherry)',
            defaults={
                'description': 'Requires higher nutrients and light.',
                'growth_stage_days': 90,
                'ideal_temperature_min': 20.0,
                'ideal_temperature_max': 28.0,
                'ideal_ph_min': 5.5,
                'ideal_ph_max': 6.5,
                'ideal_humidity_min': 60.0,
                'ideal_humidity_max': 80.0,
                'ideal_moisture_min': 60.0,
                'ideal_moisture_max': 80.0,
                'ideal_light_hours': 16,
                'nitrogen_ppm': 200.0,
                'phosphorus_ppm': 100.0,
                'potassium_ppm': 300.0,
            }
        )

        # Create Devices
        devices = []
        device_configs = [
            {
                'name': 'Greenhouse A',
                'location': 'Zone 1',
                'device_type': 'greenhouse',
                'sensor_id': 'GH-001',
                'state': 'Maharashtra',
                'region': 'Pune'
            },
            {
                'name': 'Aquaponic Tank B',
                'location': 'Zone 2',
                'device_type': 'aquaponic_tank',
                'sensor_id': 'AQ-001',
                'state': 'Maharashtra',
                'region': 'Mumbai'
            }
        ]

        for config in device_configs:
            device, created = Device.objects.get_or_create(
                sensor_id=config['sensor_id'],
                defaults={
                    'name': config['name'],
                    'location': config['location'],
                    'device_type': config['device_type'],
                    'state': config['state'],
                    'region': config['region'],
                    'owner': admin_user
                }
            )
            devices.append(device)
            if created:
                self.stdout.write(f'Created device: {device.name}')

        # Create Sensors and Readings
        sensor_types = [
            ('temperature', 20.0, 30.0),
            ('ph', 5.5, 7.5),
            ('humidity', 40.0, 80.0),
            ('moisture', 50.0, 90.0),
            ('light_hours', 0.0, 24.0),
            ('conductivity', 1.0, 3.0)
        ]

        now = timezone.now()
        
        for device in devices:
            for s_type, min_val, max_val in sensor_types:
                sensor, created = Sensor.objects.get_or_create(
                    device=device,
                    sensor_type=s_type,
                    defaults={
                        'min_threshold': min_val,
                        'max_threshold': max_val,
                        'alert_enabled': True
                    }
                )
                
                # Generate readings for the last 24 hours (every hour)
                if created or not SensorReading.objects.filter(sensor=sensor).exists():
                    readings = []
                    for i in range(24):
                        timestamp = now - timedelta(hours=i)
                        # Add some randomness
                        value = random.uniform(min_val, max_val)
                        readings.append(SensorReading(
                            sensor=sensor,
                            value=round(value, 2),
                            timestamp=timestamp
                        ))
                    SensorReading.objects.bulk_create(readings)
                    self.stdout.write(f'Generated readings for {sensor}')

                # Create Alert Rule
                AlertRule.objects.get_or_create(
                    device=device,
                    sensor_type=s_type,
                    defaults={
                        'min_value': min_val,
                        'max_value': max_val,
                        'severity': 'medium',
                        'enabled': True
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
