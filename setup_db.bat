@echo off
echo ==========================================
echo      CUSTOM DATABASE SETUP SCRIPT
echo ==========================================

echo.
echo ⚠️  WARNING: This will kill all running Python processes to free the database.
echo    Make sure you have saved your work!
echo.
timeout /t 3

echo.
echo 1. Stopping Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1

echo.
echo 2. Cleaning cleanup...
del db.sqlite3
if exist db.sqlite3 (
    echo ❌ ERROR: Could not delete db.sqlite3. It is still locked.
    echo    Please close any other terminals using the database.
    pause
    exit /b 1
)
del greeva\hydroponics\migrations\0*.py
del greeva\users\migrations\0*.py

echo.
echo 3. Creating migrations...
echo    - Users app...
python manage.py makemigrations users
if %ERRORLEVEL% NEQ 0 goto :error

echo    - Hydroponics app...
python manage.py makemigrations hydroponics
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo 4. Applying migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo 5. Seeding database...
python seed_database.py
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo 6. Verifying...
python manage.py shell -c "from greeva.hydroponics.models_custom import UserDevice; print(f'User count: {UserDevice.objects.count()}')"

echo.
echo ==========================================
echo      SETUP COMPLETE SUCCESSFULLY!
echo ==========================================
echo You can now run: python manage.py runserver
pause
exit /b 0

:error
echo.
echo ==========================================
echo           SETUP FAILED
echo ==========================================
pause
exit /b 1
