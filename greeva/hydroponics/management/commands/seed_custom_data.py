
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from greeva.hydroponics.models_custom import UserDevice, Device, SensorValue

class Command(BaseCommand):
    help = 'Seeds custom data for UserDevice, Device, and SensorValue'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Custom Data...")

        # 1. Create or Get UserDevice
        user, created = UserDevice.objects.get_or_create(
            User_ID='admin_user',
            defaults={
                'Email_ID': 'admin@greeva.com',
                'Password': 'pbkdf2_sha256$260000$checksum', # dummy hash
                'Role': 'admin',
                'Phone': '1234567890',
                'Age': 30
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created UserDevice: {user.User_ID}"))
        else:
            self.stdout.write(f"UserDevice {user.User_ID} already exists.")

        # 2. Create or Get Device
        device_id = 'HYDRO-SYS-01'
        device, created = Device.objects.get_or_create(
            Device_ID=device_id,
            defaults={
                'user': user,
                'Latitude': 28.6139,
                'Longitude': 77.2090
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Device: {device.Device_ID} linked to {user.User_ID}"))
        else:
            # Ensure it is linked to the user (fix bad links)
            if device.user != user:
                device.user = user
                device.save()
                self.stdout.write(self.style.WARNING(f"Fixed Device {device.Device_ID} linkage."))
            else:
               self.stdout.write(f"Device {device.Device_ID} already exists.")

        # 3. Create Sensor Values (Last 7 days)
        # Note: SensorValue is unmanaged, so we assume the table exists. 
        # If we can't write to it (e.g. permission or missing), we catch error.
        try:
            # Check if any data exists for today
            today = timezone.now().date()
            if not SensorValue.objects.filter(device_id=device_id, date=today).exists():
                SensorValue.objects.create(
                    device_id=device_id,
                    date=today,
                    temperature=24.5,
                    humidity=60.0,
                    pH=6.5,
                    EC=1.2
                )
                self.stdout.write(self.style.SUCCESS(f"Created SensorValue for {today}"))
            
            # Create a few history points
            for i in range(1, 5):
                d = today - timedelta(days=i)
                if not SensorValue.objects.filter(device_id=device_id, date=d).exists():
                    SensorValue.objects.create(
                        device_id=device_id,
                        date=d,
                        temperature=24.0 + random.uniform(-1, 1),
                        humidity=60.0 + random.uniform(-5, 5),
                        pH=6.5 + random.uniform(-0.2, 0.2),
                        EC=1.2 + random.uniform(-0.1, 0.1)
                    )
                    self.stdout.write(f"Created history for {d}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not write SensorValue (might be read-only view?): {e}"))

        self.stdout.write(self.style.SUCCESS("Seeding Completed Successfully."))
