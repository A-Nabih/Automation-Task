@echo off
echo TJM Automation Bot - Virtual Environment Setup
echo ===============================================

echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version
echo Python is installed correctly!

echo.
echo [2/5] Creating virtual environment...
if exist "tjm-automation-env" (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q "tjm-automation-env"
)

python -m venv tjm-automation-env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!

echo.
echo [3/5] Activating virtual environment...
call tjm-automation-env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!

echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

echo.
echo [5/5] Installing dependencies...
pip install --upgrade -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ===============================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ===============================================
echo.
echo To activate the virtual environment in the future:
echo   tjm-automation-env\Scripts\activate.bat
echo.
echo To run the bot:
echo   python bot.py
echo.
echo To deactivate the virtual environment:
echo   deactivate
echo.
pause
