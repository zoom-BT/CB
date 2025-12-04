# Script PowerShell d'installation pour NIRD Chatbot API

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Installation NIRD Chatbot API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python n'est pas installé ou n'est pas dans le PATH!" -ForegroundColor Red
    Write-Host "  Téléchargez Python depuis: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Créer un environnement virtuel (optionnel mais recommandé)
$createVenv = Read-Host "Créer un environnement virtuel? (o/N)"
if ($createVenv -eq "o" -or $createVenv -eq "O") {
    Write-Host ""
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv

    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

# Mettre à jour pip
Write-Host ""
Write-Host "1️⃣ Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null

# Installer les dépendances
Write-Host ""
Write-Host "2️⃣ Installation des dépendances..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Installation terminée avec succès!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour lancer l'API:" -ForegroundColor Cyan
    Write-Host "  python run.py" -ForegroundColor White
    Write-Host "  ou" -ForegroundColor White
    Write-Host "  .\run.bat" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Erreur lors de l'installation!" -ForegroundColor Red
    Write-Host "Consultez les messages d'erreur ci-dessus." -ForegroundColor Yellow
    exit 1
}
