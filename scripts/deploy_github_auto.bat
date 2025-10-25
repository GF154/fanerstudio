@echo off
chcp 65001 > nul
cls
echo.
echo ============================================================
echo      🇭🇹 KREYÒL IA - Déploiement Automatique GitHub
echo ============================================================
echo.
echo Ce script utilise GitHub CLI pour tout automatiser!
echo.
echo ============================================================
echo.

cd /d "%~dp0"

REM Vérifier si GitHub CLI est installé
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI n'est pas installé!
    echo.
    echo Installation en cours...
    winget install --id GitHub.cli
    echo.
    echo ✅ Redémarrez PowerShell et relancez ce script
    pause
    exit /b 1
)

echo ✅ GitHub CLI détecté
echo.

REM Vérifier l'authentification
echo [1/6] Vérification de l'authentification GitHub...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 🔐 Connexion à GitHub requise...
    echo.
    echo Choisissez votre méthode:
    echo   1. Browser (recommandé - plus facile)
    echo   2. Token (avancé)
    echo.
    set /p auth_method="Votre choix (1 ou 2): "
    
    if "%auth_method%"=="1" (
        echo.
        echo 🌐 Ouverture du navigateur pour connexion...
        gh auth login --web
    ) else (
        echo.
        gh auth login
    )
    
    if %errorlevel% neq 0 (
        echo ❌ Authentification échouée
        pause
        exit /b 1
    )
)

echo ✅ Authentifié sur GitHub
echo.

REM Initialiser Git si nécessaire
echo [2/6] Initialisation Git...
if not exist .git (
    git init
    echo ✅ Git initialisé
) else (
    echo ✅ Git déjà initialisé
)
echo.

REM Ajouter les fichiers
echo [3/6] Ajout des fichiers...
git add .
echo ✅ Fichiers ajoutés
echo.

REM Commit
echo [4/6] Création du commit...
git commit -m "🚀 Initial commit - Kreyòl IA Creative Platform" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Commit créé
) else (
    echo ⚠️ Aucun changement à commiter (déjà fait?)
)
echo.

REM Créer le repository sur GitHub
echo [5/6] Création du repository sur GitHub...
set /p repo_visibility="Repository public ou privé? (public/private) [public]: "
if "%repo_visibility%"=="" set repo_visibility=public

gh repo create kreyol-ia --source=. --%repo_visibility% --description "🇭🇹 Professional AI-powered content creation platform for Haitian Creole" --push

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Le repository existe peut-être déjà?
    echo.
    echo Tentative de connexion au repo existant...
    
    REM Récupérer le username GitHub
    for /f "tokens=*" %%i in ('gh api user --jq .login') do set GH_USERNAME=%%i
    
    git remote remove origin >nul 2>&1
    git remote add origin https://github.com/!GH_USERNAME!/kreyol-ia.git
    git branch -M main
    git push -u origin main --force
)

echo.
echo ✅ Code poussé sur GitHub!
echo.

REM Afficher l'URL
echo [6/6] Récupération de l'URL...
for /f "tokens=*" %%i in ('gh repo view --json url --jq .url') do set REPO_URL=%%i

echo.
echo ============================================================
echo ✅ DÉPLOIEMENT GITHUB TERMINÉ!
echo ============================================================
echo.
echo 📦 Repository créé: %REPO_URL%
echo.
echo 🔗 Accès direct:
echo    %REPO_URL%
echo.
echo ============================================================
echo.
echo 📋 PROCHAINE ÉTAPE: Déployer sur Render
echo.
echo Option 1 - Via Interface Web (Facile):
echo   1. Allez sur https://render.com
echo   2. Connectez-vous avec GitHub
echo   3. New ^> Web Service
echo   4. Sélectionnez 'kreyol-ia'
echo   5. Deploy!
echo.
echo Option 2 - Via Blueprint (Automatique):
echo   1. Allez sur %REPO_URL%
echo   2. Cliquez le bouton "Deploy to Render"
echo.
echo Option 3 - Via CLI (Pour experts):
echo   Installez: npm install -g @render/cli
echo   Puis: render deploy
echo.
echo ============================================================
echo.
echo 🎉 Votre code est prêt pour Render!
echo.

REM Ouvrir le repo dans le navigateur
set /p open_browser="Ouvrir le repository dans le navigateur? (o/n) [o]: "
if "%open_browser%"=="" set open_browser=o
if /i "%open_browser%"=="o" (
    start "" "%REPO_URL%"
)

echo.
pause

