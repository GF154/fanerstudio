@echo off
chcp 65001 >nul
cls

echo.
echo ════════════════════════════════════════════════════════════
echo   🤖 FANER STUDIO - AUTO WATCH ^& DEPLOY
echo   Automatic deployment on file changes
echo ════════════════════════════════════════════════════════════
echo.
echo 🔄 Mode: AUTOMATIC
echo 👁️  Watching: All project files
echo ⏱️  Check interval: 10 seconds
echo 🚀 Auto-push: Enabled
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.
echo 🚀 Starting auto-watch service...
echo.
echo ════════════════════════════════════════════════════════════
echo   Press Ctrl+C to stop watching
echo ════════════════════════════════════════════════════════════
echo.

REM Run the Python auto-watch script
python auto_watch_deploy.py

echo.
echo Auto-watch stopped.
pause

