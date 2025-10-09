@echo off
echo Building Newsletter Application Executable...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build executable using spec file
pyinstaller --clean newsletter.spec

echo.
echo Build complete! 
echo Executable location: dist\NewsletterApp.exe
echo.
echo To run the application, navigate to the dist folder and run NewsletterApp.exe
echo The web interface will be available at http://localhost:5000
echo.
pause