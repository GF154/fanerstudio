@echo off
echo ============================================================
echo PROJET KREYOL IA - INSTALLATION SCRIPT
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/6] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo.

echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)
echo.

echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/6] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [5/6] Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo.

echo [6/6] Installing PyTorch (CPU version)...
pip install torch==2.5.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
echo.

echo ============================================================
echo VERIFICATION
echo ============================================================
python test_quick.py
echo.

echo ============================================================
echo INSTALLATION COMPLETE!
echo ============================================================
echo.
echo IMPORTANT: Install FFmpeg for audio processing
echo    Run: choco install ffmpeg
echo    Or download from: https://ffmpeg.org/download.html
echo.
echo To activate the environment in the future:
echo    venv\Scripts\activate
echo.
echo To test the application:
echo    python check_setup.py
echo    streamlit run app.py
echo.
pause

