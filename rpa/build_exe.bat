@echo off
REM Windows'ta exe'yi kendiniz derlemek icin (Python 3.10+ kurulu olmali)
cd /d "%~dp0"
python -m venv .venv || goto :err
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller || goto :err
pyinstaller --noconfirm --clean --onefile --console --name PCA_RPA pca_rpa.py || goto :err
if exist paket rmdir /s /q paket
mkdir paket\input paket\output paket\archive paket\error paket\logs paket\ornek_veri
copy dist\PCA_RPA.exe paket\ >nul
copy config.ini paket\ >nul
copy KULLANIM.md paket\ >nul
copy calistir.bat paket\ >nul
copy izleme_modu.bat paket\ >nul
copy gorev_zamanlayici_kur.bat paket\ >nul
copy gorev_zamanlayici_kaldir.bat paket\ >nul
copy ornek_veri\* paket\ornek_veri\ >nul
powershell -NoProfile -Command "Compress-Archive -Path paket\* -DestinationPath PCA_RPA_Windows.zip -Force"
echo.
echo Hazir: %~dp0PCA_RPA_Windows.zip
pause
exit /b 0
:err
echo Derleme basarisiz.
pause
exit /b 1
