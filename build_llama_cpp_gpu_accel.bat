@echo off
echo ================================================
echo 🛠️ Building llama-cpp-python (stable v0.2.24)
echo ================================================

:: Step 1: Create build folder
mkdir llama_build_temp
cd llama_build_temp

:: Step 2: Clone the repo
git clone --branch v0.2.24 https://github.com/abetlen/llama-cpp-python.git
cd llama-cpp-python

:: Step 3: Install required packages
pip install --upgrade pip setuptools wheel cmake

:: Step 4: Enable AVX2 + FMA support
set CMAKE_ARGS=-DLLAMA_AVX2=ON -DLLAMA_FMA=ON

:: Step 5: Build and install llama-cpp-python
pip install . --force-reinstall --verbose

echo ✅ Successfully built with AVX2 + FMA!
pause
