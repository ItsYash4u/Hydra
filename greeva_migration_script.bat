@echo off
echo Starting Migration Process... > migration_log.txt 2>&1

echo Dumping data... >> migration_log.txt 2>&1
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > datadump.json 2>> migration_log.txt
if errorlevel 1 (
    echo Dump failed! >> migration_log.txt
    exit /b 1
)
echo Dump successful! >> migration_log.txt

echo Installing pymysql... >> migration_log.txt 2>&1
pip install pymysql >> migration_log.txt 2>&1

echo Creating MySQL DB... >> migration_log.txt 2>&1
python create_mysql_db.py >> migration_log.txt 2>&1

echo Done! >> migration_log.txt
exit /b 0
