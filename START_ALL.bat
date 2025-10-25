@echo off
chcp 65001 > nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🚀 KREYÒL IA - LANCE TOUT NAN YON SÈL TERMINAL        ║
echo ║                   VERSION 4.1.0                                ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 SA SCRIPT SA AP FÈ:
echo    1. ✅ Lance Redis (si Docker disponib)
echo    2. ✅ Lance Celery Worker (background)
echo    3. ✅ Lance Aplikasyon FastAPI
echo    4. ✅ Ouvri navigatè otomatikman
echo.
echo ⚠️  NÒTE: Tout bagay ap kouri nan yon sèl terminal!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
echo 🔍 Verifye Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python pa enstale!
    echo    Telechaje Python: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python detekte

REM Check if in correct directory
if not exist "app\main.py" (
    echo ❌ Pa nan bon dosye!
    echo    Ale nan dosye projet_kreyol_IA
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🔧 ETAP 1: PREPARE ANVIWÒNMAN
echo.

REM Create output directories
if not exist "output" mkdir output
if not exist "output\videos" mkdir output\videos
if not exist "output\chunks" mkdir output\chunks
if not exist "logs" mkdir logs

echo ✅ Dosye yo prepare

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🐳 ETAP 2: LANCE REDIS (OPTIONAL)
echo.

REM Try to start Redis with Docker
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Docker detekte
    echo 🚀 Lance Redis container...
    
    REM Stop existing container if any
    docker stop kreyolia-redis >nul 2>&1
    docker rm kreyolia-redis >nul 2>&1
    
    REM Start new container
    docker run -d -p 6379:6379 --name kreyolia-redis redis:latest >nul 2>&1
    
    if %errorlevel% == 0 (
        echo ✅ Redis ap kouri sou pò 6379!
        timeout /t 2 /nobreak >nul
    ) else (
        echo ⚠️  Pa ka lance Redis
        echo    Platfòm ap itilize memory fallback
    )
) else (
    echo ⚠️  Docker pa disponib
    echo    Redis pa disponib - itilize memory fallback
    echo    Pou enstale Docker: https://www.docker.com/get-started
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🔄 ETAP 3: LANCE CELERY WORKER (BACKGROUND)
echo.

REM Check if Redis is available for Celery
python -c "import redis; r=redis.Redis(); r.ping()" >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Redis konekte - lance Celery worker...
    
    REM Start Celery in background
    start /B "Celery Worker" cmd /c "celery -A app.tasks worker --loglevel=info --pool=solo > logs\celery.log 2>&1"
    
    echo ✅ Celery worker ap kouri nan background
    timeout /t 3 /nobreak >nul
) else (
    echo ⚠️  Redis pa disponib
    echo    Celery worker pa disponib - background jobs pa ap mache
    echo    Fonksyonalite synchronous ap travay nòmalman
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 ETAP 4: LANCE APLIKASYON FASTAPI
echo.

echo 📱 Aplikasyon ap kòmanse...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Wait a moment then open browser
start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"

REM Start the application (this will keep the terminal open)
python app\main.py

REM Cleanup on exit
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🧹 NETWAYAJ...
echo.

REM Stop Redis container
docker stop kreyolia-redis >nul 2>&1
docker rm kreyolia-redis >nul 2>&1

REM Kill any remaining Celery processes
taskkill /F /FI "WINDOWTITLE eq Celery Worker*" >nul 2>&1

echo ✅ Tout bagay rete pwòp!
echo.
pause

