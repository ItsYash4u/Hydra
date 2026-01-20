
import random
import time
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from greeva.hydroponics.models import UserDevice, Device, SensorReading

class Command(BaseCommand):
    help = 'Generates mock data for testing: User -> Device -> SensorReadings'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=1, help='Number of users to create')
        parser.add_argument('--devices', type=int, default=1, help='Number of devices per user')
        parser.add_argument('--readings', type=int, default=10, help='Number of readings per device')

    def handle(self, *args, **options):
        num_users = options['users']
        num_devices = options['devices']
        num_readings = options['readings']

        self.stdout.write(self.style.SUCCESS('Starting Mock Data Generation...'))

        for u_idx in range(num_users):
            user_id = f"MOCK_USER_{random.randint(1000, 9999)}"
            email = f"{user_id.lower()}@example.com"
            
            user, created = UserDevice.objects.get_or_create(
                User_ID=user_id,
                defaults={
                    'Email_ID': email,
                    'Password': 'pbkdf2_sha256$mock_hash',
                    'Role': 'user',
                    'Age': 25
                }
            )
            if created:
                self.stdout.write(f"Created User: {user.User_ID}")
            else:
                self.stdout.write(f"Using existing User: {user.User_ID}")

            for d_idx in range(num_devices):
                device_id = f"MOCK_DEV_{random.randint(10000, 99999)}"
                
                device, d_created = Device.objects.get_or_create(
                    user=user,
                    # We only create a new device if we have a guaranteed unique ID logic or just try random
                    # To effectively link to specific user, let's just create one.
                    defaults={
                       'Device_ID': device_id,
                       'Latitude': 20.0 + random.random(),
                       'Longitude': 78.0 + random.random()
                    }
                )
                
                # If get_or_create found a device by user, it doesn't guarantee Device_ID is what we want if we didn't filter by it.
                # Actually, usually we filter by Device_ID. Let's adjust.
                if not d_created:
                     # Just pick one of the user's devices if we want to append data
                     pass
                else:
                     self.stdout.write(f"  -> Created Device: {device.Device_ID}")

                # Ensure we have the device object
                if d_created:
                    target_device = device
                else:
                    # If we didn't create it (because we didn't filter by ID correctly above? No, wait.)
                    # Let's retry properly
                    target_device = Device.objects.create(
                        user=user,
                        Device_ID=device_id,
                        Latitude=20.0 + random.random(),
                        Longitude=78.0 + random.random()
                    )
                    self.stdout.write(f"  -> Created Device: {target_device.Device_ID}")
                
                # Generate Readings
                self.stdout.write(f"     Generating {num_readings} readings...")
                readings_to_create = []
                base_time = timezone.now()
                
                for r_idx in range(num_readings):
                    # Simulate slightly different times
                    timestamp = base_time - timedelta(minutes=r_idx*10)
                    
                    readings_to_create.append(SensorReading(
                        device=target_device,
                        timestamp=timestamp,
                        temperature=random.uniform(20.0, 35.0),
                        humidity=random.uniform(40.0, 90.0),
                        ph=random.uniform(5.5, 7.5),
                        ec=random.uniform(1.0, 2.5),
                        tds=random.uniform(400, 1200),
                        co2=random.uniform(400, 1000),
                        light=random.uniform(0, 100),
                        water_temp=random.uniform(18.0, 28.0),
                        dissolved_oxygen=random.uniform(4.0, 8.0)
                    ))
                
                SensorReading.objects.bulk_create(readings_to_create)
                self.stdout.write(self.style.SUCCESS(f"     Done."))
