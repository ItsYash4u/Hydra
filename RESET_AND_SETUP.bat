@echo off
echo ========================================================
echo   COMPLETE SYSTEM RESET AND SETUP
echo ========================================================
echo.
echo This will reset your database and create a fresh setup.
echo Press Ctrl+C now to cancel, or
pause

echo.
echo [1/5] Stopping any running servers...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo [2/5] Removing old database...
if exist db.sqlite3 del /F db.sqlite3
echo Old database removed.

echo [3/5] Creating fresh migrations...
python manage.py makemigrations
python manage.py makemigrations hydroponics

echo [4/5] Building database...
python manage.py migrate

echo [5/5] Setting up initial data...
python complete_setup.py

echo.
echo ========================================================
echo   SETUP COMPLETE!
echo ========================================================
echo.
echo You can now start the server with: START_SERVER.bat
echo.
pause
