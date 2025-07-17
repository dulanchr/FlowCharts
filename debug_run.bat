@echo off
echo =====================================================
echo   Flowchart Web Application - Debugging Mode
echo =====================================================
echo.
echo Step 1: Testing core functionality...
echo.
python test_simple.py
echo.
echo Step 2: Starting Flask application with debug logging...
echo.
echo The application will be available at:
echo   Main app: http://localhost:5000
echo   Test page: http://localhost:5000/test
echo.
echo Check the console for debug messages.
echo Press Ctrl+C to stop the server.
echo.
python app.py
