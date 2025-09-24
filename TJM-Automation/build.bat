@echo off
echo TJM Automation Bot - Build Script
echo ==================================

echo.
echo [1/5] Setting up virtual environment...
if not exist "tjm-automation-env" (
    echo Creating virtual environment...
    python -m venv tjm-automation-env
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call tjm-automation-env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

echo.
echo [3/5] Installing dependencies...
pip install --upgrade -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Running tests...
python -c "import pyautogui, pygetwindow, requests, dotenv; print('All dependencies imported successfully')"
if %errorlevel% neq 0 (
    echo ERROR: Dependency test failed
    pause
    exit /b 1
)

echo.
echo [5/5] Building executable...
pyinstaller tjm_automation.spec
if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Executable location: dist\TJM_Automation_Bot.exe
echo.
echo To run the bot:
echo   1. Double-click TJM_Automation_Bot.exe
echo   2. Or run: python bot.py
echo.
pause