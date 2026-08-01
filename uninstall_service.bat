@echo off
cd /d "%~dp0"

echo Stopping and removing Heart Rate Task...
schtasks /end /tn "HeartRateService" >nul 2>&1
schtasks /delete /tn "HeartRateService" /f >nul 2>&1

echo.
echo ========================================================
echo SUCCESS! Heart Rate Task completely removed from Windows.
echo ========================================================
pause