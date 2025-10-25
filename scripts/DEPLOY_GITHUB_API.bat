@echo off
chcp 65001 > nul
cls

cd /d "%~dp0"

echo.
echo ============================================================
echo      🇭🇹 KREYÒL IA - Déploiement via GitHub API
echo ============================================================
echo.

python deploy_github_api.py

echo.
pause

