import random
import datetime
from django.core.management.base import BaseCommand
from greeva.users.models import UserDevice
from greeva.hydroponics.models import Device, SensorValue
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds database with UserDevice, Device, and SensorValue data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding UserDevice data...')
        
        # Create Admin
        admin_email = "admin@hydroponics.local"
        if not UserDevice.objects.filter(Email_ID=admin_email).exists():
            UserDevice.objects.create(
                User_ID="USR-ADMIN-001",
                Email_ID=admin_email,
                Password="hashed_password_placeholder", # In real app, hash this
                Role="admin",
                Phone="1234567890",
                Age=30
            )
            self.stdout.write(f'Created Admin: {admin_email}')

        # Create Normal Users
        for i in range(5):
             email = f"user{i}@test.com"
             if not UserDevice.objects.filter(Email_ID=email).exists():
                 user = UserDevice.objects.create(
                     User_ID=f"USR-{random.randint(1000,9999)}",
                     Email_ID=email,
                     Password="hashed_password_placeholder",
                     Role="user",
                     Phone=f"9876543{i}00",
                     Age=random.randint(20, 50)
                 )
                 self.seed_devices(user)
        
        self.stdout.write(self.style.SUCCESS('Seeding Complete.'))

    def seed_devices(self, user):
        for j in range(random.randint(7, 10)):
            device_id = f"DEV-{user.User_ID}-{j}"
            if not Device.objects.filter(Device_ID=device_id).exists():
                device = Device.objects.create(
                    User_ID=user,
                    Device_ID=device_id,
                    Latitude=20.59 + random.uniform(-5, 5),
                    Longitude=78.96 + random.uniform(-5, 5)
                )
                self.seed_sensor_values(device)

    def seed_sensor_values(self, device):
        # Create multiple readings
        for k in range(5):
            now = timezone.now() - datetime.timedelta(hours=k)
            SensorValue.objects.create(
                Device_ID=device,
                Date=now.date(),
                Time=now.time(),
                Temperature=round(random.uniform(20, 30), 1),
                pH=round(random.uniform(5.5, 7.5), 1),
                EC=round(random.uniform(1.0, 2.5), 1),
                Humidity=round(random.uniform(40, 80), 1),
                Nitrogen=random.uniform(100, 200),
                Phosphorus=random.uniform(30, 80),
                Potassium=random.uniform(100, 300)
            )
