import os
import sys
import traceback

print("Starting Django Status Check...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    import django
    django.setup()
    print("Django Setup OK")
except Exception:
    traceback.print_exc()
    sys.exit(1)

try:
    from django.core.management import call_command
    print("Running system check...")
    call_command('check')
    print("System Check OK")
except Exception:
    traceback.print_exc()
    sys.exit(1)
