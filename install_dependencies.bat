@echo off
title Network Dashboard - Dependency Installation

echo ============================================
echo Network Device Dashboard - Setup
echo ============================================
echo.
echo Setting up Network Device Dashboard for your system...
echo This will install all required components automatically.
echo.

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed on this system!
    echo.
    echo Please install Python 3.8 or higher from: https://python.org/downloads/
    echo.
    echo ⚠️  IMPORTANT: During installation, make sure to check:
    echo    "Add Python to PATH" ✅
    echo.
    echo After installing Python, run this script again.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!

:: Check Python version
echo [2/5] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python version is too old!
    echo This dashboard requires Python 3.8 or higher.
    echo Please update Python from: https://python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python version is compatible!

:: Create virtual environment
echo [3/5] Creating isolated environment...
if exist "venv" (
    echo Virtual environment already exists, removing old version...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to create virtual environment!
    echo This might be due to permissions. Try running as Administrator.
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment created!

:: Activate virtual environment
echo [4/5] Activating environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading package installer...
python -m pip install --upgrade pip --quiet

:: Install requirements
echo [5/5] Installing dashboard components...
echo This may take 2-3 minutes depending on your internet connection...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install required packages!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo ✅ Installation Complete!
echo ============================================
echo.
echo Your Network Device Dashboard is ready to use!
echo.
echo To start the dashboard:
echo   1. Double-click "quick_start.bat"
echo   2. Open browser to: http://localhost:5000
echo.
echo The dashboard will automatically detect and scan YOUR network.
echo.
echo Need help? Check the documentation folder for:
echo   • User Manual
echo   • Installation Guide  
echo   • Troubleshooting Guide
echo.
pause