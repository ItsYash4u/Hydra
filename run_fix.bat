@echo off
set PYTHONUTF8=1
.venv312\Scripts\python manage.py makemigrations users > migration_log.txt 2>&1
echo ---------------------------------------- >> migration_log.txt
.venv312\Scripts\python manage.py migrate users >> migration_log.txt 2>&1
echo ---------------------------------------- >> migration_log.txt
.venv312\Scripts\python verify_otp_setup.py >> migration_log.txt 2>&1
