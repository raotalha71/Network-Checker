@echo off
title Network Dashboard - Complete Auto-Setup

echo ============================================
echo Network Device Dashboard - Auto Setup
echo ============================================
echo.
echo 🚀 ONE-CLICK COMPLETE INSTALLATION 🚀
echo This will automatically install EVERYTHING needed:
echo   • Python (if missing)
echo   • All dashboard components
echo   • Start the dashboard
echo.
echo No technical knowledge required!
echo.

:: Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📥 Python not found - downloading and installing automatically...
    echo This may take 3-5 minutes depending on your internet speed.
    echo.
    
    :: Create temp directory
    if not exist temp mkdir temp
    
    :: Download Python installer
    echo Downloading Python 3.11 installer...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'temp\python_installer.exe'}"
    
    if not exist "temp\python_installer.exe" (
        echo.
        echo ❌ ERROR: Failed to download Python installer!
        echo Please check your internet connection.
        echo.
        echo Manual installation: https://python.org/downloads/
        echo ⚠️  Make sure to check "Add Python to PATH" during installation
        echo.
        pause
        exit /b 1
    )
    
    :: Install Python silently
    echo Installing Python (this may take 2-3 minutes)...
    echo Please wait - DO NOT CLOSE this window!
    temp\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0
    
    :: Wait for installation to complete
    timeout /t 10 /nobreak >nul
    
    :: Clean up installer
    del /q temp\python_installer.exe
    rmdir temp
    
    :: Refresh PATH
    echo Refreshing system PATH...
    call :RefreshPath
    
    :: Verify Python installation
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ❌ ERROR: Python installation failed!
        echo Please restart your computer and try again.
        echo Or install manually from: https://python.org/downloads/
        echo.
        pause
        exit /b 1
    )
    
    echo ✅ Python installed successfully!
    echo.
) else (
    echo ✅ Python found!
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
echo [3/6] Creating isolated environment...
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
echo [4/6] Activating environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading package installer...
python -m pip install --upgrade pip --quiet

:: Install requirements
echo [5/6] Installing dashboard components...
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

:: Auto-start the dashboard
echo [6/6] Starting Network Dashboard...
echo.
echo Starting the dashboard server...
echo ⏳ Please wait while the dashboard initializes...

start /min python app.py

:: Wait for server to start
timeout /t 3 /nobreak >nul

:: Open browser automatically
echo 🌐 Opening dashboard in your default browser...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo ============================================
echo ✅ SUCCESS! Dashboard is Running! 
echo ============================================
echo.
echo 🎉 Your Network Device Dashboard is now active!
echo.
echo 📱 Dashboard URL: http://localhost:5000
echo 🌐 Browser should open automatically
echo.
echo 🔍 The dashboard is now scanning YOUR network automatically!
echo 📊 You'll see your devices appear in real-time.
echo.
echo 🛑 To stop the dashboard: Close this window or press Ctrl+C
echo.
echo 📚 Need help? Check these guides:
echo   • USER_MANUAL.md - Complete feature guide
echo   • TROUBLESHOOTING_GUIDE.md - Problem solutions
echo.
echo ⚠️  Keep this window open while using the dashboard!
echo.

:RefreshPath
:: Refresh environment variables without restart
for /f "tokens=2*" %%i in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH') do set "SysPath=%%j"
for /f "tokens=2*" %%i in ('reg query "HKCU\Environment" /v PATH') do set "UserPath=%%j"
set "PATH=%UserPath%;%SysPath%"
goto :eof

pause