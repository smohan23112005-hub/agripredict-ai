$pyExe = "$env:LOCALAPPDATA\Programs\Python311\python.exe"
if (-not (Test-Path $pyExe)) {
    $pyExe = "python"
}
Write-Host "Starting AgriPredict AI FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
Set-Location -Path "$PSScriptRoot\backend"
& $pyExe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
