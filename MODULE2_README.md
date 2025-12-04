# Module 2 : Indexation Vectorielle avec Pinecone

> Module d'indexation et de recherche sémantique pour le chatbot NIRD

## 🎯 Objectif

Ce module permet de :
- Générer des **embeddings** (vecteurs sémantiques) à partir du texte scrapé
- Indexer les chunks dans **Pinecone** (base de données vectorielle cloud)
- Effectuer des **recherches par similarité** sémantique
- Préparer les données pour le chatbot (Module 3)

## 🏗️ Architecture

```
app/modules/vector/
├── embedder.py           # Génération d'embeddings (Sentence Transformers)
├── pinecone_client.py    # Client Pinecone pour indexation/recherche
└── indexer.py            # Orchestration complète

app/routes/
└── vector_routes.py      # Endpoints API pour le module vectoriel
```

## 📦 Technologies utilisées

- **Sentence Transformers** : Génération d'embeddings localement
  - Modèle : `paraphrase-multilingual-MiniLM-L12-v2` (FR/EN)
  - Dimension : 384
  - Rapide et léger (~120MB)

- **Pinecone** : Base de données vectorielle serverless
  - Recherche par similarité ultra-rapide
  - Scalable et managée
  - Free tier : 100K vecteurs gratuits

## 🚀 Configuration

### 1. Créer un compte Pinecone

1. Allez sur [https://www.pinecone.io/](https://www.pinecone.io/)
2. Créez un compte gratuit
3. Créez un projet
4. Récupérez votre **API Key** depuis le dashboard

### 2. Configurer les variables d'environnement

Copiez `.env.example` vers `.env` et remplissez :

```bash
PINECONE_API_KEY=votre-clé-api-pinecone
PINECONE_INDEX_NAME=nird-chatbot
PINECONE_ENVIRONMENT=us-east-1
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Note** : Le premier lancement téléchargera le modèle d'embeddings (~120MB)

## 📝 Utilisation

### Via l'API

#### 1. Indexer les données scrapées

```bash
POST /vector/index

{
  "data_file": "scraped_data.json",
  "namespace": "",
  "batch_size": 32
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Indexation terminée: 11 chunks",
  "indexed_count": 11,
  "index_name": "nird-chatbot"
}
```

#### 2. Rechercher des chunks similaires

```bash
POST /vector/search

{
  "query": "C'est quoi NIRD ?",
  "top_k": 3,
  "namespace": ""
}
```

**Réponse :**
```json
{
  "query": "C'est quoi NIRD ?",
  "count": 3,
  "results": [
    {
      "id": "https://nird.forge.apps.education.fr/#0",
      "score": 0.85,
      "text": "La démarche NIRD vise à promouvoir un numérique libre...",
      "source_url": "https://nird.forge.apps.education.fr/",
      "source_title": "Accueil",
      "chunk_id": 0
    },
    ...
  ]
}
```

#### 3. Statistiques de l'index

```bash
GET /vector/stats
```

**Réponse :**
```json
{
  "success": true,
  "stats": {
    "total_vector_count": 11,
    "dimension": 384,
    "index_fullness": 0.0001,
    "namespaces": {
      "": {
        "vector_count": 11
      }
    }
  }
}
```

#### 4. Vider l'index (⚠️ destructif)

```bash
DELETE /vector/clear?namespace=
```

### Via le code Python

```python
from app.modules.vector import VectorIndexer
from app.config import settings

# Initialiser l'indexeur
indexer = VectorIndexer(
    pinecone_api_key="votre-clé",
    index_name="nird-chatbot"
)

# Indexer des chunks
chunks = [...]  # Depuis le Module 1
result = indexer.index_chunks(chunks)

# Rechercher
results = indexer.search("C'est quoi NIRD ?", top_k=3)

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Texte: {result['metadata']['text'][:100]}...")
```

## 🧪 Tests

```bash
pytest tests/test_vector.py -v
```

## 📊 Workflow complet (Modules 1 + 2)

```
1. Scraping (Module 1)
   POST /scrape {"urls": ["https://nird.forge.apps.education.fr/"]}
   → Génère scraped_data.json avec 11 chunks

2. Indexation (Module 2)
   POST /vector/index {"data_file": "scraped_data.json"}
   → Génère embeddings et indexe dans Pinecone

3. Recherche (Module 2)
   POST /vector/search {"query": "NIRD c'est quoi ?"}
   → Retourne les 3-5 chunks les plus pertinents

4. Chatbot (Module 3 - à venir)
   → Utilise les chunks pertinents comme contexte pour Gemini
```

## 🔧 Paramètres de configuration

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Modèle sentence-transformers |
| `EMBEDDING_DIMENSION` | `384` | Dimension des vecteurs |
| `PINECONE_INDEX_NAME` | `nird-chatbot` | Nom de l'index Pinecone |
| `PINECONE_ENVIRONMENT` | `us-east-1` | Région Pinecone |
| `SEARCH_TOP_K` | `5` | Nombre de résultats par défaut |

## 💡 Comment ça marche ?

### 1. Génération d'embeddings

```
"La démarche NIRD vise à promouvoir..."
    ↓ Sentence Transformer
[0.234, -0.567, 0.891, ..., 0.123]  # Vecteur de 384 dimensions
```

### 2. Indexation dans Pinecone

```python
Pinecone.upsert([
    {
        "id": "url#chunk_id",
        "values": [0.234, -0.567, ...],
        "metadata": {
            "text": "...",
            "source_url": "...",
            "source_title": "..."
        }
    }
])
```

### 3. Recherche par similarité

```
"C'est quoi NIRD ?"
    ↓ Embedding
[0.245, -0.543, ...]
    ↓ Similarité cosinus avec tous les vecteurs
    ↓ Top 3 résultats
[Chunk 1 (0.85), Chunk 2 (0.78), Chunk 3 (0.72)]
```

## 🎯 Pourquoi des embeddings et pas juste du texte ?

**Recherche textuelle classique** (mots-clés) :
- "NIRD" trouve seulement les docs avec "NIRD"
- "numérique libre" ne trouve pas "logiciel libre"
- Pas de compréhension du sens

**Recherche sémantique** (embeddings) :
- "C'est quoi NIRD ?" trouve "La démarche NIRD..."
- "écologie numérique" trouve "numérique durable"
- Comprend les synonymes, paraphrases, concepts similaires

## 🔗 Prochaine étape : Module 3

Le Module 3 utilisera :
- Les chunks pertinents trouvés par le Module 2
- Une API d'IA (Gemini) pour générer des réponses
- Une personnalité absurde pour le défi Chat'bruti !

---

**Status :** ✅ Module 2 complet et fonctionnel
**Testé avec :** 11 chunks du site NIRD, recherches sémantiques opérationnelles
