@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        💾 REDIS SERVER - KREYÒL IA v4.0                   ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 KONSÈNAN REDIS:
echo    • In-memory cache (100x pi rapid ke file)
echo    • Message broker pou Celery
echo    • Shared cache between instances
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🔧 OPSYON POU LANCE REDIS:
echo.
echo    1. Docker (REKÒMANDE)
echo       docker run -d -p 6379:6379 redis:latest
echo.
echo    2. Windows Native
echo       • Telechaje: https://github.com/microsoftarchive/redis/releases
echo       • Ekstrè redis-server.exe
echo       • Lance: redis-server.exe
echo.
echo    3. WSL2 (Windows Subsystem for Linux)
echo       wsl sudo service redis-server start
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 💡 APRE REDIS LANCE:
echo    • Lance Celery worker: CELERY_START.bat
echo    • Lance aplikasyon: python app/main.py
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🔍 Verifye si Docker disponib...
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Docker detekte!
    echo.
    set /p choice="Vle lance Redis ak Docker? (O/N): "
    if /i "%choice%"=="O" (
        echo.
        echo 🚀 Lance Redis container...
        docker run -d -p 6379:6379 --name kreyolia-redis redis:latest
        echo.
        echo ✅ Redis ap kouri sou pò 6379!
        echo.
        echo 💡 POU RETE REDIS:
        echo    docker stop kreyolia-redis
        echo.
        echo 💡 POU EFASE REDIS:
        echo    docker rm kreyolia-redis
    )
) else (
    echo ⚠️  Docker pa detekte
    echo    Swiv opsyon 2 oswa 3 anwo
)
echo.
pause

