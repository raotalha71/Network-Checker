@echo off
title Network Dashboard - Quick Launcher

echo.
echo ═══════════════════════════════════════
echo    🚀 NETWORK DASHBOARD LAUNCHER 🚀
echo ═══════════════════════════════════════
echo.

:: Check if already installed
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Dashboard not installed yet!
    echo.
    echo 🔧 Please run "ONE_CLICK_SETUP_AND_RUN.bat" first
    echo    to install everything automatically.
    echo.
    pause
    exit /b 1
)

echo ⚡ Starting Network Dashboard...

:: Activate environment
call venv\Scripts\activate.bat >nul 2>&1

:: Start dashboard
echo 🌐 Dashboard starting at: http://localhost:5000
echo.

start /min python app.py

:: Wait and open browser
timeout /t 3 /nobreak >nul
start http://localhost:5000

echo ✅ Dashboard is running!
echo.
echo 📱 Browser opened automatically
echo ⚠️  Keep this window open while using the dashboard
echo 🛑 To stop: Close this window or press Ctrl+C
echo.
pause