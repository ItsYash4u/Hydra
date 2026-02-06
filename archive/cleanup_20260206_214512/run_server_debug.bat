@echo off
rem Ensure we use the correct python interpreter
set PYTHON="C:\Users\AYUSH\AppData\Local\Programs\Python\Python312\python.exe"
%PYTHON% manage.py migrate --noinput
if errorlevel 1 (
    echo Migration failed. Check migrate.log
    exit /b 1
)
%PYTHON% manage.py runserver 0.0.0.0:8000
