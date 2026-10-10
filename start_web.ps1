# Counterfeit Detector Web Platform Launcher
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\services\api"
$env:PYTHONPATH = ".;..\..\packages"

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Counterfeit Detector Web Platform (Production)    " -ForegroundColor Cyan
Write-Host " Target Products: Panadol, Coca-Cola, Colgate     " -ForegroundColor Yellow
Write-Host " Access Web UI at: http://localhost:8000          " -ForegroundColor Green
Write-Host " API Docs at:      http://localhost:8000/docs     " -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Green

& ".\.venv\Scripts\uvicorn.exe" app.main:app --host 0.0.0.0 --port 8000 --reload
