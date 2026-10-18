@echo off
chcp 65001 >nul
REM PCA_RPA.exe'yi Windows Gorev Zamanlayici'ya ekler.
REM Kullanim: gorev_zamanlayici_kur.bat [dakika]   (varsayilan 15 dakikada bir)
cd /d "%~dp0"
set ARALIK=%1
if "%ARALIK%"=="" set ARALIK=15
schtasks /Create /F /TN "PCA_RPA" /SC MINUTE /MO %ARALIK% /TR "\"%~dp0PCA_RPA.exe\" --once --config \"%~dp0config.ini\""
if errorlevel 1 (
  echo Gorev olusturulamadi. Bu dosyayi "Yonetici olarak calistir" ile deneyin.
) else (
  echo "PCA_RPA" gorevi %ARALIK% dakikada bir calisacak sekilde olusturuldu.
)
pause
