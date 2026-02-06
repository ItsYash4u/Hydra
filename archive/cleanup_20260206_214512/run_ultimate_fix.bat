@echo off
echo ==========================================
echo    Greeva Deep Fix & Start
echo ==========================================

echo [1/5] Installing Dependencies...
pip install django-environ django-allauth argon2-cffi whitenoise > install_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Errors creating dependencies. Attempting to continue...
)

echo [2/5] Cleaning old database and migrations...
if exist db.sqlite3 del /F /Q db.sqlite3
cd greeva\hydroponics\migrations
del /Q 0*.py
cd ..\..\..

echo [3/5] Re-creating Database and Users...
python setup_project.py > setup_log_v2.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Setup CRASHED. checking log...
    type setup_log_v2.txt
    pause
    exit /b
)
type setup_log_v2.txt

echo.
echo [4/5] Starting Server...
echo Access at: http://127.0.0.1:8000/hydroponics/dashboard/
echo.
python manage.py runserver 0.0.0.0:8000
