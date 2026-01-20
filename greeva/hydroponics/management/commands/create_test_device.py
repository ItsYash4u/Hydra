"""
Management command to create test device
"""
from django.core.management.base import BaseCommand
from hydroponics.models_custom import Device, UserDevice


class Command(BaseCommand):
    help = 'Creates a test device for sensor value testing'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("CREATING TEST DEVICE")
        self.stdout.write("=" * 70)
        
        # Get or create user
        user, created = UserDevice.objects.get_or_create(
            User_ID='test_user',
            defaults={
                'Email_ID': 'test@example.com',
                'Phone': '1234567890',
                'Age': 25,
                'Role': 'user'
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created user: {user.User_ID}'))
        else:
            self.stdout.write(f'✓ Using existing user: {user.User_ID}')
        
        # Get or create device
        device, created = Device.objects.get_or_create(
            Device_ID='DEVICE_TEST_001',
            defaults={
                'user': user,
                'Latitude': 28.6139,
                'Longitude': 77.2090
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created device: {device.Device_ID}'))
        else:
            self.stdout.write(f'✓ Device already exists: {device.Device_ID}')
        
        # Summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(f"Total Users: {UserDevice.objects.count()}")
        self.stdout.write(f"Total Devices: {Device.objects.count()}")
        self.stdout.write(self.style.SUCCESS('\n✅ You can now add sensor values!'))
        self.stdout.write("=" * 70)
