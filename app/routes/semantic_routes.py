"""Routes API pour le module de recherche sémantique (Module 2)"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import logging

from app.config import settings
from app.modules.scraper import JSONExporter
from app.modules.semantic import SemanticSearchEngine, HistoryManager

logger = logging.getLogger(__name__)

# Créer le router
router = APIRouter(prefix="/semantic", tags=["Semantic Search"])

# Instances globales
search_engine: Optional[SemanticSearchEngine] = None
history_manager: Optional[HistoryManager] = None


# Modèles Pydantic
class SearchRequest(BaseModel):
    """Requête de recherche sémantique"""
    question: str


class SearchResult(BaseModel):
    """Résultat de recherche"""
    chunk_id: int
    text: str
    source_url: str
    source_title: str
    score: float


class SearchResponse(BaseModel):
    """Réponse de recherche"""
    question: str
    contexte: str
    confiance: float
    chunk_id: int
    source_url: str
    source_title: str
    timestamp: str


def get_search_engine() -> SemanticSearchEngine:
    """Récupère ou initialise le moteur de recherche"""
    global search_engine

    if search_engine is None:
        logger.info("Initialisation du moteur de recherche sémantique...")
        search_engine = SemanticSearchEngine()

        # Charger les chunks depuis le fichier JSON
        try:
            exporter = JSONExporter(output_dir=settings.OUTPUT_DIR)
            data = exporter.load(settings.OUTPUT_FILE)
            chunks = data.get("chunks", [])

            if chunks:
                search_engine.index_chunks(chunks)
                logger.info(f"✅ {len(chunks)} chunks indexés")
            else:
                logger.warning("Aucun chunk trouvé dans le fichier JSON")

        except FileNotFoundError:
            logger.warning(
                f"Fichier {settings.OUTPUT_FILE} introuvable. "
                "Lancez d'abord un scraping (POST /scrape)"
            )

    return search_engine


def get_history_manager() -> HistoryManager:
    """Récupère ou initialise le gestionnaire d'historique"""
    global history_manager

    if history_manager is None:
        history_manager = HistoryManager(history_file=settings.HISTORY_FILE)

    return history_manager


@router.get("/")
async def semantic_root():
    """Info sur le module sémantique"""
    return {
        "module": "semantic_search",
        "description": "Recherche sémantique avec TF-IDF et similarité cosinus",
        "status": "ready",
        "method": "TF-IDF + Cosine Similarity",
        "no_external_deps": True
    }


@router.post("/search", response_model=SearchResponse)
async def search_nird(request: SearchRequest):
    """
    Recherche le meilleur contexte pour une question

    Utilise la similarité cosinus pour trouver le chunk le plus pertinent
    et sauvegarde la recherche dans l'historique.
    """
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question vide")

        # Récupérer le moteur de recherche
        engine = get_search_engine()

        if not engine.indexed:
            raise HTTPException(
                status_code=503,
                detail="Index non initialisé. Lancez d'abord un scraping (POST /scrape)"
            )

        # Rechercher le meilleur contexte
        contexte, confiance, metadata = engine.get_best_context(question)

        # Créer la réponse
        response = SearchResponse(
            question=question,
            contexte=contexte,
            confiance=confiance,
            chunk_id=metadata["chunk_id"],
            source_url=metadata["source_url"],
            source_title=metadata["source_title"],
            timestamp=datetime.now().isoformat()
        )

        # Sauvegarder dans l'historique
        history = get_history_manager()
        history.save_search(response.dict())

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Récupère les statistiques du moteur de recherche"""
    try:
        engine = get_search_engine()
        return {
            "success": True,
            "search_engine": engine.get_stats(),
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history(limit: Optional[int] = None):
    """Récupère l'historique des recherches"""
    try:
        history = get_history_manager()
        return history.get_history(limit=limit)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/stats")
async def get_history_stats():
    """Récupère les statistiques de l'historique"""
    try:
        history = get_history_manager()
        return history.get_stats()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/clear")
async def clear_history():
    """Vide l'historique des recherches"""
    try:
        history = get_history_manager()
        history.clear_history()
        return {
            "success": True,
            "message": "Historique vidé"
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))
