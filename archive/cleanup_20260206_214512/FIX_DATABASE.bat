@echo off
echo ========================================================
echo   EMERGENCY DATABASE FIX
echo ========================================================
echo.

echo Stopping any running servers...
taskkill /F /IM python.exe >nul 2>&1

echo Creating migrations...
python manage.py makemigrations hydroponics
echo.

echo Applying all migrations...
python manage.py migrate
echo.

echo Creating admin user...
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local'); django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin@example.com', 'admin'); print('Admin created')"
echo.

echo Database is now ready!
echo.
pause
