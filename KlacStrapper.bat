@echo off
REM Navigate to the directory where the project is located
cd /d %~dp0

REM Navigate to klac_app where main.py is located
cd klac_app

REM Run the Python script to load preferences and start the app
python main.py

REM Pause to keep the window open after execution
pause
