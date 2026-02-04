"""
Django management command to set realistic locations and sensor data
- Groups each user's devices in nearby locations
- Sets some devices offline
- Generates sensor data for online devices
"""
from django.core.management.base import BaseCommand
from greeva.hydroponics.models_custom import Device, UserDevice, SensorValue
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Setup realistic device locations and sensor data'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("SETTING UP REALISTIC DEVICE DATA")
        self.stdout.write("=" * 80)

        # Define different regions for different users (Indian cities)
        regions = [
            {"name": "Delhi NCR", "base_lat": 28.6139, "base_lon": 77.2090},
            {"name": "Mumbai", "base_lat": 19.0760, "base_lon": 72.8777},
            {"name": "Bangalore", "base_lat": 12.9716, "base_lon": 77.5946},
            {"name": "Hyderabad", "base_lat": 17.3850, "base_lon": 78.4867},
            {"name": "Chennai", "base_lat": 13.0827, "base_lon": 80.2707},
            {"name": "Kolkata", "base_lat": 22.5726, "base_lon": 88.3639},
            {"name": "Pune", "base_lat": 18.5204, "base_lon": 73.8567},
        ]

        # Get all users
        all_users = list(UserDevice.objects.filter(Role='user').order_by('User_ID'))
        
        self.stdout.write(f"\nTotal Users: {len(all_users)}")
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("ASSIGNING LOCATIONS BY REGION")
        self.stdout.write("=" * 80)

        for idx, user in enumerate(all_users):
            # Assign a region to this user
            region = regions[idx % len(regions)]
            
            # Get all devices for this user
            user_devices = Device.objects.filter(user=user).order_by('Device_ID')
            
            self.stdout.write(f"\n{user.User_ID} - {region['name']}")
            self.stdout.write(f"  Base Location: ({region['base_lat']:.4f}, {region['base_lon']:.4f})")
            
            # Update each device with nearby location
            for device_idx, device in enumerate(user_devices):
                # Add small random offset to create nearby locations
                # Offset range: ±0.05 degrees (~5km variation)
                lat_offset = random.uniform(-0.05, 0.05)
                lon_offset = random.uniform(-0.05, 0.05)
                
                device.Latitude = region['base_lat'] + lat_offset
                device.Longitude = region['base_lon'] + lon_offset
                device.save(update_fields=['Latitude', 'Longitude'])
                
                self.stdout.write(
                    f"    {device.Device_ID}: ({device.Latitude:.4f}, {device.Longitude:.4f})"
                )

        # Mark some devices as offline (30% offline rate)
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SETTING DEVICE STATUS (ONLINE/OFFLINE)")
        self.stdout.write("=" * 80)

        all_devices = list(Device.objects.all())
        offline_count = int(len(all_devices) * 0.3)  # 30% offline
        
        # Randomly select devices to be offline
        offline_devices = random.sample(all_devices, offline_count)
        offline_device_ids = [d.Device_ID for d in offline_devices]
        
        online_devices = [d for d in all_devices if d not in offline_devices]
        
        self.stdout.write(f"\nTotal Devices: {len(all_devices)}")
        self.stdout.write(f"Online Devices: {len(online_devices)}")
        self.stdout.write(f"Offline Devices: {len(offline_devices)}")
        self.stdout.write(f"\nOffline Device IDs: {', '.join(offline_device_ids)}")

        # Generate sensor data for ONLINE devices only
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("GENERATING SENSOR DATA (ONLINE DEVICES ONLY)")
        self.stdout.write("=" * 80)

        # Delete old sensor data
        deleted_count = SensorValue.objects.all().delete()[0]
        self.stdout.write(f"\nDeleted {deleted_count} old sensor records")

        # Generate data for last 7 days
        now = timezone.now()
        
        for device in online_devices:
            # Generate 7 days of hourly data
            records_created = 0
            
            for day in range(7):
                for hour in range(0, 24, 3):  # Every 3 hours
                    timestamp = now - timedelta(days=day, hours=hour)
                    
                    # Generate realistic sensor values
                    temperature = round(random.uniform(20.0, 35.0), 2)
                    humidity = round(random.uniform(40.0, 80.0), 2)
                    ph = round(random.uniform(5.5, 7.5), 2)
                    ec = round(random.uniform(1.0, 3.0), 2)
                    
                    SensorValue.objects.create(
                        device_id=device.Device_ID,
                        date=timestamp,
                        temperature=temperature,
                        humidity=humidity,
                        pH=ph,
                        EC=ec
                    )
                    records_created += 1
            
            self.stdout.write(f"✅ {device.Device_ID}: {records_created} sensor records")

        # Summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 80)

        for user in all_users:
            user_devices = Device.objects.filter(user=user)
            online = [d for d in user_devices if d.Device_ID not in offline_device_ids]
            offline = [d for d in user_devices if d.Device_ID in offline_device_ids]
            
            self.stdout.write(f"\n{user.User_ID}:")
            self.stdout.write(f"  Total Devices: {user_devices.count()}")
            self.stdout.write(f"  Online: {len(online)} - {', '.join([d.Device_ID for d in online])}")
            if offline:
                self.stdout.write(f"  Offline: {len(offline)} - {', '.join([d.Device_ID for d in offline])}")

        total_sensor_records = SensorValue.objects.count()
        self.stdout.write(f"\n\nTotal Sensor Records: {total_sensor_records}")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✅ SETUP COMPLETE"))
        self.stdout.write("=" * 80)
        self.stdout.write("\n✅ Each user's devices are now in nearby locations")
        self.stdout.write("✅ 30% of devices are offline")
        self.stdout.write("✅ Online devices have 7 days of sensor data")
        self.stdout.write("✅ Dashboard will now show realistic data!")
