@echo off
mkdir Smart_IoT_Backup 2>nul
mkdir Smart_IoT_Backup\greeva\templates\pages 2>nul
mkdir Smart_IoT_Backup\greeva\templates\partials 2>nul
mkdir Smart_IoT_Backup\greeva\pages 2>nul
mkdir Smart_IoT_Backup\greeva\hydroponics 2>nul
mkdir Smart_IoT_Backup\greeva\users 2>nul

echo Copying files...
copy /Y greeva\templates\pages\hydroponics-dashboard.html Smart_IoT_Backup\greeva\templates\pages\
copy /Y greeva\templates\pages\measurement.html Smart_IoT_Backup\greeva\templates\pages\
copy /Y greeva\templates\pages\services.html Smart_IoT_Backup\greeva\templates\pages\
copy /Y greeva\templates\partials\sidenav.html Smart_IoT_Backup\greeva\templates\partials\
copy /Y greeva\templates\base.html Smart_IoT_Backup\greeva\templates\
copy /Y greeva\pages\views.py Smart_IoT_Backup\greeva\pages\
copy /Y greeva\pages\urls.py Smart_IoT_Backup\greeva\pages\
copy /Y greeva\hydroponics\views.py Smart_IoT_Backup\greeva\hydroponics\
copy /Y greeva\hydroponics\urls.py Smart_IoT_Backup\greeva\hydroponics\
copy /Y greeva\users\signals.py Smart_IoT_Backup\greeva\users\
copy /Y greeva\hydroponics\models.py Smart_IoT_Backup\greeva\hydroponics\

echo Backup Complete.
