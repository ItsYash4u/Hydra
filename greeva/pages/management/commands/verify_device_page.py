from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from greeva.users.models import User
from greeva.hydroponics.models import Device, MaintenanceLog, AuditLog
from django.utils import timezone

class Command(BaseCommand):
    help = 'Diff the device detail page logic'

    def handle(self, *args, **options):
        client = Client()
        user, _ = User.objects.get_or_create(email='sys_test_2@example.com', defaults={'name': 'Sys'})
        user.set_password('pass')
        user.save()
        client.force_login(user)

        # Create full test data
        device, _ = Device.objects.get_or_create(sensor_id='TEST-FULL-001', defaults={'name': 'Full Dev', 'status': 'online'})
        MaintenanceLog.objects.create(device=device, maintenance_type='cleaning', description='Test Clean', performed_at=timezone.now(), performed_by=user)
        AuditLog.objects.create(device=device, action_type='pump_toggle', details={'state': 'on'}, performed_by=user)
        
        self.stdout.write(f"Testing Device Detail for: {device.name} (ID: {device.pk})")
        
        try:
            url = reverse('pages:device_detail', args=[device.pk])
            resp = client.get(url)
            
            if resp.status_code == 200:
                self.stdout.write(self.style.SUCCESS("✓ Device Detail Page Works Perfectly"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ Failed with status {resp.status_code}"))
                # Print exception if available in context? No, client.get creates it.
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ CRASHED: {e}"))
            import traceback
            traceback.print_exc()

