@echo off
chcp 65001 >nul
cd /d "%~dp0"
PCA_RPA.exe %*
echo.
pause
