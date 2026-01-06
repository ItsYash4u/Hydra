@echo off
echo ==========================================
echo       Greeva Hydroponics Setup
echo ==========================================

echo Cleaning up pyc files...
del /S /Q *.pyc > nul 2>&1

echo.
echo Running Project Setup (Migrations, User, Data)...
python setup_project.py > setup_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Setup Failed! Check setup_log.txt for details.
    type setup_log.txt
    pause
    exit /b %ERRORLEVEL%
)
type setup_log.txt

echo.
echo ==========================================
echo       Starting Development Server
echo ==========================================
echo Access at: http://127.0.0.1:8000/hydroponics/dashboard/
echo Admin:     http://127.0.0.1:8000/admin/
echo Login:     admin@example.com / admin
echo.
python manage.py runserver 0.0.0.0:8000
