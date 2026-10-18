@echo off
chcp 65001 >nul
REM Kontrol Merkezi'ni bu makinede Windows acilisinda otomatik baslatir (YONETICI olarak calistirin).
REM Kullanim: merkez_kur.bat [port]   (varsayilan 8765)
cd /d "%~dp0"
set PORT=%1
if "%PORT%"=="" set PORT=8765
schtasks /Create /F /TN "RPA_Merkez" /SC ONSTART /RU SYSTEM /RL HIGHEST /TR "\"%~dp0RPA_Bot.exe\" --config \"%~dp0config.ini\" merkez"
if errorlevel 1 goto :hata
netsh advfirewall firewall delete rule name="RPA Kontrol Merkezi" >nul 2>&1
netsh advfirewall firewall add rule name="RPA Kontrol Merkezi" dir=in action=allow protocol=TCP localport=%PORT%
schtasks /Run /TN "RPA_Merkez"
echo.
echo Kontrol Merkezi kuruldu ve baslatildi: http://%COMPUTERNAME%:%PORT%
echo Ilk yonetici parolasi: %~dp0merkez_veri\ilk_yonetici_parolasi.txt
pause
exit /b 0
:hata
echo Kurulum basarisiz. Bu dosyayi "Yonetici olarak calistir" ile acin.
pause
exit /b 1
