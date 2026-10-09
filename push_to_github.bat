@echo off
setlocal

:: Ensure Git is in PATH
set "GIT_PATH=%LOCALAPPDATA%\Programs\Git\cmd"
if exist "%GIT_PATH%\git.exe" (
    set "PATH=%GIT_PATH%;%PATH%"
)

echo ========================================================
echo   Pushing AgriPredict AI to GitHub: S-MOHAN-91
echo ========================================================
echo.
echo Target Repository: https://github.com/S-MOHAN-91/agripredict-ai.git
echo Branch: main
echo.
echo NOTE: Make sure the repository exists on GitHub:
echo https://github.com/new (Name: agripredict-ai)
echo.
echo Pushing branch 'main' to origin...
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ----------------------------------------------------------------------
    echo Push did not complete. If prompted for password:
    echo Use a GitHub Personal Access Token (PAT) with 'repo' scope:
    echo https://github.com/settings/tokens
    echo ----------------------------------------------------------------------
) else (
    echo.
    echo [SUCCESS] Code successfully pushed to https://github.com/S-MOHAN-91/agripredict-ai !
)

echo.
pause
