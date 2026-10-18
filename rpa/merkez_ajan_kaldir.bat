@echo off
schtasks /End /TN "RPA_Ajan" 2>nul
schtasks /Delete /F /TN "RPA_Ajan" 2>nul
schtasks /End /TN "RPA_Merkez" 2>nul
schtasks /Delete /F /TN "RPA_Merkez" 2>nul
netsh advfirewall firewall delete rule name="RPA Kontrol Merkezi" >nul 2>&1
echo Kaldirildi.
pause
