# scripts/setup.ps1
Write-Host "=== Initializing IdeaOS Dev Environment (Windows) ===" -ForegroundColor Cyan

# 1. Setup python environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment in .venv..." -ForegroundColor Gray
    python -m venv .venv
}

# Activate and install dependencies
Write-Host "Installing backend dependency modules..." -ForegroundColor Gray
& .venv\Scripts\pip.exe install --upgrade pip
& .venv\Scripts\pip.exe install -e backend --use-pep517

# 2. Setup Node frontend
Write-Host "Installing React Node modules..." -ForegroundColor Gray
Set-Location frontend
npm install
Set-Location ..

# 3. Create database path
if (-not (Test-Path "backend\data")) {
    New-Item -ItemType Directory -Path "backend\data" | Out-Null
}

Write-Host "===============================================" -ForegroundColor Green
Write-Host "Bootstrap complete. Run './scripts/dev.ps1' to launch." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
