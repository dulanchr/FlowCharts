@echo off
echo.
echo ============================================
echo   Flowchart Web Application
echo ============================================
echo.
echo Choose an option:
echo.
echo 1. Start Web Application (Python)
echo 2. Test Web Application
echo 3. Start with Docker
echo 4. Install Requirements
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto start_app
if "%choice%"=="2" goto test_app
if "%choice%"=="3" goto start_docker
if "%choice%"=="4" goto install_req
if "%choice%"=="5" goto exit

:start_app
echo.
echo Starting Web Application...
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
goto end

:test_app
echo.
echo Testing Web Application...
python test_web_app.py
pause
goto end

:start_docker
echo.
echo Starting with Docker...
docker-compose up -d
if errorlevel 1 (
    echo Error: Docker is not available or not running
    echo Please install Docker Desktop or make sure it's running
    pause
    goto end
)
echo Application started with Docker
echo Available at: http://localhost:5000
echo To stop: docker-compose down
pause
goto end

:install_req
echo.
echo Installing Requirements...
pip install -r web_requirements.txt
if errorlevel 1 (
    echo Error installing requirements
    pause
    goto end
)
echo Requirements installed successfully
pause
goto end

:exit
echo.
echo Goodbye!
goto end

:end
echo.
pause
