@echo off
echo ===================================================
echo Finalizing Smart IoT System Setup (Step Id: 1)
echo ===================================================

cd greeva

echo [1/4] Applying Database Migrations...
python manage.py makemigrations hydroponics
python manage.py migrate

echo [2/4] Verifying Environment...
if not exist ".env" (
    echo Creating default .env file...
    echo DEBUG=True> .env
    echo DATA_SOURCE=DUMMY>> .env
)

echo ===================================================
echo SETUP COMPLETE!
echo ===================================================
echo To Start the System:
echo 1. Keep your existing 'runserver' running (it will auto-reload).
echo 2. Open a NEW terminal and run: python simulate_sensors.py
echo    (This will pump dummy data every 5 seconds).
echo 3. Open your dashboard in the browser.
echo ===================================================
pause
