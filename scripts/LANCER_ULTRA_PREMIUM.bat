@echo off
chcp 65001 > nul
cls
echo.
echo ============================================================
echo      🇭🇹 KREYÒL IA - ULTRA PREMIUM STUDIO
echo ============================================================
echo.
echo     ✨ Professional Content Creation Platform
echo     🎯 Native Haitian Creole AI Technology
echo.
echo ============================================================
echo.
echo 🚀 Initializing...
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Starting backend server...
echo.

start /B python api_final.py

timeout /t 3 >nul

echo [3/3] Opening application in browser...
start http://localhost:8000

echo.
echo ============================================================
echo ✅ APPLICATION LAUNCHED SUCCESSFULLY!
echo ============================================================
echo.
echo 🌐 Web Application:    http://localhost:8000
echo 📚 API Documentation:  http://localhost:8000/docs
echo.
echo Press any key to stop the server...
pause >nul

