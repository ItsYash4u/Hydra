@echo off
echo ==========================================
echo    Greeva Final Fix
echo ==========================================

echo [1/3] Installing ALL specific dependencies...
pip install django-environ django-allauth argon2-cffi whitenoise django-crispy-forms crispy-bootstrap5 django-filter djangorestframework django-cors-headers > install_log_final.txt 2>&1

echo [2/3] Re-running Setup...
python setup_project.py > setup_log_final.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Setup failed again.
    type setup_log_final.txt
) else (
    echo Setup success!
)

echo [3/3] Starting Server...
python manage.py runserver 0.0.0.0:8000
