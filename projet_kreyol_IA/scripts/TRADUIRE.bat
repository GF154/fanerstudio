@echo off
cls
echo ============================================================
echo   🇭🇹 TRADUCTION DE DOCUMENT EN CREOLE HAITIEN
echo ============================================================
echo.
echo Ce script va traduire votre PDF en creole haitien.
echo.
echo ============================================================
echo.

cd /d "%~dp0"

REM Vérifier si un PDF existe dans data/
if exist "data\input.pdf" (
    echo ✅ Document trouve: data\input.pdf
    echo.
    python traduire_document.py
) else (
    echo ⚠️  Aucun fichier data\input.pdf trouve
    echo.
    echo 📝 Instructions:
    echo    1. Placez votre PDF dans le dossier "data"
    echo    2. Renommez-le "input.pdf"
    echo    3. Relancez ce script
    echo.
    echo OU glissez-deposez votre PDF sur ce fichier .bat
    echo.
)

echo.
pause

