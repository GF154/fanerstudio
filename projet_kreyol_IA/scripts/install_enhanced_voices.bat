@echo off
REM ============================================================
REM Install Enhanced Voice Support for Better Creole Pronunciation
REM Installation des Voix Améliorées pour le Créole
REM ============================================================

echo ============================================================
echo INSTALLATION DES VOIX AMELIOREES
echo Enhanced Voice Installation
echo ============================================================
echo.

cd /d "%~dp0"

echo Activation de l'environnement virtuel...
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ============================================================
echo Installation de Edge TTS (Voix de haute qualite)
echo Installing Edge TTS (High-quality voices)
echo ============================================================
echo.

pip install edge-tts

echo.
echo ============================================================
echo Installation de pyttsx3 (Voix hors ligne - optionnel)
echo Installing pyttsx3 (Offline voices - optional)
echo ============================================================
echo.

pip install pyttsx3

echo.
echo ============================================================
echo Verification de l'installation
echo Verifying installation
echo ============================================================
echo.

python -c "import edge_tts; print('✅ Edge TTS installe / installed')" 2>nul || echo "❌ Edge TTS non installe / not installed"
python -c "import pyttsx3; print('✅ pyttsx3 installe / installed')" 2>nul || echo "❌ pyttsx3 non installe / not installed"

echo.
echo ============================================================
echo Test des voix disponibles
echo Testing available voices
echo ============================================================
echo.

echo Liste des voix francaises disponibles:
echo List of available French voices:
echo.
edge-tts --list-voices | findstr "fr-" | findstr "Neural"

echo.
echo ============================================================
echo INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Voix recommandees pour le creole haitien:
echo Recommended voices for Haitian Creole:
echo.
echo 1. fr-CA-SylvieNeural (Canadienne - MEILLEUR)
echo 2. fr-FR-DeniseNeural (Francaise - Tres bon)
echo 3. fr-CA-AntoineNeural (Canadien homme)
echo.
echo Pour utiliser:
echo To use:
echo 1. Redemarrez l'application web
echo 2. L'application choisira automatiquement la meilleure voix
echo.
echo Documentation complete: ENHANCED_VOICE_GUIDE.md
echo.
pause

