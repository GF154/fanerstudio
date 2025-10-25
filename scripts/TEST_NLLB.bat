@echo off
chcp 65001 >nul
echo ================================================================
echo 🧪 TEST RAPIDE NLLB - TRADUCTION CRÉOLE HAÏTIEN
echo ================================================================
echo.
echo Tès rapid pou verifye ke NLLB fonksyone kòrèkteman
echo Quick test to verify NLLB is working correctly
echo.
echo ================================================================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python pa enstale / Python is not installed
    pause
    exit /b 1
)

echo ✅ Python trouvé
echo.

REM Vérifier si venv existe
if not exist "venv\" (
    echo ⚠️  Environnement virtuel pa egziste
    echo    Kreye l / Creating it...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création
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

REM Lancer le test
echo ================================================================
echo 🚀 Lancement du test NLLB...
echo ================================================================
echo.

python test_nllb_quick.py

set error_code=%errorlevel%

echo.
echo ================================================================

if %error_code% equ 0 (
    echo.
    echo ✅ Tests réussis! NLLB est prêt à l'emploi.
    echo.
    echo 📚 Consultez NLLB_GUIDE.md pour plus d'informations.
    echo.
) else (
    echo.
    echo ❌ Erreur lors des tests ^(code: %error_code%^)
    echo.
    echo 💡 Si les dépendances manquent, installez-les:
    echo    pip install transformers torch sentencepiece langdetect
    echo.
)

echo Appuyez sur une touche pour fermer...
pause >nul

exit /b %error_code%

