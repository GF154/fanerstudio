@echo off
REM ============================================================
REM FFMPEG Installation Script (Requires Administrator)
REM ============================================================

echo ============================================================
echo FFMPEG Installation for Projet Kreyol IA
echo ============================================================
echo.
echo This script will install FFmpeg using Chocolatey.
echo FFmpeg is required for advanced audio processing.
echo.
echo NOTE: This script requires Administrator privileges!
echo.
pause

echo.
echo Installing FFmpeg...
choco install ffmpeg -y

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo FFmpeg installed successfully!
    echo ============================================================
    echo.
    echo Verifying installation...
    ffmpeg -version
    echo.
    echo You can now use full audio features.
) else (
    echo.
    echo ============================================================
    echo Installation failed!
    echo ============================================================
    echo.
    echo Please try one of these alternatives:
    echo 1. Run this script as Administrator
    echo 2. Download from: https://ffmpeg.org/download.html
    echo 3. Use: choco install ffmpeg
    echo.
)

pause

