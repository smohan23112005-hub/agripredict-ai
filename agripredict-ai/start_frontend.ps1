$npmCmd = "$env:LOCALAPPDATA\Programs\NodeJS\npm.cmd"
if (-not (Test-Path $npmCmd)) {
    $npmCmd = "npm"
}
Write-Host "Starting AgriPredict AI Frontend on http://localhost:5173..." -ForegroundColor Green
Set-Location -Path "$PSScriptRoot\frontend"
& $npmCmd run dev
