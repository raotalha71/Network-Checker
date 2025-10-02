@echo off
title Network Dashboard - Complete Auto-Installation and Startup

echo.
echo ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
echo ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
echo ██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
echo ██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
echo ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
echo ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
echo.
echo ============================================================================
echo                    NETWORK DEVICE DASHBOARD - ONE-CLICK SETUP
echo ============================================================================
echo.
echo 🚀 FULLY AUTOMATED INSTALLATION - NO TECHNICAL KNOWLEDGE REQUIRED!
echo.
echo This will automatically:
echo   ✅ Install Python (if missing)
echo   ✅ Install all required components  
echo   ✅ Set up the dashboard
echo   ✅ Start the dashboard automatically
echo   ✅ Open in your browser
echo.
echo Just sit back and relax! ☕
echo.

:: Administrative check
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo ⚠️  REQUESTING ADMINISTRATOR PRIVILEGES...
    echo This is needed to install Python automatically.
    echo.
    echo Please click "Yes" when prompted by Windows.
    echo.
    pause
    goto UACPrompt
) else ( 
    echo ✅ Administrator privileges confirmed!
    goto GotAdmin 
)

:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:GotAdmin
cd /d "%~dp0"

echo.
echo ============================================================================
echo                              🔍 SYSTEM CHECK
echo ============================================================================

:: Check if Python is installed
echo [1/7] 🔍 Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📥 Python not found - installing Python 3.11 automatically...
    echo ⏳ This will take 3-5 minutes. Please be patient...
    echo.
    
    :: Create temp directory
    if not exist temp mkdir temp
    
    :: Download Python installer
    echo 🌐 Downloading Python installer...
    powershell -WindowStyle Hidden -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'temp\python_installer.exe'; exit $LASTEXITCODE}"
    
    if not exist "temp\python_installer.exe" (
        echo.
        echo ❌ Failed to download Python. Trying alternative method...
        echo.
        
        :: Try using curl as fallback
        curl -L -o "temp\python_installer.exe" "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" >nul 2>&1
        
        if not exist "temp\python_installer.exe" (
            echo ❌ ERROR: Cannot download Python installer!
            echo 🌐 Please check your internet connection.
            echo.
            echo 📖 Manual installation steps:
            echo   1. Go to: https://python.org/downloads/
            echo   2. Download Python 3.8 or higher
            echo   3. ✅ CHECK: "Add Python to PATH" during installation
            echo   4. Run this script again
            echo.
            pause
            exit /b 1
        )
    )
    
    echo ✅ Download complete!
    
    :: Install Python silently
    echo 🔧 Installing Python silently...
    echo ⚠️  DO NOT CLOSE this window! Installation in progress...
    
    start /wait temp\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0 Include_launcher=1
    
    :: Clean up
    del /q temp\python_installer.exe
    rmdir temp 2>nul
    
    :: Refresh PATH variables
    echo 🔄 Refreshing system environment...
    call :RefreshPath
    
    :: Wait a moment for installation to settle
    timeout /t 5 /nobreak >nul
    
    :: Verify installation
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ❌ Python installation verification failed!
        echo.
        echo 🔄 Please try these steps:
        echo   1. Restart your computer
        echo   2. Run this script again
        echo   3. If still failing, install manually from python.org
        echo.
        pause
        exit /b 1
    )
    
    echo ✅ Python successfully installed!
    
) else (
    echo ✅ Python is already installed!
)

:: Check Python version
echo [2/7] 🔍 Verifying Python version compatibility...
python -c "import sys; print('Python', sys.version.split()[0]); exit(0 if sys.version_info >= (3, 8) else 1)" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ Python version is too old for this dashboard!
    echo 📋 Required: Python 3.8 or higher
    echo 🔄 The installer will update Python automatically...
    echo.
    
    :: Force reinstall newer version
    goto InstallPython
)

echo ✅ Python version is compatible!

:: Remove old environment if exists
echo [3/7] 🧹 Preparing clean environment...
if exist "venv" (
    echo 🗑️  Removing old installation...
    rmdir /s /q venv 2>nul
)

