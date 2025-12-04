# 🚀 Démarrage rapide - NIRD Chatbot API

## Pour les pressés (Nuit de l'Info) ⚡

### Windows 🪟

1. **Double-cliquez sur** `install.bat`
2. **Double-cliquez sur** `run.bat`
3. **Ouvrez** http://localhost:8000/docs dans votre navigateur
4. **Testez** l'API directement depuis la page Swagger

### Linux / macOS 🐧🍎

```bash
python install.py
python run.py
```

Puis ouvrez http://localhost:8000/docs

---

## Test rapide de l'API

### Depuis le navigateur
1. Allez sur http://localhost:8000/docs
2. Cliquez sur `POST /scrape`
3. Cliquez sur "Try it out"
4. Entrez :
```json
{
  "urls": ["https://nird.forge.apps.education.fr/"]
}
```
5. Cliquez sur "Execute"

### Depuis PowerShell (Windows)
```powershell
$body = @{urls = @("https://nird.forge.apps.education.fr/")} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/scrape -Method Post -Body $body -ContentType "application/json"
```

### Depuis cmd avec curl (Windows + Git Bash)
```bash
curl -X POST http://localhost:8000/scrape -H "Content-Type: application/json" -d "{\"urls\": [\"https://nird.forge.apps.education.fr/\"]}"
```

---

## Structure du projet

```
CB/
├── run.bat           ← Double-cliquez ici pour lancer (Windows)
├── install.bat       ← Double-cliquez ici pour installer (Windows)
├── run.py            ← Script de lancement cross-platform
├── app/
│   ├── main.py       ← API FastAPI
│   └── modules/scraper/
└── tests/            ← 20 tests unitaires
```

---

## Endpoints principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Info API |
| `/health` | GET | Health check |
| `/scrape` | POST | Scraper des URLs |
| `/data` | GET | Récupérer les données |
| `/data/stats` | GET | Statistiques |

---

## Prochaines étapes

1. ✅ Module de scraping → **FAIT**
2. ⏳ Module d'indexation vectorielle
3. ⏳ Module d'IA (Gemini)
4. ⏳ Chatbot Chat'bruti absurde

---

## Besoin d'aide ?

- 📖 Documentation complète : [README.md](README.md)
- 🪟 Instructions Windows : [README.WINDOWS.md](README.WINDOWS.md)
- 🌐 Documentation API : http://localhost:8000/docs (après lancement)
