@echo off
echo Stopping any existing Python processes...
taskkill /F /IM python.exe >nul 2>&1

echo Starting Backend Server on port 8000 using Python 3.13...
start "Django Backend" cmd /k ".venv312\Scripts\activate & python manage.py runserver 0.0.0.0:8000"

echo Starting Frontend Server...
cd client
start "React Frontend" cmd /k "npm run dev"

echo Done! Website should be available at http://localhost:5173/ and Admin at http://localhost:8000/admin/
pause
