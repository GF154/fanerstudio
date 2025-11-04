@echo off
REM 🔍 Production Health Check

echo.
echo ====================================
echo 🏥 Production Health Check
echo ====================================
echo.

set /p URL="Enter production URL (e.g., https://fanerstudio.vercel.app): "

echo.
echo Running health checks on: %URL%
echo.

python production_health_check.py %URL%

echo.
pause

