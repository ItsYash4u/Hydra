import os
import django
from django.conf import settings
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

try:
    t = get_template('pages/pages-404.html')
    print("Found template:", t.origin.name)
except Exception as e:
    print("Error:", e)
    print("Template Dirs:", settings.TEMPLATES[0]['DIRS'])
    print("App Dirs:", settings.TEMPLATES[0]['APP_DIRS'])
