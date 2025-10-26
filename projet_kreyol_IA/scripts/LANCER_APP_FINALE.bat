@echo off
chcp 65001 > nul
echo ============================================================
echo 🇭🇹 KREYÒL IA - PROFESSIONAL STUDIO
echo ============================================================
echo.
echo 🚀 Démarrage de l'application...
echo.

cd /d "%~dp0"

echo ✅ Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo ✅ Lancement du serveur...
echo.
python api_final.py

pause

