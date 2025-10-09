# Newsletter Application - Executable Guide

## Overview
Your Newsletter Application has been successfully compiled into a standalone executable file that can run on Windows without requiring Python to be installed.

## Files Created
- `NewsletterApp.exe` - The main executable file (located in the `dist` folder)
- `build_executable.bat` - Script to rebuild the executable if needed
- `newsletter.spec` - PyInstaller configuration file
- `launcher.py` - Executable launcher script

## How to Run the Application

### Method 1: Run the Executable Directly
1. Navigate to the `dist` folder in your project directory
2. Double-click on `NewsletterApp.exe` or run it from command prompt
3. The application will start and display console output
4. Open your web browser and go to `http://localhost:5000`
5. The newsletter web interface will be available

### Method 2: Run from Command Prompt
```cmd
cd C:\NewsletterPython\dist
NewsletterApp.exe
```

## First Run Setup
When you run the executable for the first time:
1. The application will automatically set up the database
2. Sample data will be created for testing
3. The database file will be created in your user profile at:
   `%USERPROFILE%\NewsletterApp\newsletter.db`

## Application Features
- **Web Interface**: Access at http://localhost:5000
- **Subscriber Management**: Add, edit, and import subscribers
- **Template Management**: Create and manage email templates
- **Campaign Management**: Send newsletters to subscribers
- **Email Logs**: Track sent emails and delivery status

## Distribution
The `NewsletterApp.exe` file is completely standalone and can be:
- Copied to any Windows computer
- Run without installing Python or any dependencies
- Shared with other users
- Run from a USB drive or network location

## Database Location
- **Development mode**: Database stored locally in the application folder
- **Executable mode**: Database stored in `%USERPROFILE%\NewsletterApp\newsletter.db`

## Stopping the Application
- Press `Ctrl+C` in the console window, or
- Simply close the console window

## Rebuilding the Executable
If you make changes to the source code and want to rebuild:
1. Run `build_executable.bat`
2. The new executable will be created in the `dist` folder

## Troubleshooting
- **Port already in use**: If port 5000 is busy, the application will show an error. Change the port in the source code and rebuild.
- **Database errors**: Delete the database file in `%USERPROFILE%\NewsletterApp\` to reset
- **Missing templates**: Ensure all template files are included in the build process

## File Size
The executable is approximately 45-55 MB and includes:
- Python interpreter
- All required libraries
- Flask web framework
- SQLite database engine
- Email handling components
- All HTML templates and static files

## Security Notes
- The executable runs a local web server
- Only accessible from the local machine by default
- Database is stored locally and not encrypted
- Use appropriate firewall settings if needed

For technical support or questions, refer to the source code documentation.