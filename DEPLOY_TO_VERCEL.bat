@echo off
REM 🚀 Quick Deployment Script for Vercel

echo.
echo ============================================
echo 🚀 FANER STUDIO - Vercel Deployment
echo ============================================
echo.

echo Step 1: Checking Vercel CLI...
vercel --version
echo.

echo Step 2: Logging in to Vercel...
echo (Browser will open for authentication)
vercel login
echo.

echo Step 3: Deploying to production...
echo.
echo This will deploy your app to Vercel production!
echo.
pause

vercel --prod

echo.
echo ============================================
echo ✅ Deployment Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Go to Vercel Dashboard: https://vercel.com/dashboard
echo 2. Add environment variables (see PHASE1_DEPLOYMENT_GUIDE.md)
echo 3. Redeploy: vercel --prod
echo 4. Test: python production_health_check.py [your-url]
echo.

pause

