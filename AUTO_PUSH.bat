@echo off
REM 🚀 AUTO PUSH - Automatic Git Push
REM Start auto-push in background

echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 STARTING AUTO PUSH SERVICE                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.
echo 📦 Installing dependencies...
pip install watchdog --quiet

echo.
echo 🚀 Starting auto-push...
echo.
echo Press Ctrl+C to stop
echo.

python auto_push.py

pause

