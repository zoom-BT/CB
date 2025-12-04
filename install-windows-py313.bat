@echo off
REM Script d'installation specifique pour Python 3.13 sur Windows
echo.
echo ========================================
echo   Installation NIRD (Python 3.13)
echo ========================================
echo.

echo Verification de Python...
python --version
echo.

echo Nettoyage de l'environnement virtuel...
if exist venv (
    rmdir /s /q venv
    echo Ancien environnement supprime
)

echo.
echo Creation d'un nouvel environnement virtuel...
python -m venv venv

echo.
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo Installation des dependances...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERREUR lors de l'installation!
    echo ========================================
    echo.
    echo Consultez TROUBLESHOOTING.md pour l'aide
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Pour lancer l'API:
echo   1. Activez l'environnement: venv\Scripts\activate
echo   2. Lancez l'API: python run.py
echo.
pause
