@echo off
echo ====================================================
echo      GREEVA WEBSITE STARTER
echo ====================================================

echo [1/2] Checking and Installing Dependencies...
python fix_dependencies.py

echo.
echo [2/2] Starting Web Server...
echo Access the site at: http://127.0.0.1:8000/hydroponics/dashboard/
echo.
python manage.py runserver 0.0.0.0:8000
pause
