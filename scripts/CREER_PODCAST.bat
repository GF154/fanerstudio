@echo off
cls
echo ============================================================
echo   🎙️ PODCAST CREATOR - PWOJE KREYOL IA
echo ============================================================
echo.
echo Creation de podcasts avec plusieurs voix en creole
echo.
echo ============================================================
echo.

cd /d "%~dp0"

REM Vérifier si un script existe
if exist "data\demo_podcast_script.txt" (
    echo ✅ Script trouve: data\demo_podcast_script.txt
    echo.
    python podcast_creator.py data\demo_podcast_script.txt
) else (
    echo 📝 Creation d'un podcast de demonstration...
    echo.
    python podcast_creator.py
)

echo.
pause

