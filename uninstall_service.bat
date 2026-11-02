@echo off
cd /d "%~dp0"

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ========================================================
    echo  Access denied.
    echo  Please run this script as Administrator.
    echo ========================================================
    pause
    exit /b
)

echo Stopping and removing Heart Rate Task...
schtasks /end /tn "HeartRateService" >nul 2>&1
schtasks /delete /tn "HeartRateService" /f >nul 2>&1
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Stop-Process -Force" >nul 2>&1

echo.
echo ========================================================
echo SUCCESS! Task completely removed from Windows.
echo ========================================================
pause