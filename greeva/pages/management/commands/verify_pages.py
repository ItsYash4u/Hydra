from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from greeva.users.models import User
from greeva.hydroponics.models import Device

class Command(BaseCommand):
    help = 'Verifies critical pages return 200 OK'

    def handle(self, *args, **options):
        client = Client()
        
        self.stdout.write("--- Starting System Check ---")

        # 1. Check Public Pages
        self.check_url(client, 'pages:dashboard', "Dashboard")
        self.check_url(client, 'account_login', "Login Page")

        # Setup User for authenticated tests
        user, _ = User.objects.get_or_create(email='test_sys@example.com', defaults={'name': 'System Tester'})
        user.set_password('password123')
        user.save()
        client.force_login(user)

        # 3. Check Profile Page (User Profile)
        self.check_url(client, 'users:profile', "My Profile")

        # Setup Device
        Device.objects.get_or_create(sensor_id='SYS-TEST-001', defaults={'name': 'System Device', 'status': 'online'})

        # 4. Check Search with results
        self.check_url(client, 'pages:search', "Search (Existing)", {'q': 'System'})

        # 5. Check Search with NO results (verify custom message)
        resp = client.get(reverse('pages:search'), {'q': 'NON_EXISTENT_ID_999'})
        if resp.status_code == 200:
            content = resp.content.decode('utf-8')
            if "Recheck the ID as the device is not available" in content:
                self.stdout.write(self.style.SUCCESS("✓ Search (Empty) Message Verified"))
            else:
                 self.stdout.write(self.style.ERROR("✗ Search (Empty) Message Missing!"))
        else:
             self.stdout.write(self.style.ERROR(f"✗ Search (Empty) Failed: {resp.status_code}"))
             
        self.stdout.write("--- System Check Complete ---")

    def check_url(self, client, url_name, label, params=None):
        if params is None: params = {}
        try:
            resp = client.get(reverse(url_name), params)
            if resp.status_code in [200, 302]:
                self.stdout.write(self.style.SUCCESS(f"✓ {label} OK"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ {label} Failed: {resp.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ {label} Error: {e}"))
