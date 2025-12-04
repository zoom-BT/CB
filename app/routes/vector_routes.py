"""Routes API pour le module d'indexation vectorielle (Module 2)"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.config import settings
from app.modules.vector import VectorIndexer
from app.modules.scraper import JSONExporter

logger = logging.getLogger(__name__)

# Créer le router
router = APIRouter(prefix="/vector", tags=["Vector Indexing"])

# Instance globale de l'indexeur (sera initialisée au démarrage)
vector_indexer: Optional[VectorIndexer] = None


# Modèles Pydantic
class IndexRequest(BaseModel):
    """Requête d'indexation"""

    data_file: str = "scraped_data.json"
    namespace: str = ""
    batch_size: int = 32


class IndexResponse(BaseModel):
    """Réponse d'indexation"""

    success: bool
    message: str
    indexed_count: int
    index_name: str


class SearchRequest(BaseModel):
    """Requête de recherche"""

    query: str
    top_k: int = 5
    namespace: str = ""


class SearchResult(BaseModel):
    """Résultat de recherche"""

    id: str
    score: float
    text: str
    source_url: str
    source_title: str
    chunk_id: int


class SearchResponse(BaseModel):
    """Réponse de recherche"""

    query: str
    results: List[SearchResult]
    count: int


def get_vector_indexer() -> VectorIndexer:
    """Récupère ou initialise l'indexeur vectoriel"""
    global vector_indexer

    if vector_indexer is None:
        if not settings.PINECONE_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="PINECONE_API_KEY non configurée. Ajoutez-la dans le fichier .env",
            )

        logger.info("Initialisation du VectorIndexer...")
        vector_indexer = VectorIndexer(
            pinecone_api_key=settings.PINECONE_API_KEY,
            index_name=settings.PINECONE_INDEX_NAME,
            embedding_model=settings.EMBEDDING_MODEL,
            embedding_dimension=settings.EMBEDDING_DIMENSION,
        )

    return vector_indexer


@router.get("/")
async def vector_root():
    """Info sur le module vectoriel"""
    return {
        "module": "vector_indexing",
        "status": "ready",
        "embedding_model": settings.EMBEDDING_MODEL,
        "embedding_dimension": settings.EMBEDDING_DIMENSION,
        "index_name": settings.PINECONE_INDEX_NAME,
    }


@router.post("/index", response_model=IndexResponse)
async def index_data(request: IndexRequest):
    """
    Indexe les données scrapées dans Pinecone

    Charge le fichier JSON des chunks et les indexe dans Pinecone
    après génération des embeddings.
    """
    try:
        # Charger les données
        exporter = JSONExporter(output_dir=settings.OUTPUT_DIR)
        data = exporter.load(request.data_file)
        chunks = data.get("chunks", [])

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail=f"Aucun chunk trouvé dans {request.data_file}",
            )

        logger.info(f"Chargé {len(chunks)} chunks depuis {request.data_file}")

        # Initialiser l'indexeur
        indexer = get_vector_indexer()

        # Indexer les chunks
        result = indexer.index_chunks(
            chunks=chunks,
            namespace=request.namespace,
            batch_size=request.batch_size,
        )

        return IndexResponse(
            success=True,
            message=f"Indexation terminée: {result['upserted_count']} chunks",
            indexed_count=result["upserted_count"],
            index_name=result["index_name"],
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Fichier {request.data_file} introuvable. Lancez d'abord un scraping.",
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'indexation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_similar(request: SearchRequest):
    """
    Recherche les chunks les plus similaires à une requête

    Génère l'embedding de la requête et recherche les chunks
    les plus similaires dans Pinecone.
    """
    try:
        if not request.query:
            raise HTTPException(
                status_code=400,
                detail="La requête ne peut pas être vide",
            )

        # Initialiser l'indexeur
        indexer = get_vector_indexer()

        # Rechercher
        results = indexer.search(
            query=request.query,
            top_k=request.top_k,
            namespace=request.namespace,
        )

        # Formater les résultats
        formatted_results = []
        for result in results:
            metadata = result.get("metadata", {})
            formatted_results.append(
                SearchResult(
                    id=result.get("id", ""),
                    score=result.get("score", 0.0),
                    text=metadata.get("text", ""),
                    source_url=metadata.get("source_url", ""),
                    source_title=metadata.get("source_title", ""),
                    chunk_id=metadata.get("chunk_id", 0),
                )
            )

        return SearchResponse(
            query=request.query,
            results=formatted_results,
            count=len(formatted_results),
        )

    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_index_stats():
    """Récupère les statistiques de l'index Pinecone"""
    try:
        indexer = get_vector_indexer()
        stats = indexer.get_stats()

        return {
            "success": True,
            "stats": stats,
        }

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_index(namespace: str = ""):
    """
    Supprime tous les vecteurs de l'index (ATTENTION: destructif!)

    Utilisez avec précaution. Supprime toutes les données indexées.
    """
    try:
        indexer = get_vector_indexer()
        indexer.clear_index(namespace=namespace)

        return {
            "success": True,
            "message": f"Index vidé (namespace: {namespace or 'default'})",
        }

    except Exception as e:
        logger.error(f"Erreur lors du vidage de l'index: {e}")
        raise HTTPException(status_code=500, detail=str(e))
