# scripts/dev.ps1
Write-Host "=== Starting IdeaOS Services ===" -ForegroundColor Cyan

# Start Backend Server
$BackendJob = Start-Job -ScriptBlock {
    Set-Location "d:\open source projects\AI Operating System for Ideas\backend"
    & "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
}

Write-Host "FastAPI Backend launched on http://127.0.0.1:8000" -ForegroundColor Gray

# Start Frontend
Set-Location "d:\open source projects\AI Operating System for Ideas\frontend"
npm run dev

# Cleanup jobs on exit
Stop-Job $BackendJob
Remove-Job $BackendJob
Set-Location ..
