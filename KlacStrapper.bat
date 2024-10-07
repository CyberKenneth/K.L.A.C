@echo off
REM Print the initial directory where the script starts
echo Initial directory: %CD%

REM Navigate to the directory where the script is located
cd /d "%~dp0"

REM Print the directory after navigating to the script location
echo After navigating to script location: %CD%

REM Navigate to the directory containing main.py using relative path
cd "klac_app\internal\src\core"

REM Print the directory after navigating to core directory
echo After navigating to core directory: %CD%

REM Ensure we're in the correct directory structure
if not exist "main.py" (
    echo Error: main.py not found in the current directory.
    echo Current directory: %CD%
    echo Please make sure you're running this script from the correct location.
    pause
    exit /b 1
)

REM Run the Python script to load preferences and start the app
python main.py

REM Pause to keep the window open after execution
pause
