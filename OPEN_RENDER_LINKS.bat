@echo off
REM 🚀 Quick Links - Faner Studio Deployment

echo.
echo ================================================
echo   🇭🇹 Faner Studio - Quick Access Links
echo ================================================
echo.

echo Opening deployment resources...
echo.

REM Render Dashboard
echo 1. Opening Render Dashboard...
start https://dashboard.render.com

timeout /t 2 /nobreak > nul

REM GitHub Actions
echo 2. Opening GitHub Actions...
start https://github.com/GF154/fanerstudio/actions

timeout /t 2 /nobreak > nul

REM HuggingFace (for API key)
echo 3. Opening HuggingFace Settings...
start https://huggingface.co/settings/tokens

echo.
echo ================================================
echo   ✅ All links opened in your browser!
echo ================================================
echo.
echo What's next:
echo   1. Login to Render Dashboard
echo   2. Create new Web Service
echo   3. Connect GitHub (GF154/fanerstudio)
echo   4. Deploy!
echo.
echo See RENDER_SETUP_GUIDE.md for detailed steps
echo.
pause

