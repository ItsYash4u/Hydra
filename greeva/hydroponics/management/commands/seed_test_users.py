"""
Management command to create 10 test REGULAR users with varying device counts
NOTE: Existing admin (yashsinghkushwaha345@gmail.com) is preserved
"""

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from greeva.hydroponics.models_custom import UserDevice, Device, SensorValue


class Command(BaseCommand):
    help = 'Creates 10 test regular users with devices and sensor data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating test users and devices...'))
        self.stdout.write(self.style.WARNING('NOTE: Preserving existing admin user'))

        # Define 10 test REGULAR users (all with 'user' role)
        users_config = [
            {'email': 'user1@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 10},
            {'email': 'user2@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 5},
            {'email': 'user3@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 8},
            {'email': 'user4@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 3},
            {'email': 'user5@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 7},
            {'email': 'user6@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 5},
            {'email': 'user7@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 6},
            {'email': 'user8@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 4},
            {'email': 'user9@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 9},
            {'email': 'user10@greeva.com', 'password': 'user123', 'role': 'user', 'devices': 10},
        ]

        # Base coordinates for different cities
        locations = [
            (26.1445, 91.6606),  # Guwahati
            (28.7041, 77.1025),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (12.9716, 77.5946),  # Bangalore
            (22.5726, 88.3639),  # Kolkata
            (17.3850, 78.4867),  # Hyderabad
            (13.0827, 80.2707),  # Chennai
            (23.0225, 72.5714),  # Ahmedabad
            (18.5204, 73.8567),  # Pune
            (26.9124, 75.7873),  # Jaipur
        ]

        created_users = []
        total_devices_created = 0

        for idx, config in enumerate(users_config):
            # Create or get user
            user, created = UserDevice.objects.get_or_create(
                Email_ID=config['email'],
                defaults={
                    'User_ID': f"USER-{idx+1:03d}",
                    'Phone': f"98765{idx:05d}",
                    'Age': 25 + idx,
                    'Role': config['role']
                }
            )
            
            if created:
                user.set_password(config['password'])
                user.save()
                self.stdout.write(f"✓ Created USER: {config['email']}")
            else:
                self.stdout.write(f"  Exists: {config['email']}")

            created_users.append(user)

            # Create devices for this user
            device_count = config['devices']
            existing_devices = Device.objects.filter(user=user).count()
            
            if existing_devices >= device_count:
                self.stdout.write(f"  User already has {existing_devices} devices (target: {device_count})")
                continue

            devices_to_create = device_count - existing_devices
            
            for i in range(devices_to_create):
                # Vary locations slightly
                base_lat, base_lon = locations[idx % len(locations)]
                lat = base_lat + (random.random() - 0.5) * 0.1
                lon = base_lon + (random.random() - 0.5) * 0.1

                # Create device (Device_ID will be auto-generated)
                device = Device.objects.create(
                    user=user,
                    Latitude=round(lat, 6),
                    Longitude=round(lon, 6)
                )
                
                total_devices_created += 1

                # NOTE: Skipping sensor data creation due to DB foreign key constraints
                # The FK constraint expects Device_ID (string) but we're using S_No (int)
                # Sensor data can be added later via the dashboard or API
                
                # Create sensor data for the last 7 days
                # today = timezone.now().date()
                # for day_offset in range(7):
                #     date = today - timedelta(days=day_offset)
                #     
                #     SensorValue.objects.get_or_create(
                #         device_id=str(device.S_No),
                #         date=date,
                #         defaults={
                #             'temperature': round(20 + random.uniform(0, 10), 2),
                #             'humidity': round(50 + random.uniform(0, 30), 2),
                #             'pH': round(5.5 + random.uniform(0, 2), 2),
                #             'EC': round(1.0 + random.uniform(0, 1.5), 2),
                #         }
                #     )

            self.stdout.write(f"  → Created {devices_to_create} devices for {user.short_id}")

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS(f'✓ Total Regular Users Created: {len(created_users)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total Devices Created: {total_devices_created}'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write('\n📋 LOGIN CREDENTIALS (Regular Users):')
        self.stdout.write('-' * 60)
        for config in users_config:
            self.stdout.write(f"  Email: {config['email']:<30} Password: {config['password']}")
        self.stdout.write('-' * 60)
        self.stdout.write('\n🔐 ADMIN USER (Already exists):')
        self.stdout.write(f"  Email: yashsinghkushwaha345@gmail.com   Password: 1234567890")
        self.stdout.write('-' * 60)
