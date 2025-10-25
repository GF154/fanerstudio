@echo off
chcp 65001 > nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║       🧪 KREYÒL IA - TEST COVERAGE                       ║
echo ║       Run Tests with Coverage Report                      ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

SET SCRIPT_DIR=%~dp0

echo 📋 Running tests with coverage...
echo.

REM Run pytest with coverage
python -m pytest "%SCRIPT_DIR%tests\test_services.py" ^
  --cov=app ^
  --cov-report=html ^
  --cov-report=term ^
  -v

echo.
echo ═══════════════════════════════════════════════════════════
echo ✅ Tests completed!
echo 📊 Coverage report: htmlcov\index.html
echo ═══════════════════════════════════════════════════════════
echo.

REM Open coverage report in browser
start "" "%SCRIPT_DIR%htmlcov\index.html"

pause

