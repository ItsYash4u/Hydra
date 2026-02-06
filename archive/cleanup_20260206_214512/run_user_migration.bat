@echo off
set PYTHONUTF8=1
echo Making migrations...
.venv312\Scripts\python manage.py makemigrations users > migration_log_user.txt 2>&1
echo Migrating...
.venv312\Scripts\python manage.py migrate users >> migration_log_user.txt 2>&1
echo Done.
