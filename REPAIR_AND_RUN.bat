@echo off
echo ===================================================
echo REPAIRING IOT DATABASE & RESTARTING SERVER (FIXED)
echo ===================================================

REM Ensure we are in the project root containing manage.py
if not exist "manage.py" (
    echo Error: manage.py not found in current directory.
    echo Please make sure you are running this from the folder containing manage.py
    pause
    exit /b
)

echo [1/3] Applying Migrations Explicitly...
python manage.py migrate hydroponics --noinput

echo [2/3] Starting Simulated Sensor Device (New Window)...
REM simulate_sensors.py is inside the greeva app directory
start "Sensor Simulator" python greeva/simulate_sensors.py

echo [3/3] Starting Django Server...
echo Please ensure no other server is running on port 8000.
python manage.py runserver

pause
