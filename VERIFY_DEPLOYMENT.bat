@echo off
:: Verify Render Deployment Configuration
:: Diagnostic tool to identify deployment issues

echo.
echo ========================================
echo   RENDER DEPLOYMENT VERIFICATION
echo ========================================
echo.
echo This will check:
echo   - Local configuration files
echo   - Render service status
echo   - All API endpoints
echo   - Deployment issues
echo.
pause

python verify_deployment.py

echo.
echo ========================================
echo Verification Complete!
echo ========================================
echo.
echo Follow the recommendations above to fix any issues.
echo.
pause

