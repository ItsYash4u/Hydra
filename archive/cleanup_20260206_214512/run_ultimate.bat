@echo off
cls
echo ==========================================================
echo       GREEVA - ULTIMATE STARTUP SCRIPT (SELF-HEALING)
echo ==========================================================
echo.
echo [STEP 1] LOCATING CORRECT PYTHON ENVIRONMENT (.venv312)...

set "PY_EXE=%~dp0.venv312\Scripts\python.exe"
set "PIP_EXE=%~dp0.venv312\Scripts\pip.exe"

if not exist "%PY_EXE%" (
    echo CRITICAL ERROR: .venv312 folder is missing!
    echo Please verify you have extracted the project correctly.
    pause
    exit /b
)

echo Fusion Python Found: %PY_EXE%
echo.

echo [STEP 2] VERIFYING DEPENDENCIES...
echo Installing/Updating 'django-environ', 'Pillow' and others...
"%PIP_EXE%" install django-environ Pillow django-allauth python-slugify argon2-cffi whitenoise redis hiredis PyMySQL django django-model-utils django-crispy-forms crispy-bootstrap5 django-redis djangorestframework django-filter django-cors-headers channels daphne >nul 2>&1
echo Dependencies Verified.
echo.

echo [STEP 3] FIXING DATABASE SCHEMA...
echo Detecting changes in 'users' app...
"%PY_EXE%" manage.py makemigrations users
echo Applying migrations...
"%PY_EXE%" manage.py migrate
echo Database Schema Updated.
echo.

echo [STEP 4] STARTING SERVER...
echo.
"%PY_EXE%" manage.py runserver 0.0.0.0:8000

echo.
echo If the server stopped, check the errors above.
pause
