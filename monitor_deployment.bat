@echo off
REM ================================================================
REM 🔄 Auto-Refresh Deployment Monitor
REM Opens GitHub Actions & Render Dashboard with auto-refresh
REM ================================================================

echo.
echo ════════════════════════════════════════════════════════════
echo 🔄 FANER STUDIO - DEPLOYMENT MONITOR
echo ════════════════════════════════════════════════════════════
echo.
echo 📊 Opening monitoring pages with auto-refresh...
echo.

REM Open GitHub Actions (auto-refresh every 30 seconds)
echo [1/3] Opening GitHub Actions...
start "" "https://github.com/GF154/fanerstudio/actions"

timeout /t 2 /nobreak >nul

REM Open Render Dashboard
echo [2/3] Opening Render Dashboard...
start "" "https://dashboard.render.com"

timeout /t 2 /nobreak >nul

REM Open Live Platform
echo [3/3] Opening Live Platform...
start "" "https://fanerstudio-1.onrender.com"

echo.
echo ════════════════════════════════════════════════════════════
echo ✅ MONITORING PAGES OPENED
echo ════════════════════════════════════════════════════════════
echo.
echo 📍 Pages opened:
echo    [1] GitHub Actions - Check workflow status
echo    [2] Render Dashboard - Monitor build progress
echo    [3] Live Platform - Test deployed features
echo.
echo 🔄 Refresh pages manually (F5) to see updates
echo ⏱️  Deployment takes ~3-5 minutes
echo.
echo 💡 TIP: Keep this window open for quick access
echo.

:MENU
echo ════════════════════════════════════════════════════════════
echo 🎯 QUICK ACTIONS:
echo ════════════════════════════════════════════════════════════
echo.
echo [1] Refresh all pages
echo [2] Open GitHub Actions only
echo [3] Open Render Dashboard only
echo [4] Open Live Platform only
echo [5] Check deployment status
echo [6] Exit
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto REFRESH_ALL
if "%choice%"=="2" goto OPEN_GITHUB
if "%choice%"=="3" goto OPEN_RENDER
if "%choice%"=="4" goto OPEN_LIVE
if "%choice%"=="5" goto CHECK_STATUS
if "%choice%"=="6" goto EXIT

echo ❌ Invalid option. Try again.
goto MENU

:REFRESH_ALL
echo.
echo 🔄 Refreshing all pages...
start "" "https://github.com/GF154/fanerstudio/actions"
timeout /t 1 /nobreak >nul
start "" "https://dashboard.render.com"
timeout /t 1 /nobreak >nul
start "" "https://fanerstudio-1.onrender.com"
echo ✅ Pages refreshed!
echo.
timeout /t 2 /nobreak >nul
goto MENU

:OPEN_GITHUB
echo.
echo 📊 Opening GitHub Actions...
start "" "https://github.com/GF154/fanerstudio/actions"
echo ✅ Done!
echo.
timeout /t 2 /nobreak >nul
goto MENU

:OPEN_RENDER
echo.
echo 🚀 Opening Render Dashboard...
start "" "https://dashboard.render.com"
echo ✅ Done!
echo.
timeout /t 2 /nobreak >nul
goto MENU

:OPEN_LIVE
echo.
echo 🌐 Opening Live Platform...
start "" "https://fanerstudio-1.onrender.com"
echo ✅ Done!
echo.
timeout /t 2 /nobreak >nul
goto MENU

:CHECK_STATUS
echo.
echo 📊 Checking deployment status...
echo.
git log --oneline -3
echo.
echo 📍 Latest commits shown above
echo 🔗 Check GitHub Actions for workflow status
echo 🔗 Check Render Dashboard for build status
echo.
timeout /t 3 /nobreak >nul
goto MENU

:EXIT
echo.
echo 👋 Exiting deployment monitor...
echo ✅ Keep checking your pages for deployment updates!
echo.
timeout /t 2 /nobreak >nul
exit

