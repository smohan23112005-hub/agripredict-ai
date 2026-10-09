@echo off
echo ===================================================
echo   AgriPredict AI - Full Stack Runner
echo ===================================================
echo.
echo Starting Backend and Frontend services...
start "AgriPredict Backend" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0start_backend.ps1"
timeout /t 3 /nobreak >nul
start "AgriPredict Frontend" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0start_frontend.ps1"
echo.
echo Services launched!
echo - Backend:  http://localhost:8000 (API Docs at /docs)
echo - Frontend: http://localhost:5173
echo.
