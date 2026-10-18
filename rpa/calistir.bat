@echo off
chcp 65001 >nul
cd /d "%~dp0"
REM Argumansiz: menu. Ornek: calistir.bat ise-giris
RPA_Bot.exe %*
if not "%~1"=="" pause
