@echo off
echo ======================================================================
echo CREATING TEST DEVICE
echo ======================================================================
echo.

cd /d "c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva"
call ..\.venv312\Scripts\activate.bat
python create_test_device.py

echo.
echo ======================================================================
echo Done! Press any key to close...
pause
