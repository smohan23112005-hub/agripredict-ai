# AgriPredict AI GitHub Push Script for PowerShell

$gitDir = "$env:LOCALAPPDATA\Programs\Git\cmd"
if (Test-Path "$gitDir\git.exe") {
    $env:Path = "$gitDir;" + $env:Path
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Pushing AgriPredict AI to GitHub" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: https://github.com/smohan23112005-hub/agripredict-ai.git" -ForegroundColor Yellow
Write-Host "Branch: main" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot

& git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Pushed successfully to https://github.com/smohan23112005-hub/agripredict-ai !" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Please complete the browser authentication or provide your GitHub Personal Access Token." -ForegroundColor Yellow
}
