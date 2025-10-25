@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🚀 KREYÒL IA - DEPLOYMENT TO RENDER.COM                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📋 PRE-DEPLOYMENT CHECKLIST:
echo.
echo ✅ 1. Git installed and configured
echo ✅ 2. GitHub account created
echo ✅ 3. Render.com account created
echo ✅ 4. All deployment files ready
echo.

pause

echo.
echo 🔍 CHECKING DEPLOYMENT FILES...
echo.

set "FILES_OK=1"

if exist "requirements.txt" (
    echo ✅ requirements.txt - Found
) else (
    echo ❌ requirements.txt - Missing!
    set "FILES_OK=0"
)

if exist "Procfile" (
    echo ✅ Procfile - Found
) else (
    echo ❌ Procfile - Missing!
    set "FILES_OK=0"
)

if exist "runtime.txt" (
    echo ✅ runtime.txt - Found
) else (
    echo ❌ runtime.txt - Missing!
    set "FILES_OK=0"
)

if exist "render.yaml" (
    echo ✅ render.yaml - Found
) else (
    echo ❌ render.yaml - Missing!
    set "FILES_OK=0"
)

if exist "app\api.py" (
    echo ✅ app\api.py - Found
) else (
    echo ❌ app\api.py - Missing!
    set "FILES_OK=0"
)

if exist ".gitignore" (
    echo ✅ .gitignore - Found
) else (
    echo ⚠️  .gitignore - Missing (will create)
    echo .env > .gitignore
    echo __pycache__/ >> .gitignore
    echo *.pyc >> .gitignore
    echo venv/ >> .gitignore
    echo output/ >> .gitignore
    echo cache/ >> .gitignore
    echo logs/ >> .gitignore
)

echo.

if "%FILES_OK%"=="0" (
    echo ❌ SOME FILES ARE MISSING!
    echo    Please make sure all required files exist.
    echo.
    pause
    exit /b 1
)

echo ✅ ALL DEPLOYMENT FILES READY!
echo.
pause

echo.
echo 📝 STEP 1: PREPARE GIT REPOSITORY
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed!
    echo    Download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

if not exist ".git" (
    echo 🔄 Initializing git repository...
    git init
    echo ✅ Repository initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo 🔄 Adding files to git...
git add .

echo.
echo 📝 Creating commit...
git commit -m "Deploy to Render.com - Kreyòl IA Platform v4.1"

echo.
echo ✅ Git repository prepared!
echo.

pause

echo.
echo 📝 STEP 2: PUSH TO GITHUB
echo.
echo Please follow these steps:
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: kreyol-ia-platform
echo 3. Visibility: Public (or Private if preferred)
echo 4. Click "Create repository"
echo.
echo 5. Copy the URL (should look like):
echo    https://github.com/YOUR_USERNAME/kreyol-ia-platform.git
echo.

set /p "REPO_URL=Paste your GitHub repository URL here: "

if "%REPO_URL%"=="" (
    echo ❌ No URL provided!
    pause
    exit /b 1
)

echo.
echo 🔄 Adding remote repository...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo ⚠️  Remote already exists, updating...
    git remote set-url origin %REPO_URL%
)

echo.
echo 🚀 Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  Push failed! This might be because:
    echo    - You need to authenticate with GitHub
    echo    - The repository URL is incorrect
    echo    - Network issues
    echo.
    echo Please try pushing manually:
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ CODE PUSHED TO GITHUB!
echo.

pause

echo.
echo 📝 STEP 3: DEPLOY ON RENDER
echo.
echo Now, follow these steps on Render.com:
echo.
echo 1. Go to: https://render.com
echo    • Sign up/login with GitHub (recommended)
echo.
echo 2. Click "New +" → "Web Service"
echo.
echo 3. Connect your repository:
echo    • Authorize Render to access GitHub
echo    • Find: kreyol-ia-platform
echo    • Click "Connect"
echo.
echo 4. Configure (should auto-fill from render.yaml):
echo    • Name: kreyol-ia-studio
echo    • Region: Oregon
echo    • Branch: main
echo    • Build Command: Auto-detected ✅
echo    • Start Command: Auto-detected ✅
echo    • Plan: Free (for testing)
echo.
echo 5. Environment Variables (auto-generated):
echo    • SECRET_KEY ✅
echo    • PYTHON_VERSION ✅
echo    • PORT ✅
echo.
echo 6. Click "Create Web Service"
echo.
echo 7. Wait 5-10 minutes for deployment
echo.
echo 8. You'll get a URL like:
echo    https://kreyol-ia-studio.onrender.com
echo.

pause

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              ✅ DEPLOYMENT GUIDE COMPLETE!                     ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📚 For detailed instructions, see:
echo    DEPLOYMENT_GUIDE_RENDER.md
echo.
echo 🌐 After deployment, your platform will be at:
echo    https://kreyol-ia-studio.onrender.com
echo.
echo 📱 Test these URLs:
echo    • https://your-url.onrender.com/
echo    • https://your-url.onrender.com/docs
echo    • https://your-url.onrender.com/health
echo.
echo 🎯 NEXT STEPS:
echo    1. Test your deployed platform
echo    2. Add Redis ($10/month) for all 23 features
echo    3. Share your platform URL!
echo.
echo 💰 COSTS:
echo    • Free tier: $0/month (15 features)
echo    • With Redis: $17/month (23 features) ⭐ Recommended
echo.
echo 🇭🇹 Fèlisitasyon! Platfòm ou an prèt pou deployment!
echo.

pause

