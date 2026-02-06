@echo off
cd /d "c:\Users\AYUSH\Downloads\admin\Greeva"
call .venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8000
pause
