@echo off
chcp 65001 >nul
echo ================================================================
echo 🇭🇹 TRADUCTION NLLB - CRÉOLE HAÏTIEN
echo ================================================================
echo.
echo Tradiksyon ak modèl NLLB Meta (pi bon kalite pou Kreyòl)
echo Translation with Meta NLLB model (best quality for Creole)
echo.
echo ================================================================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python pa enstale / Python is not installed
    echo    Tanpri enstale Python 3.8+ / Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python trouvé / Python found
echo.

REM Vérifier si venv existe
if not exist "venv\" (
    echo ⚠️  Environnement virtuel pa egziste
    echo    Kreye environnement virtuel / Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de l'environnement
        pause
        exit /b 1
    )
    echo ✅ Environnement créé
    echo.
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur d'activation
    pause
    exit /b 1
)

echo ✅ Environnement activé
echo.

REM Vérifier les dépendances
echo 🔍 Vérification des dépendances...
python -c "import transformers" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dépendances manquantes / Missing dependencies
    echo    Instalasyon depandans... / Installing dependencies...
    pip install transformers torch sentencepiece langdetect tqdm
    if errorlevel 1 (
        echo ❌ Erreur d'installation
        pause
        exit /b 1
    )
    echo ✅ Dépendances installées
    echo.
)

echo ✅ Dépendances OK
echo.
echo ================================================================

REM Vérifier si un fichier est passé en argument
if "%~1"=="" (
    echo 📖 Usage: TRADUIRE_NLLB.bat fichier.txt [modele]
    echo.
    echo Modèles disponibles:
    echo   - distilled : Rapide, ~2.5GB ^(défaut^)
    echo   - medium    : Meilleure qualité, ~5GB
    echo   - large     : Excellente qualité, ~13GB
    echo.
    echo Exemples:
    echo   TRADUIRE_NLLB.bat data\test_document.txt
    echo   TRADUIRE_NLLB.bat mon_livre.txt medium
    echo.
    
    REM Chercher un fichier de test par défaut
    if exist "data\test_document.txt" (
        echo 📄 Fichier de test trouvé: data\test_document.txt
        echo    Lancer traduction? ^(Y/N^)
        set /p choice="> "
        if /i "!choice!"=="Y" (
            set "fichier=data\test_document.txt"
            goto :run_translation
        )
    )
    
    echo.
    echo Glissez-déposez un fichier .txt sur ce script
    echo ou lancez: TRADUIRE_NLLB.bat votre_fichier.txt
    pause
    exit /b 0
)

:run_translation
if "%fichier%"=="" set "fichier=%~1"

REM Vérifier que le fichier existe
if not exist "%fichier%" (
    echo ❌ Fichier introuvable: %fichier%
    pause
    exit /b 1
)

echo 📄 Fichier: %fichier%
echo.

REM Construire la commande
set "cmd=python traduire_nllb.py "%fichier%""

REM Ajouter le modèle si spécifié
if not "%~2"=="" (
    echo 🤖 Modèle: %~2
    set "cmd=%cmd% --modele %~2"
)

echo.
echo 🚀 Lancement de la traduction NLLB...
echo ================================================================
echo.

REM Exécuter la traduction
%cmd%

set error_code=%errorlevel%

echo.
echo ================================================================

if %error_code% equ 0 (
    echo ✅ Traduction réussie!
    echo.
    echo 📁 Les fichiers sont dans le dossier: output\
    echo.
) else (
    echo ❌ Erreur lors de la traduction ^(code: %error_code%^)
    echo.
)

echo Appuyez sur une touche pour fermer...
pause >nul

exit /b %error_code%

