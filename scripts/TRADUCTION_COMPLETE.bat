@echo off
cls
echo ============================================================
echo   🇭🇹 TRADUCTION COMPLETE EN CREOLE HAITIEN
echo   PDF → Texte → Traduction → Audiobook
echo ============================================================
echo.
echo Ce script realise la traduction complete en 3 etapes:
echo   1. Extraction du texte (ou utilisation de fichier texte)
echo   2. Traduction en creole haitien
echo   3. Generation de l'audiobook avec voix native
echo.
echo ============================================================
echo.

cd /d "%~dp0"

REM Vérifier si le document de test existe
if not exist "data\test_document.txt" (
    echo 📝 Creation d'un document de test...
    python creer_pdf_test.py
    echo.
)

echo ============================================================
echo ETAPE 1: TRADUCTION
echo ============================================================
echo.

python traduire_texte.py data\test_document.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erreur lors de la traduction
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ETAPE 2: GENERATION AUDIOBOOK
echo ============================================================
echo.

python generer_audio_huggingface.py output\test_document\test_document_kreyol.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erreur lors de la generation audio
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ TRADUCTION COMPLETE TERMINEE!
echo ============================================================
echo.
echo 📂 Dossier de sortie: output\test_document\
echo.
echo 📄 Fichiers crees:
echo    - test_document_original.txt (texte original)
echo    - test_document_kreyol.txt (traduction creole)
echo    - test_document_audio_hf.mp3 (audiobook avec voix native)
echo.
echo 💡 Double-cliquez sur le fichier MP3 pour ecouter!
echo.
echo ============================================================

pause

