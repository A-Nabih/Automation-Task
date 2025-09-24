# TJM Automation Bot - PowerShell Virtual Environment Setup

Write-Host "TJM Automation Bot - Virtual Environment Setup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

Write-Host ""
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Cyan
if (-not (Test-Command "python")) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version
Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green

Write-Host ""
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "tjm-automation-env") {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "tjm-automation-env"
}

python -m venv tjm-automation-env
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Virtual environment created successfully!" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Cyan
& "tjm-automation-env\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Virtual environment activated!" -ForegroundColor Green

Write-Host ""
Write-Host "[4/5] Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to upgrade pip, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[5/5] Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "SETUP COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment in the future:" -ForegroundColor Cyan
Write-Host "  tjm-automation-env\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run the bot:" -ForegroundColor Cyan
Write-Host "  python bot.py" -ForegroundColor White
Write-Host ""
Write-Host "To deactivate the virtual environment:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
