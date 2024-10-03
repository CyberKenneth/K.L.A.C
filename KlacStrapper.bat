@echo off
setlocal

REM Set the target directory and GitHub repository
set "TARGET_DIR=K.L.A.C"
set "GIT_REPO=https://raw.githubusercontent.com/CyberKenneth/K.L.A.C/Main/requirements.txt"
set "REQ_FILE_PATH=data\requirements.txt"

REM Get the current directory
set "CURRENT_DIR=%cd%"

REM Prompt user for setup confirmation
echo Do you want to proceed with the directory setup? (Y/N)
choice /c YN /n /m "Press Y to confirm or N to exit."
if %ERRORLEVEL%==2 (
    echo Setup cancelled by user.
    exit /b 0
)

REM Check if the K.L.A.C directory exists in the current directory
if not exist "%TARGET_DIR%" (
    echo Creating K.L.A.C directory...
    mkdir "%TARGET_DIR%"
)

REM Change to the K.L.A.C directory
cd "%TARGET_DIR%"

:setup_structure
REM Create subdirectories only if they do not exist

REM Create the klac_app directory and its subdirectories
if not exist "klac_app" (
    mkdir "klac_app"
)
if not exist "klac_app\main.py" (
    echo. > "klac_app\main.py"
)
if not exist "klac_app\gui" (
    mkdir "klac_app\gui"
)
if not exist "klac_app\conversion" (
    mkdir "klac_app\conversion"
)
if not exist "klac_app\viewers" (
    mkdir "klac_app\viewers"
)
if not exist "klac_app\utils" (
    mkdir "klac_app\utils"
)

REM Create the resources directory
if not exist "resources" (
    mkdir "resources"
)

REM Create the dependencies directory and its subdirectories
if not exist "dependencies" (
    mkdir "dependencies"
)
if not exist "dependencies\poppler" (
    mkdir "dependencies\poppler"
)
if not exist "dependencies\other_libs" (
    mkdir "dependencies\other_libs"
)

REM Create the data directory and its subdirectories
if not exist "data" (
    mkdir "data"
)
if not exist "data\config.json" (
    echo {} > "data\config.json"
)
if not exist "data\updates" (
    mkdir "data\updates"
)
if not exist "data\temp" (
    mkdir "data\temp"
)

REM Create the update.py file
if not exist "update.py" (
    echo. > "update.py"
)
if not exist "start.py" (
    echo. > "start.py"
)

REM Check for updates on GitHub for requirements.txt
echo Checking for updates from GitHub...
powershell -Command "Invoke-WebRequest -Uri '%GIT_REPO%' -OutFile 'data\requirements.txt'"

REM Compare with local file and install dependencies if changed
if exist "%REQ_FILE_PATH%" (
    echo Comparing with the existing requirements file...
    powershell -Command "(Compare-Object (Get-Content '%REQ_FILE_PATH%') (Invoke-WebRequest -Uri '%GIT_REPO%' | Select-Object -Expand Content))"

    REM Install dependencies if there are changes
    if "%ERRORLEVEL%" neq "0" (
        echo Installing or updating dependencies...
        pip install -r "data\requirements.txt"
    )
)

REM Execute Python script for startup logging and main program launch
echo Running Python setup...
python start.py

echo K.L.A.C. setup structure is complete.

REM Automatically delete the setup script
echo Deleting setup script...
del "%~f0"

pause
exit /b 0
