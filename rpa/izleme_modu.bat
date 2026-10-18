@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo input klasoru PCA icin izleniyor. Durdurmak icin Ctrl+C ...
RPA_Bot.exe pca --watch
pause
