@echo off
echo Building and starting Flowchart Web Application with Docker...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)

cd /d "%~dp0"

echo Building Docker image...
docker-compose build

if errorlevel 1 (
    echo Error building Docker image
    pause
    exit /b 1
)

echo Starting application...
docker-compose up -d

if errorlevel 1 (
    echo Error starting application
    pause
    exit /b 1
)

echo.
echo Application is starting...
echo It will be available at: http://localhost:5000
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f
echo.
pause
