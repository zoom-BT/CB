@echo off
REM Script de lancement Windows pour l'API NIRD
echo.
echo ========================================
echo   NIRD Chatbot API - Nuit de l'Info
echo ========================================
echo.

python run.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Erreur lors du lancement!
    pause
)
