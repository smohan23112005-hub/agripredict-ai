@echo off
setlocal

set "GIT_PATH=%LOCALAPPDATA%\Programs\Git\cmd"
if exist "%GIT_PATH%\git.exe" (
    set "PATH=%GIT_PATH%;%PATH%"
)

echo ========================================================
echo   Pushing AgriPredict AI to GitHub
echo ========================================================
echo.
echo Target: https://github.com/smohan23112005-hub/agripredict-ai.git
echo Branch: main
echo.
echo Pushing branch 'main' to origin...
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ----------------------------------------------------------------------
    echo Push incomplete.
    echo If prompted, complete the GitHub login in your browser, or use a PAT:
    echo https://github.com/settings/tokens
    echo ----------------------------------------------------------------------
) else (
    echo.
    echo [SUCCESS] Code successfully pushed to https://github.com/smohan23112005-hub/agripredict-ai !
)

echo.
pause
