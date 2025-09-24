@echo off
echo TJM Automation Bot - Quick Run Script
echo =====================================

echo.
echo [1/3] Checking virtual environment...
if not exist "tjm-automation-env" (
    echo Virtual environment not found. Creating one...
    python -m venv tjm-automation-env
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Installing dependencies...
    call tjm-automation-env\Scripts\activate.bat
    pip install --upgrade -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [2/3] Activating virtual environment...
call tjm-automation-env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/3] Starting TJM Automation Bot...
echo.
echo IMPORTANT: 
echo - Make sure you have an internet connection
echo - Do not move the mouse during automation
echo - Move mouse to top-left corner to emergency stop
echo - Check config.env for configuration options
echo.

python bot.py

echo.
echo Automation completed. Check the log file for details.
pause
