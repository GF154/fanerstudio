@echo off
REM ============================================================
REM Start Streamlit Web Interface - Projet Kreyol IA
REM ============================================================

echo ============================================================
echo 🇭🇹 PWOJE KREYOL IA - WEB INTERFACE
echo ============================================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Streamlit web interface...
echo.
echo The app will open at: http://localhost:8501
echo Your browser should open automatically.
echo.
echo ============================================================
echo TO STOP THE SERVER: Press Ctrl+C
echo ============================================================
echo.

streamlit run app.py

pause

