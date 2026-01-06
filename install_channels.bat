@echo off
set PIP_REQUIRE_VIRTUALENV=
set PIP_CONFIG_FILE=
set PIP_INDEX_URL=
set PIP_EXTRA_INDEX_URL=
set PIP_CONSTRAINT=
"c:\Users\AYUSH\Downloads\admin\.venv\Scripts\python.exe" -m pip install channels daphne channels-redis paho-mqtt > install_log.txt 2>&1
echo Done >> install_log.txt
