# Data Science & AI Job-Ready Hub - Launcher PowerShell
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  🚀 Iniciando Data Science & AI Job-Ready Hub..." -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[INFO] Configurando entorno virtual .venv..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r daily_training\requirements.txt
} else {
    & .\.venv\Scripts\Activate.ps1
}

python daily_training\runner.py

