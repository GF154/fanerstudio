@echo off
echo ========================================
echo   FANER STUDIO - DEPLOYMENT MONITOR
echo ========================================
echo.
echo Opening deployment monitoring pages...
echo.

REM Open GitHub Actions
start "" "https://github.com/GF154/fanerstudio/actions"

REM Wait 2 seconds
timeout /t 2 /nobreak > NUL

REM Open Render Dashboard
start "" "https://dashboard.render.com"

REM Wait 2 seconds
timeout /t 2 /nobreak > NUL

REM Open Live Platform
start "" "https://fanerstudio-1.onrender.com"

echo.
echo ========================================
echo   PAGES OPENED:
echo ========================================
echo   1. GitHub Actions
echo   2. Render Dashboard
echo   3. Live Platform
echo.
echo   Deployment ETA: 3-5 minutes
echo ========================================
echo.
pause

