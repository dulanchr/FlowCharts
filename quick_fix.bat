@echo off
echo =====================================================
echo   Flowchart Web Application - Quick Fix
echo =====================================================
echo.

echo Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    goto :error
) else (
    echo ✓ Python is available
)

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ pip is not available
    echo Please reinstall Python with pip
    goto :error
) else (
    echo ✓ pip is available
)

REM Check fonts directory
if not exist "fonts" (
    echo ✗ fonts directory not found
    echo Creating fonts directory...
    mkdir fonts
)

REM Check font files
if not exist "fonts\NotoSans-Regular.ttf" (
    if not exist "fonts\SFUIText-Regular.otf" (
        echo ✗ No font files found
        echo Please copy font files to the fonts directory
        goto :error
    )
)
echo ✓ Font files found

REM Install/update requirements
echo.
echo Installing/updating requirements...
pip install -r web_requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install requirements
    goto :error
) else (
    echo ✓ Requirements installed
)

REM Test core functionality
echo.
echo Testing core functionality...
python -c "from Converter import generate_flowchart_direct; print('✓ Core functionality available')"
if errorlevel 1 (
    echo ✗ Core functionality test failed
    goto :error
) else (
    echo ✓ Core functionality test passed
)

REM Clean up temporary files
echo.
echo Cleaning up temporary files...
del /q "%TEMP%\temp_*.txt" >nul 2>&1
del /q "%TEMP%\temp_*.png" >nul 2>&1
echo ✓ Temporary files cleaned

echo.
echo =====================================================
echo   All checks passed! Your system is ready.
echo =====================================================
echo.
echo You can now start the application with:
echo   python app.py
echo.
echo Or use the menu:
echo   start_menu.bat
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
pause
goto :end

:error
echo.
echo =====================================================
echo   Issues found. Please fix them and try again.
echo =====================================================
echo.
pause

:end
