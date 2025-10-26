@echo off
chcp 65001 > nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║          🚀 KREYÒL IA - LANCE RAPID (YON TERMINAL)           ║
echo ║                   VERSION SENP 4.1.0                           ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 💡 VÈSYON SA A:
echo    • Pa bezwen Redis
echo    • Pa bezwen Celery
echo    • Pa bezwen Docker
echo    • Fonksyone imedyatman!
echo.
echo ⚙️  FONKSYONALITE:
echo    ✅ Audiobook Creation (synchrone)
echo    ✅ Podcast Generation
echo    ✅ Text-to-Speech
echo    ✅ Speech-to-Text
echo    ✅ Video Processing (si ffmpeg disponib)
echo    ✅ AI Script Generation (si API key disponib)
echo    ✅ Translation
echo.
echo ⚠️  PA GEN:
echo    ❌ Background jobs (timeout 60s)
echo    ❌ Redis cache (itilize memory)
echo    ❌ Real-time WebSocket
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 Lance aplikasyon...
echo.

REM Create directories
if not exist "output" mkdir output
if not exist "output\videos" mkdir output\videos
if not exist "logs" mkdir logs

REM Open browser after 5 seconds
start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"

REM Start application
python app\main.py

echo.
pause

