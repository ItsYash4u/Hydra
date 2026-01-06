@echo off
C:\Python314\python.exe -c "import os; open('env_vars.txt', 'w').write(str(os.environ))"
echo Done >> install_log.txt
