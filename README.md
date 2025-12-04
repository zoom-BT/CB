# NIRD Chatbot API - Module de Scraping

> Projet pour la Nuit de l'Info 2025 - Défi NIRD + Chat'bruti

API FastAPI pour scraper, chunker et indexer des contenus web pour alimenter un chatbot sur le projet NIRD (Numérique Inclusif, Responsable et Durable).

## 🎯 Objectif

Ce module permet de :
- Scraper des pages web (individuelles ou via sitemap)
- Découper le contenu en chunks intelligents
- Tokenizer le texte pour une utilisation avec des LLM
- Exporter les données au format JSON pour l'indexation vectorielle

## 🏗️ Architecture

```
app/
├── main.py                    # API FastAPI
├── config.py                  # Configuration
└── modules/
    └── scraper/
        ├── scraper.py         # Web scraping
        ├── chunker.py         # Chunking et tokenization
        └── exporter.py        # Export JSON
```

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip

### Étapes

1. Cloner le dépôt :
```bash
git clone <votre-repo>
cd CB
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Créer un fichier `.env` (optionnel) :
```bash
cp .env.example .env
```

## 📦 Utilisation

### Lancer l'API

```bash
python -m uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

### Endpoints disponibles

#### `GET /`
Point d'entrée principal avec informations sur l'API

#### `GET /health`
Vérification de l'état de santé de l'API

#### `POST /scrape`
Lance un scraping d'URLs

**Body :**
```json
{
  "urls": [
    "https://nird.forge.apps.education.fr/",
    "https://example.com/page2"
  ],
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Scraping terminé avec succès",
  "total_documents": 2,
  "total_chunks": 15,
  "total_tokens": 3500,
  "output_file": "data/scraped_data.json"
}
```

#### `GET /data`
Récupère toutes les données scrapées

#### `GET /data/stats`
Récupère les statistiques sur les données scrapées

## 🧪 Tests

Lancer tous les tests :
```bash
pytest
```

Avec couverture :
```bash
pytest --cov=app tests/
```

Tests spécifiques :
```bash
pytest tests/test_scraper.py -v
pytest tests/test_api.py -v
```

## ⚙️ Configuration

Variables d'environnement disponibles (dans `.env`) :

```env
# Chunking
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_TOKENS=8000

# Output
OUTPUT_DIR=data
OUTPUT_FILE=scraped_data.json

# API
API_TITLE=NIRD Chatbot API
API_VERSION=1.0.0
```

## 📊 Format de données exportées

```json
{
  "metadata": {
    "export_date": "2025-12-04T12:00:00",
    "total_chunks": 15,
    "total_tokens": 3500
  },
  "chunks": [
    {
      "chunk_id": 0,
      "text": "Le projet NIRD vise à promouvoir...",
      "length": 485,
      "token_count": 120,
      "tokens": [1234, 5678, ...],
      "source_url": "https://nird.forge.apps.education.fr/",
      "source_title": "NIRD - Accueil"
    }
  ]
}
```

## 🔧 Prochaines étapes

Ce module fait partie d'une architecture en 3 parties :

1. ✅ **Module de scraping** (actuel)
2. ⏳ **Module d'indexation vectorielle** (à venir)
3. ⏳ **Module d'interfaçage IA** (à venir)

## 🎭 Défi Chat'bruti

Ce module servira de base de connaissances pour un chatbot absurde et décalé qui répondra aux questions sur NIRD de manière... créative !

## 👥 Équipe

[Votre nom d'équipe] - Nuit de l'Info 2025

## 📝 Licence

Projet sous licence libre (à préciser selon les règles de la Nuit de l'Info)

## 🔗 Liens utiles

- [Site NIRD](https://nird.forge.apps.education.fr/)
- [Défi Chat'bruti](https://www.nuitdelinfo.com/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
