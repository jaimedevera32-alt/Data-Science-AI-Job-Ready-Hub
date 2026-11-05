@echo off
setlocal
cd /d "%~dp0"

echo ==============================================================================
echo   Iniciando Data Science ^& AI Job-Ready Hub...
echo ==============================================================================

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Configurando entorno virtual .venv...
    "C:\Program Files\Python314\python.exe" -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r daily_training\requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

python daily_training\runner.py

pause