@echo off
REM 🇭🇹 Faner Studio - Quick Deployment Check
REM Check deployment status

echo.
echo ================================================
echo   🇭🇹 Faner Studio - Deployment Checker
echo ================================================
echo.

python check_deployment.py

if errorlevel 1 (
    echo.
    echo ❌ Error running script
    echo Make sure Python is installed
    pause
)

