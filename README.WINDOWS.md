# NIRD Chatbot API - Guide Windows 🪟

> Instructions spécifiques pour Windows 10/11

## 🚀 Installation rapide (Windows)

### Méthode 1 : Scripts automatiques (Recommandé)

1. **Installer Python** (si ce n'est pas déjà fait)
   - Télécharger Python 3.10+ depuis [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important** : Cocher "Add Python to PATH" lors de l'installation

2. **Installer les dépendances**
   ```cmd
   install.bat
   ```
   Double-cliquez sur `install.bat` ou lancez dans cmd/PowerShell

3. **Lancer l'API**
   ```cmd
   run.bat
   ```
   Double-cliquez sur `run.bat` ou lancez dans cmd/PowerShell

### Méthode 2 : Installation manuelle

```cmd
# Ouvrir PowerShell ou cmd dans le dossier du projet

# 1. Installer les dépendances
python -m pip install -r requirements.txt

# 2. Lancer l'API
python run.py

# Ou avec uvicorn directement
python -m uvicorn app.main:app --reload
```

## 🧪 Lancer les tests

### Avec le script
```cmd
test.bat
```

### Manuellement
```cmd
python -m pytest tests/ -v
```

## 📝 Tester l'API avec PowerShell

### 1. Tester l'endpoint racine
```powershell
Invoke-RestMethod -Uri http://localhost:8000/ -Method Get
```

### 2. Tester le health check
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health -Method Get
```

### 3. Lancer un scraping
```powershell
$body = @{
    urls = @("https://nird.forge.apps.education.fr/")
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/scrape -Method Post -Body $body -ContentType "application/json"
```

### 4. Voir les statistiques
```powershell
Invoke-RestMethod -Uri http://localhost:8000/data/stats -Method Get
```

## 🔧 Tester l'API avec curl (Git Bash / WSL)

Si vous avez Git Bash ou WSL installé :

```bash
# Test scraping
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://nird.forge.apps.education.fr/"]}'

# Voir les stats
curl http://localhost:8000/data/stats
```

## 📊 Documentation interactive

Une fois l'API lancée, ouvrez votre navigateur :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

Vous pourrez tester tous les endpoints directement depuis le navigateur !

## 🐛 Résolution de problèmes (Windows)

### Erreur "python n'est pas reconnu"
```cmd
# Vérifier que Python est installé
python --version

# Si erreur, réinstaller Python et cocher "Add to PATH"
```

### Erreur lors de l'installation de lxml
```cmd
# Installer Visual C++ Build Tools
# Télécharger depuis: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Ou utiliser une version précompilée
pip install --only-binary :all: lxml
```

### Erreur de permissions
```cmd
# Lancer cmd ou PowerShell en tant qu'administrateur
# Clic droit > "Exécuter en tant qu'administrateur"
```

### Le port 8000 est déjà utilisé
```cmd
# Trouver le processus
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID par le numéro)
taskkill /PID <PID> /F

# Ou changer le port dans run.py (ligne avec --port)
```

## 📁 Structure des fichiers (Windows)

```
CB\
├── app\
│   ├── main.py
│   ├── config.py
│   └── modules\scraper\
├── tests\
├── data\
│   └── scraped_data.json
├── requirements.txt
├── run.py              # Script de lancement cross-platform
├── install.py          # Script d'installation cross-platform
├── run.bat             # Raccourci Windows
├── install.bat         # Raccourci Windows
├── test.bat            # Raccourci Windows
└── README.md
```

## 🎯 Étapes suivantes

1. ✅ Module de scraping fonctionnel
2. ⏳ Module d'indexation vectorielle (ChromaDB, FAISS)
3. ⏳ Module d'interfaçage IA (Gemini)
4. ⏳ Chatbot Chat'bruti

## 💡 Astuces Windows

### Utiliser un environnement virtuel (recommandé)

```cmd
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (cmd)
venv\Scripts\activate.bat

# Activer l'environnement (PowerShell)
venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### Script PowerShell pour tout installer automatiquement

```powershell
# install.ps1
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Installation terminée! Lancez 'python run.py'"
```

## 🔗 Ressources

- [Python Windows](https://www.python.org/downloads/windows/)
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- [Git for Windows](https://gitforwindows.org/)
- [Windows Terminal](https://www.microsoft.com/store/productId/9N0DX20HK701)

## 📞 Support

En cas de problème pendant la Nuit de l'Info, contactez votre équipe ou les organisateurs !
