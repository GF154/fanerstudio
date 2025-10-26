@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║          🧪 TEST GWO PDF - KAPASITE TRETMAN                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 KONSENAN TEST SA A:
echo    • Teste ekstraksyon PDF gwo volim
echo    • Verifye progress indicators
echo    • Teste chunk processing
echo    • Mesire pèfòmans
echo.
echo ═══════════════════════════════════════════════════════════
echo.

echo 🔧 OPTION TEST:
echo.
echo    1. Test PDF nòmal (50-100 paj)
echo    2. Test PDF mwayen (100-500 paj)
echo    3. Test PDF gwo (500-2000 paj)
echo    4. Test streaming extraction
echo    5. Test ak limit paj
echo.

set /p choice="Chwazi opsyon (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🧪 TEST 1: PDF Nòmal (50-100 paj)
    echo    • Limit: Pa gen
    echo    • Progress: Wi
    echo    • Chunk size: 50 paj
    echo.
    echo 💡 PASE FICHYE PDF OU YO NAN FOLDÈ 'input\'
    echo.
    pause
    python -c "import asyncio; from app.services.media_service import MediaService; from pathlib import Path; asyncio.run(MediaService().extract_text_from_document(str(Path('input').glob('*.pdf').__next__()), show_progress=True))"
)

if "%choice%"=="2" (
    echo.
    echo 🧪 TEST 2: PDF Mwayen (100-500 paj)
    echo    • Limit: 300 paj
    echo    • Progress: Wi
    echo    • Chunk size: 50 paj
    echo.
    pause
    python -c "import asyncio; from app.services.media_service import MediaService; from pathlib import Path; asyncio.run(MediaService().extract_text_from_document(str(Path('input').glob('*.pdf').__next__()), max_pages=300, show_progress=True))"
)

if "%choice%"=="3" (
    echo.
    echo 🧪 TEST 3: PDF Gwo (500-2000 paj)
    echo    • Limit: 1000 paj
    echo    • Progress: Wi
    echo    • Chunk size: 50 paj
    echo    ⚠️  SA KA PRAN 10-30 MINIT!
    echo.
    pause
    python -c "import asyncio; from app.services.media_service import MediaService; from pathlib import Path; asyncio.run(MediaService().extract_text_from_document(str(Path('input').glob('*.pdf').__next__()), max_pages=1000, show_progress=True))"
)

if "%choice%"=="4" (
    echo.
    echo 🧪 TEST 4: Streaming Extraction
    echo    • Chunk size: 100 paj
    echo    • Memwa optimize: Wi
    echo    • Callback progress: Wi
    echo.
    pause
    python -c "import asyncio; from app.services.media_service import MediaService; from pathlib import Path; asyncio.run(MediaService().extract_text_from_pdf_streaming(Path('input').glob('*.pdf').__next__(), chunk_size_pages=100))"
)

if "%choice%"=="5" (
    echo.
    set /p max_paj="Kantite paj maksimòm (100-2000): "
    echo.
    echo 🧪 TEST 5: Limit Paj Kustom
    echo    • Limit: %max_paj% paj
    echo    • Progress: Wi
    echo.
    pause
    python -c "import asyncio; from app.services.media_service import MediaService; from pathlib import Path; asyncio.run(MediaService().extract_text_from_document(str(Path('input').glob('*.pdf').__next__()), max_pages=%max_paj%, show_progress=True))"
)

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ TEST KONPLE!
echo.
pause

