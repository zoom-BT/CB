@echo off
REM Script de test Windows pour l'API NIRD
echo.
echo ========================================
echo   Tests NIRD Chatbot API
echo ========================================
echo.

python -m pytest tests/ -v --tb=short

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Des tests ont echoue!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Tous les tests sont passes!
echo ========================================
pause
