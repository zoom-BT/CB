# 🔧 Guide de Dépannage Windows - Python 3.13

## ⚠️ Problème avec Python 3.13

Si vous utilisez **Python 3.13**, vous pouvez rencontrer des erreurs lors de l'installation car certaines versions anciennes de packages nécessitent Rust pour compiler.

### ✅ Solution : Requirements mis à jour

Le fichier `requirements.txt` a été mis à jour avec des versions compatibles Python 3.13 qui ont des **binaires précompilés (wheels)**.

## 🚀 Installation sur Windows avec Python 3.13

### Étape 1 : Vérifier votre version de Python

```powershell
python --version
# ou
py --version
```

Si vous voyez `Python 3.13.x`, suivez ce guide.

### Étape 2 : Nettoyer et réinstaller

```powershell
# Dans le dossier CB

# 1. Supprimer l'ancien environnement virtuel (si existant)
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# 2. Créer un nouvel environnement virtuel
py -3 -m venv venv

# 3. Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# 4. Mettre à jour pip
python -m pip install --upgrade pip

# 5. Installer les dépendances
pip install -r requirements.txt
```

### Étape 3 : Lancer l'API

```powershell
# Avec l'environnement virtuel activé
python run.py

# Ou directement
python -m uvicorn app.main:app --reload
```

## 🎯 Installation simple (sans environnement virtuel)

Si vous ne voulez pas créer d'environnement virtuel :

```powershell
# Installer directement
py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt

# Lancer l'API
py -3 run.py
```

## 📋 Vérification que tout fonctionne

```powershell
# Tester les imports
python -c "import fastapi; import uvicorn; import tiktoken; print('✅ Toutes les dépendances sont installées!')"

# Lancer les tests
pytest tests/ -v
```

## 🐛 Problèmes courants et solutions

### Erreur : "pydantic-core requires Rust"

**Cause :** Anciennes versions de pydantic-core sans wheels pour Python 3.13

**Solution :**
```powershell
# Utiliser le requirements.txt mis à jour
pip install -r requirements.txt

# Ou installer manuellement les versions récentes
pip install "pydantic>=2.10.0" "fastapi>=0.115.0"
```

### Erreur : "lxml compilation failed"

**Cause :** lxml essaie de compiler depuis les sources

**Solution :**
```powershell
# Installer uniquement les binaires précompilés
pip install --only-binary :all: lxml

# Ou installer une version récente avec wheels
pip install "lxml>=5.3.0"
```

### Erreur : "tiktoken needs to compile C extensions"

**Cause :** Ancienne version de tiktoken sans wheels Python 3.13

**Solution :**
```powershell
# Installer la version récente
pip install "tiktoken>=0.8.0"
```

### Erreur : "Microsoft Visual C++ 14.0 is required"

**Cause :** Tentative de compilation depuis les sources

**Solution 1 (Recommandée) :**
```powershell
# Utiliser uniquement des binaires précompilés
pip install --only-binary :all: -r requirements.txt
```

**Solution 2 (Si ça ne marche pas) :**
Installer Visual Studio Build Tools :
1. Télécharger depuis : https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Installer "Desktop development with C++"
3. Réessayer l'installation

### Erreur : "python n'est pas reconnu"

**Solution :**
```powershell
# Utiliser py à la place
py -3 --version
py -3 -m pip install -r requirements.txt
py -3 run.py
```

## 🔄 Réinitialisation complète

Si rien ne fonctionne, réinitialisez tout :

```powershell
# 1. Supprimer l'environnement virtuel
Remove-Item -Recurse -Force venv

# 2. Nettoyer le cache pip
pip cache purge

# 3. Recréer l'environnement
py -3 -m venv venv
.\venv\Scripts\Activate.ps1

# 4. Installer proprement
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 📊 Versions recommandées

Pour Python 3.13, utilisez ces versions minimales :

| Package | Version min | Raison |
|---------|-------------|--------|
| fastapi | 0.115.0 | Support Python 3.13 |
| pydantic | 2.10.0 | Wheels précompilés |
| uvicorn | 0.32.0 | Compatibilité récente |
| tiktoken | 0.8.0 | Wheels Python 3.13 |
| lxml | 5.3.0 | Wheels Python 3.13 |

## 💡 Alternative : Utiliser Python 3.11 ou 3.12

Si vous rencontrez trop de problèmes avec Python 3.13 :

1. Télécharger Python 3.11 ou 3.12 depuis python.org
2. Installer en parallèle de Python 3.13
3. Utiliser explicitement cette version :

```powershell
# Utiliser Python 3.11
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## ✅ Vérification finale

Après installation, testez que tout fonctionne :

```powershell
# 1. Tester les imports
python -c "import fastapi, uvicorn, tiktoken, lxml; print('✅ OK')"

# 2. Lancer les tests
pytest tests/ -v

# 3. Démarrer l'API
python run.py
```

Ouvrez http://localhost:8000/docs pour vérifier que l'API fonctionne.

## 📞 Besoin d'aide ?

Si les problèmes persistent, partagez :
1. Votre version Python (`python --version`)
2. Le message d'erreur complet
3. Votre système d'exploitation (Windows 10/11)

---

**Note :** Le fichier `requirements.txt` principal utilise maintenant des versions `>=` au lieu de `==` pour permettre l'installation des versions les plus récentes compatibles avec votre Python.
