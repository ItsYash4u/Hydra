
import random
import uuid
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from greeva.hydroponics.models_custom import UserDevice, Device, SensorValue, SensorReading

class Command(BaseCommand):
    help = 'Generates sample data for the Custom Database Schema (UserDevice, Device, SensorReading)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating Custom DB sample data...')

        # 1. Create Admin User
        admin_email = "admin@greeva.com"
        admin_user = UserDevice.objects.filter(Email_ID=admin_email).first()
        if not admin_user:
            admin_user = UserDevice(
                User_ID=f"USER-{uuid.uuid4().hex[:8].upper()}",
                Email_ID=admin_email,
                Phone="9999999999",
                Role='admin',
                Age=30
            )
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(f'Created Admin: {admin_email}')
        else:
            self.stdout.write(f'Admin exists: {admin_email}')

        # 2. Create Regular User
        user_email = "ayush@greeva.com"
        normal_user = UserDevice.objects.filter(Email_ID=user_email).first()
        if not normal_user:
            normal_user = UserDevice(
                User_ID=f"USER-{uuid.uuid4().hex[:8].upper()}",
                Email_ID=user_email,
                Phone="8888888888",
                Role='user',
                Age=25
            )
            normal_user.set_password("user123")
            normal_user.save()
            self.stdout.write(f'Created User: {user_email}')
        else:
            self.stdout.write(f'User exists: {user_email}')

        # 3. Create Devices
        devices_config = [
            {'user': admin_user, 'lat': 20.59, 'lon': 78.96},
            {'user': normal_user, 'lat': 19.07, 'lon': 72.87},
            {'user': normal_user, 'lat': 12.97, 'lon': 77.59},
        ]

        created_devices = []
        for conf in devices_config:
            u = conf['user']
            # Re-fetch to ensure PK is available
            u.refresh_from_db()
            
            # Check if user has devices
            existing = Device.objects.filter(user=u).first()
            if not existing:
                device_id = f"DEV-{uuid.uuid4().hex[:8].upper()}"
                try:
                    device = Device.objects.create(
                        user=u,
                        Device_ID=device_id,
                        Latitude=conf['lat'],
                        Longitude=conf['lon']
                    )
                    self.stdout.write(f'Created Device {device_id} for {u.Email_ID}')
                    created_devices.append(device)
                except Exception as e:
                     self.stdout.write(f"Error creating device: {e}")
            else:
                self.stdout.write(f'User {u.Email_ID} already has device {existing.Device_ID}')
                created_devices.append(existing)

        # 4. Generate Sensor Readings (High Frequency - last 1 hour)
        self.stdout.write('Generating Sensor Readings...')
        now = timezone.now()
        
        for device in created_devices:
            # Generate 60 readings (1 per minute for last hour)
            readings = []
            for i in range(60):
                timestamp = now - timedelta(minutes=i)
                
                readings.append(SensorReading(
                    device_id=device.Device_ID,
                    timestamp=timestamp,
                    temperature=random.uniform(22.0, 28.0),
                    humidity=random.uniform(50.0, 70.0),
                    ph=random.uniform(5.5, 6.5),
                    ec=random.uniform(1.0, 2.0),
                    tds=random.uniform(500, 1000),
                    co2=random.uniform(400, 800),
                    light=random.uniform(10, 16),
                    water_temp=random.uniform(20.0, 24.0),
                    dissolved_oxygen=random.uniform(6.0, 8.0)
                ))
            
            # Bulk create to save time
            SensorReading.objects.bulk_create(readings)
            self.stdout.write(f'Added 60 readings for {device.Device_ID}')
            
            # 5. Update Legacy SensorValue (Snapshot)
            latest = readings[0] # The one at 'now'
            # Check if exists for today
            today = now.date()
            sv, created = SensorValue.objects.get_or_create(
                Device_ID=device.Device_ID,
                date=today,
                defaults={
                    'temperature': latest.temperature,
                    'humidity': latest.humidity,
                    'pH': latest.ph,
                    'EC': latest.ec
                }
            )
            if not created:
                sv.temperature = latest.temperature
                sv.humidity = latest.humidity
                sv.pH = latest.ph
                sv.EC = latest.ec
                sv.save()
                
        self.stdout.write(self.style.SUCCESS('Successfully generated Custom DB sample data'))
