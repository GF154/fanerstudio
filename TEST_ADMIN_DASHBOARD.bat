@echo off
:: Test Admin Dashboard
:: Quick script to test admin dashboard functionality

echo.
echo ========================================
echo    TESTING ADMIN DASHBOARD
echo ========================================
echo.
echo This will test all admin endpoints
echo.
pause

python test_admin_dashboard.py

echo.
echo ========================================
echo Test complete!
echo ========================================
echo.
echo To access admin dashboard:
echo   http://localhost:8000/admin
echo.
echo Or on Render:
echo   https://fanerstudio-1.onrender.com/admin
echo.
pause

