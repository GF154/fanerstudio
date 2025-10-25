@echo off
cls
echo ============================================================
echo   🇭🇹 PWOJE KREYOL IA - Interface FastAPI
echo ============================================================
echo.
echo Demarrage de l'interface web FastAPI...
echo.
echo Ouvrez votre navigateur sur: http://localhost:8000
echo.
echo Pour arreter: Appuyez sur Ctrl+C
echo ============================================================
echo.

cd /d "%~dp0"

echo Lancement du serveur...
python web_interface.py

pause

