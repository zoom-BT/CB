# Script PowerShell de lancement pour NIRD Chatbot API

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NIRD Chatbot API" -ForegroundColor Cyan
Write-Host "   Nuit de l'Info 2025" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que les dépendances sont installées
try {
    python -c "import fastapi" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "FastAPI not found"
    }
} catch {
    Write-Host "✗ Dépendances manquantes!" -ForegroundColor Red
    Write-Host "  Installez-les avec: python install.py" -ForegroundColor Yellow
    Write-Host "  ou: .\install.bat" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Démarrage de l'API..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 URL API: " -NoNewline -ForegroundColor Yellow
Write-Host "http://localhost:8000" -ForegroundColor White
Write-Host "📚 Documentation: " -NoNewline -ForegroundColor Yellow
Write-Host "http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Gray
Write-Host ""

# Lancer l'API
try {
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
} catch {
    Write-Host ""
    Write-Host "✗ Erreur lors du lancement!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Serveur arrêté proprement" -ForegroundColor Green
