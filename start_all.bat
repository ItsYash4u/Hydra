@echo off
echo Starting cleanup... > server_log.txt
del /S /Q *.pyc >> server_log.txt 2>&1
del db.sqlite3 >> server_log.txt 2>&1
echo DB Deleted >> server_log.txt

echo Making migrations... >> server_log.txt
python manage.py makemigrations >> server_log.txt 2>&1
echo Migrating... >> server_log.txt
python manage.py migrate >> server_log.txt 2>&1

echo Creating superuser... >> server_log.txt
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'admin')" >> server_log.txt 2>&1

echo Starting Server... >> server_log.txt
python manage.py runserver 0.0.0.0:8000 --noreload >> server_log.txt 2>&1
