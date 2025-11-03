@echo off
:: Test Supabase Connection
:: Quick script to verify Supabase integration

echo.
echo ========================================
echo    TESTING SUPABASE CONNECTION
echo ========================================
echo.
echo Wait 5 minutes after deployment starts
echo Then run this test to verify connection
echo.
pause

python test_supabase_connection.py

echo.
echo ========================================
echo Test complete!
echo ========================================
echo.
pause

