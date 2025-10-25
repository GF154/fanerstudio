@echo off
REM Deployment script for Windows
REM Usage: deploy.bat [environment]

setlocal enabledelayedexpansion

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   🇭🇹 Pwojè Kreyòl IA - Deployment Script (Windows)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Get environment
set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=development

echo [INFO] Deploying to: %ENVIRONMENT%
echo.

REM Step 1: Check Docker
echo [INFO] Step 1: Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are installed
echo.

REM Step 2: Build Docker image
echo [INFO] Step 2: Building Docker image...
docker build -t kreyol-ai:latest . || (
    echo [ERROR] Docker build failed
    exit /b 1
)

echo [SUCCESS] Docker image built
echo.

REM Step 3: Stop existing containers
echo [INFO] Step 3: Stopping existing containers...
docker-compose down

echo [SUCCESS] Containers stopped
echo.

REM Step 4: Start services
echo [INFO] Step 4: Starting services...
docker-compose up -d --build

echo [SUCCESS] Services started
echo.

REM Step 5: Wait for services
echo [INFO] Step 5: Waiting for services to be ready...
timeout /t 15 /nobreak >nul

echo [SUCCESS] Services should be ready
echo.

REM Step 6: Display status
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [SUCCESS] Deployment completed!
echo.
echo [INFO] Services:
echo   📡 API:        http://localhost:8000
echo   📚 API Docs:   http://localhost:8000/docs
echo   🖥️  GUI:        http://localhost:8501
echo.
echo [INFO] Management commands:
echo   View logs:     docker-compose logs -f
echo   Stop services: docker-compose down
echo   Restart:       docker-compose restart
echo.
echo [SUCCESS] Deployment finished! 🚀
echo.

endlocal

