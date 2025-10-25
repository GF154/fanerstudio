@echo off
REM Setup script for cloud storage integration (Windows)

echo ==================================================
echo 🚀 KONFIGIRASYON CLOUD STORAGE
echo    Cloud Storage Configuration
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python pa enstale / not installed
    exit /b 1
)

echo ✅ Python installed

REM Install cloud storage packages
echo.
echo 📦 Enstalasyon pakèt / Installing packages...
pip install google-cloud-storage boto3 python-dotenv

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo 📝 Kreyasyon fichye .env / Creating .env file...
    copy cloud_env_template.txt .env
    echo ✅ .env file created. Please edit it with your bucket name.
) else (
    echo.
    echo ✅ .env file already exists
)

REM Create directories
echo.
echo 📁 Kreyasyon repèrtwa / Creating directories...
if not exist input mkdir input
if not exist output mkdir output
if not exist cache mkdir cache
if not exist logs mkdir logs

echo.
echo ==================================================
echo ✅ Konfigirasyon konplè / Setup complete!
echo ==================================================
echo.
echo Pwochen etap / Next steps:
echo 1. Edit .env file with your GCS_BUCKET_NAME
echo    notepad .env
echo.
echo 2. Set up Google Cloud authentication:
echo    gcloud auth application-default login
echo    OR
echo    set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json
echo.
echo 3. Run test:
echo    python test_cloud_storage.py
echo.
echo 4. Process a book:
echo    python process_book.py
echo.
pause

