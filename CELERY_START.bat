@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        🔄 CELERY WORKER - KREYÒL IA v4.0                  ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 KONSÈNAN CELERY WORKER:
echo    • Pwosese background tasks (audiobook, etc.)
echo    • Evite timeout pou gwo fichye
echo    • Support pou multiple tasks an menm tan
echo.
echo ⚠️  NÒTE:
echo    • Redis dwe ap kouri (pò 6379)
echo    • Si Redis pa disponib, worker ap pa mache
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Check if Redis is running
echo 🔍 Verifye si Redis ap kouri...
python -c "import redis; r=redis.Redis(); r.ping(); print('✅ Redis connected!')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ Redis pa ap kouri!
    echo.
    echo 💡 POU LANCE REDIS:
    echo    • Option 1: docker run -d -p 6379:6379 redis:latest
    echo    • Option 2: Telechaje Redis pou Windows
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 LANCE CELERY WORKER...
echo.
echo ═══════════════════════════════════════════════════════════
echo.

celery -A app.tasks worker --loglevel=info --pool=solo

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Worker rete!
pause

