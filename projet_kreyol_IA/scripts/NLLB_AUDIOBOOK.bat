@echo off
chcp 65001 > nul
echo ============================================================
echo 🇭🇹 KREYÒL IA - NLLB AUDIOBOOK CREATOR
echo ============================================================
echo.
echo 📚 Kreye audiobook an Kreyòl soti nan PDF
echo.

SET SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if PDF file is provided
if "%~1"=="" (
    echo ⚠️  Tanpri bay chemen fichye PDF la!
    echo.
    echo Usage: NLLB_AUDIOBOOK.bat "fichye.pdf" [lang]
    echo.
    echo Egzanp:
    echo   NLLB_AUDIOBOOK.bat "mon_livre.pdf"
    echo   NLLB_AUDIOBOOK.bat "book.pdf" eng_Latn
    echo.
    echo Lang disponib:
    echo   - fra_Latn  (Franse - default)
    echo   - eng_Latn  (Angle)
    echo   - spa_Latn  (Panyòl)
    echo.
    pause
    exit /b 1
)

REM Get parameters
SET PDF_FILE=%~1
SET SRC_LANG=%~2
if "%SRC_LANG%"=="" SET SRC_LANG=fra_Latn

echo 📄 Fichye PDF: %PDF_FILE%
echo 🌍 Lang sous: %SRC_LANG%
echo.
echo ⏳ Kòmanse pwosesis...
echo.

python app\nllb_pipeline.py "%PDF_FILE%" %SRC_LANG%

echo.
echo ============================================================
echo ✅ Fini! Gade dosye 'output/nllb' pou rezilta yo
echo ============================================================
pause

