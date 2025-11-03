@echo off
:: Run All Tests
:: Execute all unit and integration tests with coverage

echo.
echo ========================================
echo    RUNNING FANER STUDIO TESTS
echo ========================================
echo.

:: Check if pytest is installed
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo ERROR: pytest not installed!
    echo.
    echo Installing pytest...
    pip install pytest pytest-asyncio pytest-cov httpx
    echo.
)

:: Run tests
echo Running tests with coverage...
echo.
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

echo.
echo ========================================
echo    TEST RESULTS
echo ========================================
echo.
echo Coverage report saved to: htmlcov/index.html
echo.
echo To view coverage report:
echo   start htmlcov\index.html
echo.
pause

