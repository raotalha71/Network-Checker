@echo off
title Network Device Dashboard

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Start the application
echo Starting Network Device Dashboard...
echo.
echo The dashboard will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py