@echo off
cd /d "%~dp0"

echo [1/3] Safely stopping background task...
:: Останавливаем фоновое задание в планировщике
schtasks /end /tn "HeartRateService" >nul 2>&1

:: Принудительно гасим сам фоновый процесс Python, чтобы он точно отпустил Bluetooth
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Stop-Process -Force" >nul 2>&1

:: Даем Windows 2 секунды на полное освобождение Bluetooth-модуля
timeout /t 2 /nobreak >nul

echo [2/3] Scanning and selecting new device...
python main.py --reset

echo [3/3] Resuming background service...
:: Запускаем фоновую службу обратно
schtasks /run /tn "HeartRateService" >nul

echo.
echo ========================================================
echo SUCCESS! Device updated and background service resumed!
echo ========================================================
pause