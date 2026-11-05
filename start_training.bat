@echo off
chcp 65001 > nul
title Data Science & AI Job-Ready Hub - Daily Training

:: Cambiar al directorio del script
cd /d "%~dp0"

echo ==============================================================================
echo   🚀 Iniciando Data Science & AI Job-Ready Hub...
echo ==============================================================================

:: Comprobar si existe el entorno virtual
if not exist ".venv" (
    echo [INFO] Creando entorno virtual .venv por primera vez...
    python -m venv .venv
    echo [INFO] Instalando dependencias necesarias (pytest, duckdb, pandas, rich...)...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r daily_training\requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: Lanzar el runner interactivo
python daily_training\runner.py

pause

