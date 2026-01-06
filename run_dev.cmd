@echo off
REM Run backend and frontend in separate command windows (Windows cmd.exe)
SET ROOT=%~dp0
REM Activate virtualenv and run Django server
start "Greeva Backend" cmd /k "cd /d "%ROOT%" && if exist .venv\Scripts\activate ( .venv\Scripts\activate && echo Activated venv ) else echo No venv found. Create with: python -m venv .venv && .venv\Scripts\activate && pip install -r requirements\base.txt && echo After installing, re-run this script. && pause && exit ) && python manage.py runserver 0.0.0.0:8000"

REM Start frontend dev server
start "Greeva Frontend" cmd /k "cd /d "%ROOT%client" && if exist node_modules ( npm run dev ) else ( echo Running npm install && npm install && npm run dev )"

echo Launched backend and frontend windows.
exit /b 0
