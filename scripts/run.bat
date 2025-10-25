@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════
echo 🇭🇹 PWOJÈ KREYÒL IA / HAITIAN CREOLE AI PROJECT
echo ═══════════════════════════════════════════════════════════
echo.

REM Verifye si Python enstale
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python pa enstale! Tanpri enstale Python 3.8+
    echo ❌ Python not installed! Please install Python 3.8+
    pause
    exit /b 1
)

REM Verifye si depandans yo enstale
echo 🔍 Verifye depandans / Checking dependencies...
python -c "import pypdf, transformers, torch, gtts, langdetect, tqdm" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Depandans pa enstale! / Dependencies not installed!
    echo.
    set /p install="Vle w enstale yo kounye a? (y/n): "
    if /i "%install%"=="y" (
        echo.
        echo 📦 Enstalasyon depandans / Installing dependencies...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo ❌ Enstalasyon echwe / Installation failed
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Depandans nesesè pou egzekite / Dependencies required to run
        pause
        exit /b 1
    )
)

REM Verifye si gen PDF
if not exist "data\input.pdf" (
    echo.
    echo ⚠️  Pa gen fichye PDF nan data\input.pdf
    echo ⚠️  No PDF file found at data\input.pdf
    echo.
    echo 📝 Tanpri mete yon fichye PDF nan dosye 'data' ak non 'input.pdf'
    echo 📝 Please place a PDF file in the 'data' folder named 'input.pdf'
    pause
    exit /b 1
)

echo.
echo ✅ Tout bagay pare! Ap kòmanse pwosesis la...
echo ✅ Everything ready! Starting process...
echo.

REM Egzekite script prensipal
python main.py

echo.
echo ═══════════════════════════════════════════════════════════
if errorlevel 0 (
    echo ✅ Pwosesis la fini! Gade rezilta yo nan dosye 'output'
    echo ✅ Process complete! Check results in 'output' folder
) else (
    echo ❌ Yon erè rive pandan pwosesis la
    echo ❌ An error occurred during processing
)
echo ═══════════════════════════════════════════════════════════
echo.
pause

