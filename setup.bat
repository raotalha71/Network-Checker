@echo off
echo Setting up Network Device Dashboard...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or later from https://python.org
    pause
    exit /b 1
)

:: Check if nmap is available (optional but recommended)
nmap --version >nul 2>&1
if errorlevel 1 (
    echo Warning: nmap is not installed. Some features may be limited.
    echo Download from: https://nmap.org/download.html
    echo.
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

:: Initialize database
echo Initializing database...
python -c "from database import DatabaseManager; DatabaseManager()"

echo.
echo Setup complete!
echo.
echo To start the dashboard:
echo   1. Run: venv\Scripts\activate
echo   2. Run: python app.py
echo   3. Open: http://localhost:5000
echo.
pause