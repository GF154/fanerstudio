@echo off
cls
echo ============================================================
echo   🎧 CREATION D'AUDIOBOOK EN CREOLE HAITIEN
echo   avec Voix Native Hugging Face
echo ============================================================
echo.
echo Ce script genere un audiobook avec une vraie voix creole.
echo.
echo ============================================================
echo.

cd /d "%~dp0"

REM Vérifier si un fichier créole existe
if exist "output\test_document\test_document_kreyol.txt" (
    echo ✅ Fichier créole trouvé!
    echo.
    echo 🎧 Génération de l'audiobook en cours...
    echo.
    python generer_audio_huggingface.py output\test_document\test_document_kreyol.txt
) else (
    echo ⚠️  Aucun fichier créole trouvé
    echo.
    echo 📝 Instructions:
    echo    1. Traduisez d'abord un document avec TRADUIRE.bat
    echo    2. Puis relancez ce script
    echo.
)

echo.
pause

