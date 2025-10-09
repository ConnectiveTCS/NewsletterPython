@echo off
title Newsletter Application
echo ====================================
echo    Newsletter Application v1.0
echo ====================================
echo.
echo Initializing the Newsletter Application...
echo.
echo The application will:
echo - Set up the database automatically
echo - Start the web server on port 5000
echo - Create sample data for first-time users
echo.
echo Once started, open your web browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C in this window to stop the application
echo ====================================
echo.

REM Change to the dist directory and run the executable
cd /d "%~dp0dist"
if not exist NewsletterApp.exe (
    echo ERROR: NewsletterApp.exe not found!
    echo Make sure the executable has been built properly.
    echo Run build_executable.bat first to create the executable.
    pause
    exit /b 1
)

NewsletterApp.exe

echo.
echo ====================================
echo Newsletter Application has stopped.
echo Thank you for using our software!
echo ====================================
pause