if exist "__pycache__" (
    rmdir /s /q __pycache__ 2>nul
)

if exist "network_devices.db" (
    echo 🗑️  Removing old database (fresh start)...
    del /q network_devices.db 2>nul
)

echo ✅ Environment cleaned!

:: Create virtual environment
echo [4/7] 🏗️  Creating isolated Python environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo ❌ Failed to create Python environment!
    echo 🔧 This might be a permission issue.
    echo.
    echo 💡 Try these solutions:
    echo   1. Run as Administrator (recommended)
    echo   2. Check antivirus isn't blocking Python
    echo   3. Ensure enough disk space (1GB needed)
    echo.
    pause
    exit /b 1
)

echo ✅ Python environment created!

:: Activate environment
echo [5/7] ⚡ Activating environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate Python environment!
    pause
    exit /b 1
)

:: Upgrade pip
echo 📦 Upgrading package manager...
python -m pip install --upgrade pip --quiet --disable-pip-version-check

echo ✅ Environment activated!

:: Install requirements
echo [6/7] 📦 Installing dashboard components...
echo ⏳ This may take 2-4 minutes depending on internet speed...
echo.

pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Failed to install required packages!
    echo.
    echo 🌐 Common causes:
    echo   • Internet connection issues
    echo   • Firewall blocking downloads
    echo   • Antivirus blocking installation
    echo.
    echo 🔄 Try running this script again.
    pause
    exit /b 1
)

echo ✅ All components installed successfully!

:: Start the dashboard
echo [7/7] 🚀 Starting your Network Dashboard...
echo.
echo ⚡ Initializing dashboard server...

:: Start the Flask app in background
start /min python app.py

:: Wait for server startup
echo ⏳ Waiting for dashboard to initialize...
timeout /t 5 /nobreak >nul

:: Test if server is running
echo 🔍 Verifying dashboard startup...
powershell -Command "try { (Invoke-WebRequest -Uri 'http://localhost:5000' -TimeoutSec 5).StatusCode } catch { 500 }" >nul 2>&1

:: Open browser
echo 🌐 Opening dashboard in your browser...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo ██████████████████████████████████████████████████████████████████████████████
echo                                  🎉 SUCCESS! 🎉
echo ██████████████████████████████████████████████████████████████████████████████
echo.
echo ✅ Your Network Device Dashboard is now RUNNING!
echo.
echo 🌐 Dashboard URL: http://localhost:5000
echo 📱 Browser opened automatically
echo.
echo 🎯 WHAT HAPPENS NEXT:
echo   📡 Dashboard is scanning YOUR network right now
echo   🔍 Devices will appear automatically (usually within 30 seconds)
echo   📊 Click around and explore all the features!
echo.
echo 🎮 DASHBOARD FEATURES:
echo   📱 Real-time device monitoring
echo   🏷️  Device grouping and organization  
echo   📈 Network statistics and charts
echo   🔍 Advanced search and filtering
echo   📋 Export device lists
echo   📊 Historical performance tracking
echo.
echo ⚠️  IMPORTANT: Keep this window OPEN while using the dashboard!
echo    Closing this window will stop the dashboard.
echo.
echo 🛑 TO STOP: Close this window or press Ctrl+C
echo 🔄 TO RESTART: Run this file again anytime
echo.
echo 📚 NEED HELP?
echo   📖 USER_MANUAL.md - Complete guide to all features
echo   🔧 TROUBLESHOOTING_GUIDE.md - Solutions to common issues
echo   💼 DELIVERY_PACKAGE_SUMMARY.md - Professional overview
echo.
echo 💡 TIP: Bookmark http://localhost:5000 for quick access!
echo.

:: Function to refresh PATH environment variable
:RefreshPath
for /f "tokens=2*" %%i in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%j"
for /f "tokens=2*" %%i in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%j"
if defined UserPath (
    set "PATH=%UserPath%;%SysPath%"
) else (
    set "PATH=%SysPath%"
)
goto :eof

echo 🎉 Enjoy your professional Network Device Dashboard!
echo.
pause