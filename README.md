# 🤖 NIRD Chatbot API - Nuit de l'Info 2025

API complète combinant les défis **NIRD** (Numérique Inclusif, Responsable et Durable) et **Chat'bruti** pour la Nuit de l'Info 2025.

## 🎯 Concept

Un chatbot humoristique qui sensibilise au numérique responsable de manière absurde et décalée :
- **Module 1** : Scrape le site NIRD et découpe le contenu en chunks
- **Module 2** : Recherche sémantique pour trouver le contexte pertinent
- **Module 3** : Chatbot Chat-Bruti qui génère des réponses absurdes mais éducatives

## ⚡ Installation rapide (Windows)

### 1. Prérequis
- Python 3.13+
- Git

### 2. Installation

```powershell
# Cloner le projet
git clone https://github.com/zoom-BT/CB.git
cd CB

# Installer les dépendances
py -m pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` avec votre clé Groq (gratuite) :

```bash
# Obtenez votre clé gratuite sur: https://console.groq.com/keys
GROQ_API_KEY=votre-clé-groq-ici
GROQ_MODEL=llama-3.3-70b-versatile
CHATBOT_TEMPERATURE=1.5
CHATBOT_MAX_TOKENS=200
```

### 4. Lancer l'API

```powershell
py run.py
```

L'API sera accessible sur **http://localhost:8000**

Documentation interactive : **http://localhost:8000/docs**

## 📚 Utilisation

### Workflow complet

#### 1. Scraper les données NIRD (Module 1)

```bash
POST /scrape
{
  "urls": ["https://nird.forge.apps.education.fr/"]
}
```

**Note** : Les données sont déjà scrapées dans `data/scraped_data.json`, cette étape est optionnelle.

#### 2. Rechercher un contexte pertinent (Module 2)

```bash
POST /semantic/search
{
  "question": "C'est quoi Linux ?"
}
```

**Réponse** :
```json
{
  "question": "C'est quoi Linux ?",
  "contexte": "Linux est un système d'exploitation libre utilisé dans les écoles...",
  "confiance": 0.856,
  "chunk_id": 12,
  "source_url": "https://nird.forge.apps.education.fr/linux/",
  "source_title": "Linux dans l'éducation"
}
```

#### 3. Obtenir une réponse absurde de Chat-Bruti (Module 3)

```bash
POST /chatbot/ask
{
  "question": "C'est quoi Linux ?",
  "contexte": "Linux est un système d'exploitation libre..."
}
```

**Réponse** :
```json
{
  "response": "Waouh, Linux ? C'est comme un pingouin philosophe qui refuse de payer Windows ! Yeahh, l'écologie numérique à son paroxysme : un OS qui tourne sur une patate et qui juge ton empreinte carbone. Oups, j'en ai trop dit..."
}
```

### Endpoint simplifié (Module 2 + 3 combinés)

```bash
POST /chatbot/chat
{
  "question": "Pourquoi le reconditionnement c'est bien ?"
}
```

Cette route fait automatiquement la recherche sémantique puis génère la réponse.

## 🛠️ Architecture technique

### Module 1 - Scraping
- **BeautifulSoup4** : Extraction du contenu web
- **LangChain** : Découpage intelligent en chunks
- **tiktoken** : Comptage des tokens (encodage cl100k_base)
- Export JSON optimisé (~60% plus léger)

### Module 2 - Recherche sémantique
- **TF-IDF** + Similarité cosinus (pas de dépendances externes)
- Stopwords français
- Boost de mots-clés NIRD (linux, reconditionnement, libre, etc.)
- Historique sauvegardé en JSON

### Module 3 - Chatbot Chat-Bruti
- **Groq API** : LLM gratuit (llama-3.3-70b-versatile)
- Personnalité absurde et philosophique
- Temperature élevée (1.5) pour plus de créativité
- Détourne le contexte de manière humoristique

## 📁 Structure du projet

