@echo off
REM Script d'installation Windows pour l'API NIRD
echo.
echo ========================================
echo   Installation NIRD Chatbot API
echo ========================================
echo.

python install.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Erreur lors de l'installation!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee!
echo Pour lancer l'API: run.bat
echo ========================================
pause
