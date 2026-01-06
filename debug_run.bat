@echo off
echo Starting server debug...
echo Python path: ..\.venv\Scripts\python.exe
..\.venv\Scripts\python.exe --version
echo Checking project...
..\.venv\Scripts\python.exe manage.py check
if %errorlevel% neq 0 (
    echo Check failed!
    exit /b %errorlevel%
)
echo Check passed. Starting runserver...
..\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000 --noreload
