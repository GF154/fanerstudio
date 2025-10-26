@echo off
chcp 65001 > nul
cls
echo.
echo ============================================================
echo      🇭🇹 KREYÒL IA - GitHub Setup
echo ============================================================
echo.
echo Ce script va préparer votre projet pour GitHub et Render
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/5] Vérification de Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git n'est pas installé!
    echo.
    echo Téléchargez Git: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo ✅ Git installé

echo.
echo [2/5] Initialisation du repository...
if not exist .git (
    git init
    echo ✅ Repository initialisé
) else (
    echo ✅ Repository déjà initialisé
)

echo.
echo [3/5] Configuration Git (optionnel)...
set /p git_name="Entrez votre nom (ou appuyez sur Entrée): "
set /p git_email="Entrez votre email (ou appuyez sur Entrée): "

if not "%git_name%"=="" (
    git config user.name "%git_name%"
    echo ✅ Nom configuré: %git_name%
)

if not "%git_email%"=="" (
    git config user.email "%git_email%"
    echo ✅ Email configuré: %git_email%
)

echo.
echo [4/5] Ajout des fichiers...
git add .
echo ✅ Fichiers ajoutés

echo.
echo [5/5] Création du premier commit...
git commit -m "Initial commit - Kreyòl IA Creative Platform"
if %errorlevel% equ 0 (
    echo ✅ Commit créé
) else (
    echo ⚠️ Aucun changement à commiter ou commit déjà fait
)

echo.
echo ============================================================
echo ✅ PRÉPARATION TERMINÉE!
echo ============================================================
echo.
echo 📋 PROCHAINES ÉTAPES:
echo.
echo 1. Créez un repository sur GitHub:
echo    👉 https://github.com/new
echo.
echo 2. Nommez-le: kreyol-ia
echo.
echo 3. Copiez l'URL du repository (exemple):
echo    https://github.com/VOTRE_USERNAME/kreyol-ia.git
echo.
echo 4. Exécutez ces commandes:
echo.
echo    git remote add origin VOTRE_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo 5. Puis allez sur Render.com pour déployer!
echo    👉 https://render.com
echo.
echo ============================================================
echo.
echo 📖 Guide complet: DEPLOYMENT_GUIDE.md
echo.
pause

