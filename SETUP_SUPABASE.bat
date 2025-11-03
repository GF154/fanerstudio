@echo off
chcp 65001 >nul
cls

echo.
echo ════════════════════════════════════════════════════════════
echo   🔥 SUPABASE SETUP - FANER STUDIO
echo   Interactive database configuration
echo ════════════════════════════════════════════════════════════
echo.
echo This will help you setup Supabase for Faner Studio!
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════
echo   OPTION 1: RUN INTERACTIVE SETUP
echo ════════════════════════════════════════════════════════════
echo.
echo This will guide you through each step.
echo.

set /p run_setup="Run interactive setup? (Y/N): "

if /i "%run_setup%"=="Y" (
    echo.
    echo Starting setup...
    python setup_supabase.py
    echo.
    pause
    exit /b 0
)

echo.
echo ════════════════════════════════════════════════════════════
echo   OPTION 2: OPEN DOCUMENTATION
echo ════════════════════════════════════════════════════════════
echo.

set /p open_docs="Open setup guide? (Y/N): "

if /i "%open_docs%"=="Y" (
    echo.
    echo Opening SUPABASE_SETUP_GUIDE.md...
    start SUPABASE_SETUP_GUIDE.md
)

echo.
echo ════════════════════════════════════════════════════════════
echo   QUICK LINKS
echo ════════════════════════════════════════════════════════════
echo.
echo 🌐 Supabase Dashboard: https://app.supabase.com
echo 📚 Supabase Docs: https://supabase.com/docs
echo 💬 Discord Support: https://discord.supabase.com
echo.

set /p open_supabase="Open Supabase website? (Y/N): "

if /i "%open_supabase%"=="Y" (
    echo.
    echo Opening Supabase...
    start https://supabase.com
)

echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

