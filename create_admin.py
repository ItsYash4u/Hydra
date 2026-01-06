#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
if not User.objects.filter(email='admin@hydroponics.local').exists():
    admin = User.objects.create_superuser(
        email='admin@hydroponics.local',
        password='admin123456',
        name='Admin User'
    )
    print('✅ Superuser created successfully!')
    print(f'Email: admin@hydroponics.local')
    print(f'Password: admin123456')
else:
    print('✅ Superuser already exists')

print('\n🌱 System is ready to run!')
print('Access points:')
print('  - Dashboard: http://localhost:8000/pages/hydroponics-dashboard/')
print('  - Admin: http://localhost:8000/admin/')
print('  - API: http://localhost:8000/hydroponics/api/')
