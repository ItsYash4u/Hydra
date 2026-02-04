"""
Django management command to redistribute devices among users
WITHOUT changing Device_IDs (to avoid foreign key issues)
"""
from django.core.management.base import BaseCommand
from greeva.hydroponics.models_custom import Device, UserDevice
import random


class Command(BaseCommand):
    help = 'Redistribute devices among users (5-10 per user) without changing IDs'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("DEVICE REDISTRIBUTION (SAFE MODE)")
        self.stdout.write("=" * 80)

        # Get all regular users
        all_users = list(UserDevice.objects.filter(Role='user').order_by('User_ID'))
        
        if not all_users:
            self.stdout.write(self.style.ERROR("\n⚠️  No regular users found!"))
            return

        total_users = len(all_users)
        self.stdout.write(f"\nTotal Regular Users: {total_users}")

        # Calculate required devices
        min_devices_needed = total_users * 5
        target_devices = total_users * 7  # Target 7 devices per user
        
        # Get current devices
        current_devices = list(Device.objects.all().order_by('Device_ID'))
        current_count = len(current_devices)
        
        self.stdout.write(f"Current Devices: {current_count}")
        self.stdout.write(f"Minimum Required: {min_devices_needed}")
        self.stdout.write(f"Target: {target_devices}")

        # Create additional devices if needed
        if current_count < min_devices_needed:
            needed = min_devices_needed - current_count
            self.stdout.write(f"\n⚠️  Creating {needed} additional devices...")
            
            # Find the highest existing device number
            existing_ids = [d.Device_ID for d in current_devices]
            max_num = 0
            for dev_id in existing_ids:
                try:
                    # Try to extract number from various formats
                    if dev_id.startswith('DEV-'):
                        num = int(dev_id.split('-')[1])
                        max_num = max(max_num, num)
                except:
                    pass
            
            # Create new devices with sequential IDs
            for i in range(needed):
                new_id = f"DEV-{max_num + i + 1:03d}"
                new_device = Device.objects.create(
                    Device_ID=new_id,
                    Latitude=26.0 + (i * 0.1),
                    Longitude=91.0 + (i * 0.1),
                    user=all_users[i % total_users]
                )
                self.stdout.write(f"✅ Created {new_device.Device_ID}")
            
            # Refresh device list
            current_devices = list(Device.objects.all().order_by('Device_ID'))

        # Redistribute devices evenly
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("REDISTRIBUTING DEVICES")
        self.stdout.write("=" * 80)

        total_devices = len(current_devices)
        devices_per_user = total_devices // total_users
        extra_devices = total_devices % total_users
        
        # Ensure minimum 5 devices per user
        if devices_per_user < 5:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️  Warning: Only {devices_per_user} devices per user. Need more devices!"
            ))

        self.stdout.write(f"\nBase allocation: {devices_per_user} devices per user")
        if extra_devices:
            self.stdout.write(f"Extra devices: {extra_devices} (will be distributed to first users)")

        # Shuffle for fair distribution
        random.shuffle(current_devices)

        # Distribute devices
        device_index = 0
        for user_idx, user in enumerate(all_users):
            # Calculate devices for this user
            user_device_count = devices_per_user
            if user_idx < extra_devices:
                user_device_count += 1  # Give extra device to first N users
            
            # Get devices for this user
            user_devices = current_devices[device_index:device_index + user_device_count]
            
            # Assign devices to user
            for device in user_devices:
                device.user = user
                device.save(update_fields=['user'])  # Only update user field
            
            device_index += user_device_count
            
            # Display assignment
            device_ids = [d.Device_ID for d in user_devices]
            self.stdout.write(f"\n✅ {user.User_ID} ({user.Email_ID})")
            self.stdout.write(f"   Devices ({len(user_devices)}): {', '.join(device_ids)}")

        # Final summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("FINAL DISTRIBUTION SUMMARY")
        self.stdout.write("=" * 80)

        all_good = True
        for user in all_users:
            device_count = Device.objects.filter(user=user).count()
            if device_count < 5:
                status = "⚠️"
                all_good = False
            elif device_count > 10:
                status = "⚠️"
                all_good = False
            else:
                status = "✅"
            self.stdout.write(f"{status} {user.User_ID}: {device_count} devices")

        self.stdout.write("\n" + "=" * 80)
        if all_good:
            self.stdout.write(self.style.SUCCESS("✅ REDISTRIBUTION COMPLETE"))
            self.stdout.write("All users have 5-10 devices!")
        else:
            self.stdout.write(self.style.WARNING("⚠️  REDISTRIBUTION COMPLETE WITH WARNINGS"))
            self.stdout.write("Some users may have less than 5 or more than 10 devices")
        self.stdout.write("=" * 80)
