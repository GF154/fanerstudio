@echo off
cls
echo ============================================================
echo   🇭🇹 PWOJE KREYOL IA - Interface Streamlit
echo ============================================================
echo.
echo Demarrage de l'interface web Streamlit...
echo Le navigateur va s'ouvrir automatiquement.
echo.
echo Pour arreter: Appuyez sur Ctrl+C
echo ============================================================
echo.

cd /d "%~dp0"

python -m streamlit run web_app.py

pause

