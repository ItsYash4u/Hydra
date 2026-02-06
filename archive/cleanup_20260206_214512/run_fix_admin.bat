@echo off
set "PYTHON=.venv312\Scripts\python.exe"
if exist "%PYTHON%" (
    "%PYTHON%" fix_admin_login.py > fix_output.txt 2>&1
) else (
    echo Python not found at %PYTHON% > fix_output.txt
    python fix_admin_login.py >> fix_output.txt 2>&1
)
type fix_output.txt
