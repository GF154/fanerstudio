@echo off
chcp 65001 > nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              🇭🇹 KÒMANSE ICI - CHWAZI OPSYON 🇭🇹              ║
echo ║                   KREYÒL IA v4.1.0                             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 CHWAZI KIJAN OU VLE LANCE PLATFÒM LAN:
echo.
echo    1️⃣  RAPID - Lance imedyatman (pa bezwen Docker/Redis)
echo        • Pi senp
echo        • Fonksyone tou suit
echo        • Timeout 60s pou gwo fichye
echo.
echo    2️⃣  KONPLÈ - Tout fonksyonalite (ak Redis + Celery)
echo        • Pa gen timeout
echo        • Background jobs
echo        • Cache 100x pi rapid
echo        • Bezwen Docker oswa Redis enstale
echo.
echo    3️⃣  SÈLMAN APLIKASYON - San Redis/Celery (manual)
echo        • Ou menm lance Redis/Celery si ou vle
echo        • Plis kontwòl
echo.
echo    4️⃣  EXIT - Soti
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
set /p choice="Chwazi opsyon (1/2/3/4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Lance vèsyon RAPID...
    echo.
    call START_ALL_SIMPLE.bat
    exit /b 0
)

if "%choice%"=="2" (
    echo.
    echo 🚀 Lance vèsyon KONPLÈ...
    echo.
    call START_ALL.bat
    exit /b 0
)

if "%choice%"=="3" (
    echo.
    echo 🚀 Lance aplikasyon sèlman...
    echo.
    
    REM Create directories
    if not exist "output" mkdir output
    if not exist "output\videos" mkdir output\videos
    if not exist "logs" mkdir logs
    
    REM Open browser
    start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"
    
    REM Start app
    python app\main.py
    exit /b 0
)

if "%choice%"=="4" (
    echo.
    echo 👋 Orevwa!
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo.
echo ❌ Opsyon pa valid! Chwazi 1, 2, 3, oswa 4.
timeout /t 3 /nobreak >nul
goto :eof

