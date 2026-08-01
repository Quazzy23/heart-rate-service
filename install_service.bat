@echo off
cd /d "%~dp0"

echo [1/3] Cleaning up previous tasks...
schtasks /delete /tn "HeartRateService" /f >nul 2>&1

echo [2/3] Checking Python dependencies...
python -m pip install -r requirements.txt

echo [3/3] Registering Background Task: HeartRateService...
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
set PYTHONW_PATH=%PYTHON_PATH:python.exe=pythonw.exe%
set SCRIPT_PATH=%~dp0main.py

:: Регистрируем фоновую задачу для обычного пользователя без прав админа
schtasks /create /tn "HeartRateService" /tr "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\" --server" /sc onlogon /f >nul
schtasks /run /tn "HeartRateService" >nul

echo.
echo ========================================================
echo SUCCESS! Heart Rate Task registered and running!
echo ========================================================
pause