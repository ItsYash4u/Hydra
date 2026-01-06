@echo off
echo ====================================================
echo      GREEVA DATABASE REPAIR & START
echo ====================================================

echo [1/3] Applying Database Migrations...
python manage.py makemigrations
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo Migration Failed!
    pause
    exit /b
)

echo.
echo [2/3] Ensuring Admin User (admin@example.com)...
python setup_project.py

echo.
echo [3/3] Starting Web Server...
echo Access at: http://127.0.0.1:8000/hydroponics/dashboard/
echo.
python manage.py runserver 0.0.0.0:8000
