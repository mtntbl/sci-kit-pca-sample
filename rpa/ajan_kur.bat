@echo off
chcp 65001 >nul
REM Robot ajanini bu kullanici oturum actiginda otomatik baslatir.
REM Masaustu (Mikro) otomasyonu icin ajan ACIK BIR KULLANICI OTURUMUNDA calismalidir.
REM Once config.ini [AJAN] bolumune merkez_url, robot_adi, robot_anahtari yazin.
cd /d "%~dp0"
schtasks /Create /F /TN "RPA_Ajan" /SC ONLOGON /RL LIMITED /TR "\"%~dp0RPA_Bot.exe\" --config \"%~dp0config.ini\" ajan"
if errorlevel 1 goto :hata
schtasks /Run /TN "RPA_Ajan"
echo Robot ajani kuruldu ve baslatildi (%USERNAME% oturumunda).
pause
exit /b 0
:hata
echo Kurulum basarisiz.
pause
exit /b 1
