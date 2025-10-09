@echo off
echo Newsletter Application - Windows Startup Script
echo ================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your email settings
    echo.
    choice /C YN /M "Continue without email configuration? (Y/N)"
    if errorlevel 2 exit /b 1
)

:: Start the application
echo.
echo Starting Newsletter Application...
echo Web interface will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
python run.py

pause