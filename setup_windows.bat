@echo off
setlocal

set RESET=%1

if "%RESET%"=="--reset" (
    echo 🧹 Resetting profiles...
    del /q prompts\user_profiles.json 2>nul
    del /q prompts\assistant_profiles.json 2>nul
)

python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing Python 3.10.11...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

python -m pip install --upgrade pip

if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
)

echo Installing PyAudio...
pip install pipwin
pipwin install pyaudio

echo Running setup...
python setup.py

echo Launching assistant...
python main.py

endlocal
pause
