@echo off
chcp 65001 > nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║       🧪 KREYÒL IA - TEST SUITE                          ║
echo ║       Run Automated Tests                                 ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

SET SCRIPT_DIR=%~dp0

echo 📋 Running tests...
echo.

REM Run pytest with verbose output
python -m pytest "%SCRIPT_DIR%tests\test_services.py" -v --tb=short

echo.
echo ═══════════════════════════════════════════════════════════
echo Tests completed!
echo ═══════════════════════════════════════════════════════════
echo.

pause

