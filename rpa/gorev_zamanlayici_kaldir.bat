@echo off
schtasks /Delete /F /TN "RPA_Bot_IseGiris"
schtasks /Delete /F /TN "RPA_Bot_PCA"
schtasks /Delete /F /TN "PCA_RPA" 2>nul
pause
