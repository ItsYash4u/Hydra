@echo off
set PYTHON="c:\Users\AYUSH\Downloads\admin\.venv\Scripts\python.exe"
set MANAGE="c:\Users\AYUSH\Downloads\admin\Greeva\manage.py"

echo Running check... > server_status.txt
%PYTHON% --version >> server_status.txt 2>&1
%PYTHON% %MANAGE% check >> server_check.log 2>&1
if %errorlevel% neq 0 (
    echo Check FAILD >> server_status.txt
    exit /b
)
echo Check PASSED >> server_status.txt
echo Starting Runserver... >> server_status.txt
%PYTHON% %MANAGE% runserver 127.0.0.1:8000 --noreload >> server_run.log 2>&1
