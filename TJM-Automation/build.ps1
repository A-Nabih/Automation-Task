# TJM Automation Bot - PowerShell Build Script
# This script handles the complete build process

Write-Host "TJM Automation Bot - PowerShell Build Script" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check Python installation
if (-not (Test-Command "python")) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip installation
if (-not (Test-Command "pip")) {
    Write-Host "ERROR: pip is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/5] Setting up virtual environment..." -ForegroundColor Cyan
try {
    if (-not (Test-Path "tjm-automation-env")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv tjm-automation-env
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
    }
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "tjm-automation-env\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to activate virtual environment"
    }
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Virtual environment setup failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/5] Upgrading pip..." -ForegroundColor Cyan
try {
    python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Failed to upgrade pip, continuing anyway..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Failed to upgrade pip, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Cyan
try {
    pip install --upgrade -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed"
    }
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[4/5] Testing dependencies..." -ForegroundColor Cyan
try {
    python -c "import pyautogui, pygetwindow, requests, dotenv, pathlib, logging, subprocess, time, os, sys, typing; print('All dependencies imported successfully')"
    if ($LASTEXITCODE -ne 0) {
        throw "Dependency test failed"
    }
    Write-Host "Dependency test passed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Dependency test failed" -ForegroundColor Red
    Write-Host "Some required modules are missing" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[5/5] Building executable..." -ForegroundColor Cyan
try {
    # Check if PyInstaller is available
    if (-not (Test-Command "pyinstaller")) {
        Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
        pip install pyinstaller
    }
    
    # Build the executable
    pyinstaller tjm_automation.spec
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller build failed"
    }
    Write-Host "Executable built successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location: dist\TJM_Automation_Bot.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run the bot:" -ForegroundColor Cyan
Write-Host "  1. Double-click TJM_Automation_Bot.exe" -ForegroundColor White
Write-Host "  2. Or run: python bot.py" -ForegroundColor White
Write-Host ""

# Check if executable was created
if (Test-Path "dist\TJM_Automation_Bot.exe") {
    $fileSize = (Get-Item "dist\TJM_Automation_Bot.exe").Length / 1MB
    Write-Host "Executable size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "WARNING: Executable not found in dist folder" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"