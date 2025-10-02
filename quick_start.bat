@echo off
title Network Device Dashboard - Starting...

echo ============================================
echo Network Device Dashboard
echo ============================================
echo.
echo Initializing dashboard for your network...
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo.
    echo This usually means the dashboard hasn't been installed yet.
    echo.
    echo Please run: install_dependencies.bat first
    echo.
    echo Steps:
    echo   1. Right-click "install_dependencies.bat"
    echo   2. Select "Run as administrator"
    echo   3. Wait for installation to complete
    echo   4. Then run this script again
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Initialize database (if needed)
echo Preparing database...
python -c "from database import DatabaseManager; db = DatabaseManager(); db.init_database()" >nul 2>&1

:: Start the application
echo Starting dashboard server...
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                 Network Device Dashboard                 ║
echo ║                                                          ║
echo ║  🌐 Dashboard URL: http://localhost:5000                 ║
echo ║                                                          ║
echo ║  📊 The dashboard will automatically detect and scan     ║
echo ║     YOUR network (not the developer's network)          ║
echo ║                                                          ║
echo ║  🔍 Network auto-detection:                              ║
echo ║     • Home networks (192.168.x.x)                       ║
echo ║     • Office networks (10.x.x.x)                        ║
echo ║     • Corporate networks (172.16.x.x)                   ║
echo ║                                                          ║
echo ║  ⏹️  Press Ctrl+C to stop the server                     ║
echo ║                                                          ║
echo ║  📖 Need help? Check the Documentation folder           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Give user a moment to read the information
timeout /t 3 /nobreak >nul

echo Starting in 3 seconds...
timeout /t 1 /nobreak >nul
echo Starting in 2 seconds...
timeout /t 1 /nobreak >nul
echo Starting in 1 second...
timeout /t 1 /nobreak >nul

echo.
echo ✅ Dashboard is now running!
echo.
echo 👉 Open your web browser and go to: http://localhost:5000
echo.

python app.py

echo.
echo Dashboard has stopped.
echo.
pause