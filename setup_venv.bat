@echo off
SETLOCAL

echo 🚀 Setting up your myAI environment...

:: Step 1: Navigate to project folder
cd /d %~dp0

:: Step 2: Check if venv exists
if not exist venv (
    echo 🧪 Creating virtual environment...
    python -m venv venv
) else (
    echo ⚙️ Virtual environment already exists.
)

:: Step 3: Activate virtual environment
call venv\Scripts\activate.bat

:: Step 4: Install required packages
echo 📦 Installing dependencies from requirements.txt...
pip install -r requirements.txt

:: Step 5: Confirm setup
echo ✅ Setup complete! Virtual environment is ready and activated.
echo 🔐 Make sure your .env file has your OPENAI_API_KEY.

:: Keep the command window open
cmd /k
