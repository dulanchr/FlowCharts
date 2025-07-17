@echo off
echo Creating executable for Flowchart Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Kill any running instances of the executable
taskkill /f /im FlowchartGenerator.exe >nul 2>&1

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Create executable using PyInstaller
echo.
echo Creating executable...
pyinstaller flowchart_gui.spec

REM Check if build was successful
if exist "dist\FlowchartGenerator.exe" (
    echo.
    echo Build successful!
    echo Executable created: dist\FlowchartGenerator.exe
    echo.
    echo You can now run the executable from the dist folder.
    echo The previous file access issues have been fixed.
    pause
) else (
    echo.
    echo Build failed. Please check the error messages above.
    pause
)
