@echo off
chcp 65001 > nul
echo ============================================================
echo 🇭🇹 KREYÒL IA STUDIO - PROFESSIONAL VERSION
echo ============================================================
echo.
echo 🚀 Lanse aplikasyon pwofesyonèl la...
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️  Virtual environment pa egziste!
    echo 📦 Kreye virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📥 Enstale dependencies...
    pip install -r requirements_studio.txt
) else (
    call venv\Scripts\activate.bat
)

echo.
echo ============================================================
echo ✅ Environment aktivè!
echo ============================================================
echo.
echo 🌐 Lance servè...
echo.

python -m app.main

pause

