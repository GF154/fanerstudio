@echo off
REM 🎵 Test Rapide - Générateur de Musique Faner Studio
echo.
echo ========================================
echo   🎵 TEST JENERATÈ MIZIK FANER STUDIO
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python pa enstale!
    echo    Tanpri enstale Python 3.11+
    pause
    exit /b 1
)

echo ✅ Python detekte
echo.

REM Activer l'environnement virtuel si disponible
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Aktivasyon venv...
    call venv\Scripts\activate.bat
    echo ✅ venv aktive
) else (
    echo ⚠️  venv pa detekte (opsyonèl)
)
echo.

REM Vérifier les dépendances
echo 🔍 Verifikasyon dependans...
python -c "import pydub" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  pydub pa enstale!
    echo    Ap enstale dependans nesesè...
    echo.
    pip install pydub soundfile scipy numpy
    if errorlevel 1 (
        echo ❌ Pwoblem pandan enstalasyon
        pause
        exit /b 1
    )
)

echo ✅ Tout dependans la disponib
echo.

echo ========================================
echo   📋 TEST KÒMANSE
echo ========================================
echo.

REM Test du module music_generator
echo 🎼 Test 1: Jeneratè Mizik...
python -c "from src.music_generator import HaitianMusicGenerator; print('✅ Module music_generator OK')"
if errorlevel 1 (
    echo ❌ Erè nan module music_generator
    pause
    exit /b 1
)
echo.

echo 🎛️ Test 2: Editè Odyo...
python -c "from src.audio_editor import AudioEditor; print('✅ Module audio_editor OK')"
if errorlevel 1 (
    echo ❌ Erè nan module audio_editor
    pause
    exit /b 1
)
echo.

echo 🔌 Test 3: API Routes...
python -c "from app.api_music import router; print('✅ API Music OK')"
if errorlevel 1 (
    echo ❌ Erè nan API music
    pause
    exit /b 1
)
python -c "from app.api_audio_editor import router; print('✅ API Audio Editor OK')"
if errorlevel 1 (
    echo ❌ Erè nan API audio editor
    pause
    exit /b 1
)
echo.

echo ========================================
echo   ✅ TOUT TEST REYISI!
echo ========================================
echo.
echo 🎵 Fonksyonalite Mizik la pare pou itilize!
echo.
echo 📋 Pou teste nan pwatik:
echo    1. Lance aplikasyon an: python app/main.py
echo    2. Ouvè navigatè ou: http://localhost:8000/pages/music_generator.html
echo    3. Chwazi yon stil (Konpa, Rara, etc.)
echo    4. Jenere mizik ou!
echo.
echo 🌐 Endpoints disponib:
echo    • GET  /api/music/styles
echo    • POST /api/music/generate
echo    • POST /api/music/beat
echo    • POST /api/music/mix
echo    • GET  /api/music/templates
echo    • POST /api/audio-editor/preset/podcast
echo.
echo 📚 Dokumentasyon: docs/MUSIC_FEATURES.md
echo.

pause

