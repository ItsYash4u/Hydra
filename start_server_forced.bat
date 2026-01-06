@echo off
echo ====================================================
echo FORCE START SERVER - IGNORING SYSTEM PYTHON
echo ====================================================

:: 1. Force use of .venv312 where we installed dependencies
set "VENV_PYTHON=.venv312\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: .venv312 not found!
    echo Attempting to use .venv...
    set "VENV_PYTHON=.venv\Scripts\python.exe"
)

if not exist "%VENV_PYTHON%" (
    echo CRITICAL ERROR: No valid virtual environment found.
    pause
    exit /b 1
)

echo Using Python: %VENV_PYTHON%
echo.

:: 2. Check for django-environ again just to be safe
%VENV_PYTHON% -c "import environ; print('django-environ is ready')" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: django-environ missing in %VENV_PYTHON%. Installing...
    .venv312\Scripts\pip install django-environ Pillow
)

:: 3. Run Server
echo Starting Django Server...
%VENV_PYTHON% manage.py runserver 0.0.0.0:8000

pause
