@echo off
:: Launch Faner Studio Platform
:: Opens all platform pages in browser

echo.
echo ========================================
echo   LAUNCHING FANER STUDIO PLATFORM
echo ========================================
echo.

echo Opening main platform...
start "" "https://fanerstudio-1.onrender.com"
timeout /t 2 /nobreak >nul

echo Opening admin dashboard...
start "" "https://fanerstudio-1.onrender.com/admin"
timeout /t 2 /nobreak >nul

echo Opening API documentation...
start "" "https://fanerstudio-1.onrender.com/docs"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   PLATFORM LAUNCHED!
echo ========================================
echo.
echo Pages opened:
echo   1. Main Platform
echo   2. Admin Dashboard
echo   3. API Documentation
echo.
echo If pages didn't open automatically,
echo copy and paste these URLs:
echo.
echo Main:  https://fanerstudio-1.onrender.com
echo Admin: https://fanerstudio-1.onrender.com/admin
echo Docs:  https://fanerstudio-1.onrender.com/docs
echo.
pause

