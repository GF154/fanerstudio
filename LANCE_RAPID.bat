@echo off
chcp 65001 > nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║           🚀 KREYÒL IA - LANCE RAPID v4.1.0                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Ap lance servè a...
echo.

cd /d "%~dp0"

REM Set PYTHONPATH
set PYTHONPATH=%CD%

REM Start server with uvicorn directly
echo ✅ Lance servè FastAPI...
python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

pause

