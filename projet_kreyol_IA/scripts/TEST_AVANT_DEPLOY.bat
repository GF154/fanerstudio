@echo off
chcp 65001 > nul
cls

cd /d "%~dp0"

python test_deployment.py

pause

