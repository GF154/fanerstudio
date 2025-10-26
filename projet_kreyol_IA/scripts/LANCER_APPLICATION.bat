@echo off
cls
echo ============================================================
echo   🇭🇹 PWOJE KREYOL IA - APPLICATION COMPLETE
echo ============================================================
echo.
echo Demarrage de l'application avec backend fonctionnel...
echo.
echo Fonctionnalites actives:
echo   - 📚 Audiobook Creator (avec voix creole native)
echo   - 🎙️ Podcast Creator (multi-voix)
echo   - 🌍 Text Translator (AI M2M100)
echo   - 📄 PDF Translator
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo ⚡ Lancement du serveur API...
echo.
echo 🌐 L'application s'ouvrira automatiquement sur:
echo    http://localhost:8000
echo.
echo 🛑 Pour arreter: Appuyez sur Ctrl+C
echo.
echo ============================================================
echo.

REM Lancer l'API et ouvrir le navigateur après 3 secondes
start /B python api_backend.py

timeout /t 5 /nobreak >nul

start http://localhost:8000

echo.
echo ✅ Application lancee!
echo.
pause

