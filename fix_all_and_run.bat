@echo off
set PYTHONUTF8=1
echo ===================================================
echo       Greeva Admin - Fix & Run Script
echo ===================================================

echo [1/4] Checking Virtual Environment...
if exist ".venv312\Scripts\python.exe" (
    echo Using .venv312
    set VENV=.venv312
) else (
    echo .venv312 not found. Checking .venv...
    if exist ".venv\Scripts\python.exe" (
        echo Using .venv
        set VENV=.venv
    ) else (
        echo ERROR: No virtual environment found!
        pause
        exit /b 1
    )
)

echo [2/4] Installing Critical Dependencies...
%VENV%\Scripts\pip install django-environ Pillow django-allauth python-slugify argon2-cffi whitenoise redis hiredis PyMySQL django django-model-utils django-crispy-forms crispy-bootstrap5 django-redis djangorestframework django-filter django-cors-headers channels daphne
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [3/4] Running Migrations...
%VENV%\Scripts\python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Migration encountered an issue (maybe already applied). Continuing...
)

echo [4/4] Starting Server...
echo ---------------------------------------------------
echo Server running at: http://127.0.0.1:8000/
echo Admin running at:  http://127.0.0.1:8000/admin/
echo ---------------------------------------------------
%VENV%\Scripts\python manage.py runserver 0.0.0.0:8000

pause
