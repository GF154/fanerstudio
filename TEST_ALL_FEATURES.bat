@echo off
:: Test All Platform Features
:: Comprehensive integration test for all tools

echo.
echo ========================================
echo   TESTING ALL PLATFORM FEATURES
echo ========================================
echo.
echo This will test all tools:
echo   - Core endpoints
echo   - Translation
echo   - Performance monitoring
echo   - Voice & Audio
echo   - Authentication
echo.
pause

python test_all_features.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
pause

