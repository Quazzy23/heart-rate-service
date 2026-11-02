@echo off
title Heart Rate Service Installer
cd /d "%~dp0"

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ========================================================
    echo  Access denied.
    echo  Please run this script as Administrator.
    echo ========================================================
    pause
    exit /b
)

echo [1/4] Safely stopping old tasks...
schtasks /end /tn "HeartRateService" >nul 2>&1
schtasks /delete /tn "HeartRateService" /f >nul 2>&1
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Stop-Process -Force" >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/4] Checking Python dependencies...
:: Скрываем весь технический вывод, оставляем только ошибки, если они будут
python -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies. Check your internet connection.
    pause
    exit /b
)

echo [3/4] Scanning for Bluetooth devices...
python main.py --reset

if not exist "config.json" (
    echo.
    echo ERROR: Configuration not found. Device setup was not completed.
    pause
    exit /b
)

echo [4/4] Registering Background Task: HeartRateService...
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
set PYTHONW_PATH=%PYTHON_PATH:python.exe=pythonw.exe%
set SCRIPT_PATH=%~dp0main.py

schtasks /create /tn "HeartRateService" /tr "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\" --server" /sc onlogon /f
schtasks /run /tn "HeartRateService"

echo.
echo ========================================================
echo SUCCESS! Task registered and running!
echo ========================================================
pause