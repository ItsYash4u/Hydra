from django.contrib.auth import get_user_model
from greeva.hydroponics.models import Device
import datetime

User = get_user_model()
users = User.objects.all()
print(f"Users: {users.count()}")
for u in users:
    print(f" - {u.email} (Phone: {u.phone_number}, Age: {u.age})")

devices = Device.objects.all()
print(f"Devices: {devices.count()}")
for d in devices:
    print(f" - {d.device_id} (User: {d.user.email})")
