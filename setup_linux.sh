#!/bin/bash

LOGDIR="logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/setup_log.txt"
echo "📋 Logging to $LOGFILE..."

{
echo "==== SETUP STARTED ===="

if [[ "$1" == "--reset" ]]; then
  echo "🧹 Resetting profiles..."
  rm -f prompts/user_profiles.json
  rm -f prompts/assistant_profiles.json
fi

if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ Python not found. Install Python 3.10+ and re-run."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON -m venv venv
fi

source venv/bin/activate

$PYTHON -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

echo "🎙 Installing PyAudio..."
sudo apt-get install -y portaudio19-dev
pip install pyaudio

echo "⚙️ Running setup..."
$PYTHON setup.py

echo "🚀 Launching assistant..."
$PYTHON main.py

echo "==== SETUP COMPLETE ===="
} &> "$LOGFILE"

echo "✅ Done! Log saved to $LOGFILE"
