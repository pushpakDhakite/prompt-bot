@echo off
echo ========================================
echo    AI Prompt Generator Pro
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install packages
        pause
        exit /b 1
    )
)

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Start the application
echo.
echo Starting AI Prompt Generator Pro...
echo.
python run_gui.py

pause