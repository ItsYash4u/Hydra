@echo off
cls
echo ========================================================
echo           GREEVA HYDROPONICS - LAUNCHER
echo ========================================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [Step 1/2] Initializing Database and System...
echo.
python complete_setup.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo   ERROR: Setup failed! Please check the error above.
    echo ========================================================
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [Step 2/2] Starting Development Server...
echo ========================================================
echo.
echo Server is starting at: http://127.0.0.1:8000
echo Dashboard URL: http://127.0.0.1:8000/hydroponics/dashboard/
echo.
echo Press Ctrl+C to stop the server
echo ========================================================
echo.

python manage.py runserver 0.0.0.0:8000

pause
