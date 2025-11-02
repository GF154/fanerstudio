@echo off
chcp 65001 >nul
cls
echo.
echo ════════════════════════════════════════════════════════════
echo   🚀 FANER STUDIO - AUTO DEPLOY TO GITHUB & RENDER
echo ════════════════════════════════════════════════════════════
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found! Please install Git first.
    pause
    exit /b 1
)

echo 📊 Checking for changes...
echo.

REM Show status
git status --short

echo.
echo ════════════════════════════════════════════════════════════

REM Check if there are changes
git diff-index --quiet HEAD --
if errorlevel 1 (
    echo ✅ Changes detected! Proceeding with deployment...
    echo.
    
    REM Ask for commit message
    set /p commit_msg="📝 Enter commit message (or press Enter for auto-message): "
    
    if "%commit_msg%"=="" (
        REM Generate auto commit message with timestamp
        for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
        for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)
        set commit_msg=🔄 Auto-deploy - !mydate! !mytime!
    )
    
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   📦 STAGE 1: ADDING FILES
    echo ════════════════════════════════════════════════════════════
    echo.
    
    git add .
    
    if errorlevel 1 (
        echo ❌ Error adding files!
        pause
        exit /b 1
    )
    
    echo ✅ All files staged successfully!
    echo.
    
    echo ════════════════════════════════════════════════════════════
    echo   💾 STAGE 2: COMMITTING CHANGES
    echo ════════════════════════════════════════════════════════════
    echo.
    echo Commit message: %commit_msg%
    echo.
    
    git commit -m "%commit_msg%"
    
    if errorlevel 1 (
        echo ❌ Error committing changes!
        pause
        exit /b 1
    )
    
    echo ✅ Changes committed successfully!
    echo.
    
    echo ════════════════════════════════════════════════════════════
    echo   🚀 STAGE 3: PUSHING TO GITHUB
    echo ════════════════════════════════════════════════════════════
    echo.
    
    git push origin master
    
    if errorlevel 1 (
        echo.
        echo ❌ Error pushing to GitHub!
        echo.
        echo 💡 Possible solutions:
        echo    1. Check your internet connection
        echo    2. Verify GitHub credentials
        echo    3. Make sure you have push access to the repository
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    
    echo ════════════════════════════════════════════════════════════
    echo   🎉 DEPLOYMENT COMPLETE!
    echo ════════════════════════════════════════════════════════════
    echo.
    echo ✅ Git Status: Pushed to master
    echo 🔄 GitHub Actions: Validating code...
    echo 🚀 Render: Auto-deploying...
    echo ⏱️  ETA: 3-5 minutes
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   📍 MONITOR DEPLOYMENT
    echo ════════════════════════════════════════════════════════════
    echo.
    echo Would you like to open deployment monitoring pages?
    echo.
    set /p open_pages="Open monitoring pages? (Y/N): "
    
    if /i "%open_pages%"=="Y" (
        echo.
        echo Opening monitoring pages...
        start "" "https://github.com/GF154/fanerstudio/actions"
        timeout /t 2 /nobreak >nul
        start "" "https://dashboard.render.com"
        timeout /t 2 /nobreak >nul
        start "" "https://fanerstudio-1.onrender.com"
        echo.
        echo ✅ Pages opened!
    )
    
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   🌐 DEPLOYMENT LINKS
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 🤖 GitHub Actions:
    echo    https://github.com/GF154/fanerstudio/actions
    echo.
    echo 📊 Render Dashboard:
    echo    https://dashboard.render.com
    echo.
    echo 🌐 Live Platform:
    echo    https://fanerstudio-1.onrender.com
    echo.
    echo 📚 API Documentation:
    echo    https://fanerstudio-1.onrender.com/docs
    echo.
    echo ════════════════════════════════════════════════════════════
    
) else (
    echo ℹ️  No changes detected in working directory.
    echo.
    echo Current status: Clean working tree ✅
    echo.
    echo 💡 Make some changes to your files and run this script again.
    echo.
)

echo.
echo Press any key to exit...
pause >nul

