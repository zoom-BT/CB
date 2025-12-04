# 🚀 Démarrage rapide - Module 2 (Pinecone)

## Étape 1 : Obtenir une clé API Pinecone (GRATUIT) ⚡

1. Allez sur **https://www.pinecone.io/**
2. Cliquez sur **"Start Free"**
3. Créez un compte (Google/GitHub ou email)
4. Dans le dashboard, allez dans **"API Keys"**
5. Copiez votre clé API

**C'est gratuit** : 100 000 vecteurs gratuitement !

---

## Étape 2 : Configurer votre clé API 🔑

**Windows (PowerShell) :**
```powershell
# Créer un fichier .env
Copy-Item .env.example .env

# Éditer avec Notepad
notepad .env

# Remplacer cette ligne:
PINECONE_API_KEY=your-pinecone-api-key-here
# Par votre vraie clé:
PINECONE_API_KEY=pcsk_123456_abcdef...
```

**Linux/macOS :**
```bash
cp .env.example .env
nano .env  # ou vim, ou votre éditeur préféré

# Remplacer:
PINECONE_API_KEY=pcsk_123456_votre_cle
```

---

## Étape 3 : Installer les dépendances 📦

```bash
pip install -r requirements.txt
```

**Note** : Le premier lancement téléchargera le modèle d'embeddings (~120MB)

---

## Étape 4 : Lancer l'API 🚀

```bash
python run.py
```

Ouvrez http://localhost:8000/docs

---

## Étape 5 : Tester le Module 2 🧪

### Test 1 : Indexer les données

Dans Swagger UI (http://localhost:8000/docs) :

1. Allez sur **POST /vector/index**
2. Cliquez **"Try it out"**
3. Utilisez ce JSON :
```json
{
  "data_file": "scraped_data.json",
  "namespace": "",
  "batch_size": 32
}
```
4. Cliquez **"Execute"**

**Résultat attendu :**
```json
{
  "success": true,
  "message": "Indexation terminée: 11 chunks",
  "indexed_count": 11,
  "index_name": "nird-chatbot"
}
```

⏱️ **Durée** : ~10-20 secondes (téléchargement du modèle + indexation)

---

### Test 2 : Rechercher "C'est quoi NIRD ?"

1. Allez sur **POST /vector/search**
2. Cliquez **"Try it out"**
3. Utilisez ce JSON :
```json
{
  "query": "C'est quoi NIRD ?",
  "top_k": 3
}
```
4. Cliquez **"Execute"**

**Résultat attendu :**
```json
{
  "query": "C'est quoi NIRD ?",
  "count": 3,
  "results": [
    {
      "score": 0.82,
      "text": "La démarche NIRD vise à promouvoir un numérique libre...",
      "source_url": "https://nird.forge.apps.education.fr/",
      "source_title": "Accueil"
    },
    ...
  ]
}
```

✅ **Ça marche !** Le module 2 trouve les chunks les plus pertinents !

---

### Test 3 : Statistiques de l'index

1. Allez sur **GET /vector/stats**
2. Cliquez **"Try it out"** → **"Execute"**

**Résultat attendu :**
```json
{
  "success": true,
  "stats": {
    "total_vector_count": 11,
    "dimension": 384,
    "index_fullness": 0.0001
  }
}
```

---

## 🎭 Essayez d'autres recherches !

### Recherches sémantiques qui fonctionnent :

- `"logiciel libre"`
- `"obsolescence programmée"`
- `"établissements scolaires"`
- `"numérique écologique"`
- `"Linux éducation"`
- `"autonomie technologique"`

### 💡 Comparez avec des mots-clés inexacts :

- `"éco-responsable"` → trouve "durable", "écologique"
- `"collèges lycées"` → trouve "établissements scolaires"
- `"open source"` → trouve "logiciel libre"

C'est la **magie de la recherche sémantique** ! 🪄

---

## 🐛 Problèmes courants

### Erreur : "PINECONE_API_KEY non configurée"

**Solution :**
- Vérifiez que vous avez bien créé le fichier `.env`
- Vérifiez que la clé est sur la ligne `PINECONE_API_KEY=pcsk_...`
- Relancez l'API : `python run.py`

### Erreur : "401 Unauthorized" de Pinecone

**Solution :**
- Votre clé API est invalide
- Reconnectez-vous à Pinecone et récupérez une nouvelle clé
- Mettez à jour le `.env` et relancez

### Téléchargement du modèle trop lent

**Solution :**
- C'est normal la première fois (~120MB)
- Les fois suivantes c'est instantané (modèle en cache)

---

## 📊 Workflow complet (Modules 1 + 2)

```bash
# 1. Scraper le site NIRD
POST /scrape {"urls": ["https://nird.forge.apps.education.fr/"]}

# 2. Indexer dans Pinecone
POST /vector/index {"data_file": "scraped_data.json"}

# 3. Chercher des infos
POST /vector/search {"query": "NIRD c'est quoi ?"}
```

---

## ✅ Checklist de validation

- [ ] Clé API Pinecone récupérée
- [ ] Fichier `.env` créé avec la clé
- [ ] Dépendances installées
- [ ] API lancée sur http://localhost:8000
- [ ] Test 1 : Indexation réussie (11 chunks)
- [ ] Test 2 : Recherche "C'est quoi NIRD ?" fonctionne
- [ ] Test 3 : Statistiques affichées

Si tous les ✅ sont cochés → **Module 2 opérationnel** ! 🎉

---

## 🚀 Prochaine étape : Module 3

Le Module 3 utilisera les résultats de recherche pour :
- Envoyer le contexte pertinent à Gemini
- Générer des réponses avec une personnalité absurde (Chat'bruti)
- Compléter le chatbot NIRD !

**Besoin d'aide ?** Consultez [MODULE2_README.md](MODULE2_README.md) pour la doc complète.
