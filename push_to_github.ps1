# AgriPredict AI GitHub Push Script for PowerShell

$gitDir = "$env:LOCALAPPDATA\Programs\Git\cmd"
if (Test-Path "$gitDir\git.exe") {
    $env:Path = "$gitDir;" + $env:Path
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Pushing AgriPredict AI to GitHub: S-MOHAN-91" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: https://github.com/S-MOHAN-91/agripredict-ai.git" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot

& git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Pushed successfully to GitHub!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Note: If prompted for authentication, enter your GitHub Personal Access Token (PAT):" -ForegroundColor Yellow
    Write-Host "https://github.com/settings/tokens (scope: repo)" -ForegroundColor Gray
}
