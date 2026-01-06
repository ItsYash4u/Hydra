@echo off
echo Running check... > server_status.txt
..\.venv\Scripts\python.exe manage.py check > server_check.log 2>&1
if %errorlevel% neq 0 (
    echo Check FAILD >> server_status.txt
    exit /b
)
echo Check PASSED >> server_status.txt
echo Starting Runserver... >> server_status.txt
..\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload > server_run.log 2>&1