```
CB/
├── app/
│   ├── modules/
│   │   ├── scraper/          # Module 1
│   │   │   ├── scraper.py
│   │   │   ├── chunker.py
│   │   │   └── exporter.py
│   │   ├── semantic/         # Module 2
│   │   │   ├── semantic_search.py
│   │   │   └── history_manager.py
│   │   └── chatbot/          # Module 3
│   │       └── chatbruti.py
│   ├── routes/
│   │   ├── semantic_routes.py
│   │   └── chatbot_routes.py
│   ├── config.py
│   └── main.py
├── data/
│   ├── scraped_data.json     # Données NIRD (déjà scrapées)
│   └── historique_recherches.json
├── requirements.txt
├── run.py
└── README.md
```

## 🚀 Endpoints disponibles

### Module 1 - Scraping
- `POST /scrape` - Scraper des URLs
- `GET /data` - Récupérer les données scrapées
- `GET /data/stats` - Statistiques des données

### Module 2 - Recherche sémantique
- `POST /semantic/search` - Rechercher le meilleur contexte
- `GET /semantic/stats` - Statistiques du moteur de recherche
- `GET /semantic/history` - Historique des recherches
- `DELETE /semantic/history/clear` - Vider l'historique

### Module 3 - Chatbot
- `GET /chatbot/` - Informations sur Chat-Bruti
- `POST /chatbot/ask` - Poser une question avec contexte
- `POST /chatbot/chat` - Interface simplifiée (recherche + réponse)

### Général
- `GET /` - Page d'accueil avec la liste des modules
- `GET /health` - Vérification de l'état de l'API
- `GET /docs` - Documentation Swagger interactive

## 🎭 Personnalité Chat-Bruti

Chat-Bruti est un chatbot volontairement absurde qui :
- Ne répond jamais directement aux questions
- Fait des jeux de mots et des exagérations
- Se prend pour un philosophe du dimanche
- Utilise des interjections : "waouh", "yeahh", "oups"
- S'appuie vaguement sur le contexte NIRD mais le détourne complètement

## ⚙️ Configuration avancée

Toutes les variables d'environnement disponibles dans `.env` :

```bash
# Scraping
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_TOKENS=8000
OUTPUT_DIR=data
OUTPUT_FILE=scraped_data.json

# Recherche sémantique
HISTORY_FILE=data/historique_recherches.json
MIN_SIMILARITY_SCORE=0.12
SEARCH_TOP_K=1

# Chatbot Groq
GROQ_API_KEY=your-key-here
GROQ_MODEL=llama-3.3-70b-versatile
CHATBOT_TEMPERATURE=1.5
CHATBOT_MAX_TOKENS=200
```

## 🧪 Tests

```powershell
# Tester les imports
py test_import.py

# Lancer les tests unitaires
pytest
```

## 📝 Branches

- `claude/nird-chatbot-final-01V964kxTWdi92DQMbdbXyQz` - **Version finale complète** (3 modules)
- `claude/module1-stable-01V964kxTWdi92DQMbdbXyQz` - Version stable Module 1 uniquement
- `claude/french-greeting-01V964kxTWdi92DQMbdbXyQz` - Branche de développement

## 🎓 Valeurs NIRD

Ce projet promeut :
- **Inclusif** : Accès au numérique pour tous via des solutions libres
- **Responsable** : Sensibilisation à l'impact écologique du numérique
- **Durable** : Reconditionnement d'appareils, lutte contre l'obsolescence programmée

Outils mis en avant : Linux, PrimTux, Tchap, Forge, logiciels libres.

## 🏆 Nuit de l'Info 2025

Projet réalisé pour la Nuit de l'Info 2025, combinant :
- Défi principal : **NIRD** (Numérique Inclusif, Responsable et Durable)
- Défi annexe : **Chat'bruti** (chatbot humoristique)

## 📄 Licence

Projet éducatif - Nuit de l'Info 2025

## 🙏 Remerciements

- Site NIRD : https://nird.forge.apps.education.fr/
- Groq : Pour l'API LLM gratuite
- Équipe Nuit de l'Info 2025

---

**Fait avec ❤️ (et beaucoup de café) pour la Nuit de l'Info 2025** ☕🌙
