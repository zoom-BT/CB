"""API FastAPI pour le chatbot NIRD"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import logging

from app.config import settings
from app.modules.scraper import WebScraper, TextChunker, JSONExporter
from app.routes import semantic_routes, chatbot_routes

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)

# Initialisation des modules (Module 1 uniquement au démarrage)
scraper = None
chunker = None
exporter = None


def get_scraper():
    """Initialise le scraper à la demande"""
    global scraper
    if scraper is None:
        scraper = WebScraper()
    return scraper


def get_chunker():
    """Initialise le chunker à la demande"""
    global chunker
    if chunker is None:
        chunker = TextChunker(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
    return chunker


def get_exporter():
    """Initialise l'exporter à la demande"""
    global exporter
    if exporter is None:
        exporter = JSONExporter(output_dir=settings.OUTPUT_DIR)
    return exporter


# Inclure les routes Module 2 (recherche sémantique)
app.include_router(semantic_routes.router)

# Inclure les routes Module 3 (chatbot Chat-Bruti)
app.include_router(chatbot_routes.router)


# Modèles Pydantic
class ScrapeRequest(BaseModel):
    """Requête de scraping"""

    urls: List[HttpUrl]
    chunk_size: Optional[int] = settings.CHUNK_SIZE
    chunk_overlap: Optional[int] = settings.CHUNK_OVERLAP


class ScrapeResponse(BaseModel):
    """Réponse de scraping"""

    success: bool
    message: str
    total_documents: int
    total_chunks: int
    total_tokens: int
    output_file: str


# Routes
@app.get("/")
async def root():
    """Route racine"""
    return {
        "message": "Bienvenue sur l'API NIRD Chatbot",
        "version": settings.API_VERSION,
        "description": "API complète pour la Nuit de l'Info 2025",
        "modules": {
            "module_1": "Scraping web et découpage en chunks",
            "module_2": "Recherche sémantique (TF-IDF + similarité cosinus)",
            "module_3": "Chatbot Chat-Bruti avec Groq API"
        },
        "endpoints": {
            "scraping": "/scrape, /data, /data/stats",
            "semantic": "/semantic/search, /semantic/stats, /semantic/history",
            "chatbot": "/chatbot/ask, /chatbot/chat, /chatbot/"
        }
    }


@app.get("/health")
async def health():
    """Vérification de l'état de l'API"""
    return {"status": "healthy", "module": "scraper"}


@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_urls(request: ScrapeRequest):
    """
    Scrape une liste d'URLs, découpe le contenu en chunks et exporte en JSON

    Args:
        request: Liste d'URLs à scraper avec paramètres optionnels

    Returns:
        Informations sur le scraping effectué
    """
    try:
        # Convertir les URLs Pydantic en strings
        urls = [str(url) for url in request.urls]

        logger.info(f"Début du scraping de {len(urls)} URLs")

        # Scraper les URLs
        documents = get_scraper().scrape_multiple_urls(urls)

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="Aucun document n'a pu être scrapé",
            )

        # Configurer le chunker si nécessaire
        if (
            request.chunk_size != settings.CHUNK_SIZE
            or request.chunk_overlap != settings.CHUNK_OVERLAP
        ):
            custom_chunker = TextChunker(
                chunk_size=request.chunk_size,
                chunk_overlap=request.chunk_overlap,
            )
        else:
            custom_chunker = get_chunker()

        # Découper en chunks
        chunks = custom_chunker.chunk_documents(documents)

        # Calculer le total de tokens
        total_tokens = sum(chunk.get("token_count", 0) for chunk in chunks)

        # Exporter en JSON
        output_file = get_exporter().export(chunks, settings.OUTPUT_FILE)

        logger.info(
            f"Scraping terminé: {len(documents)} docs, "
            f"{len(chunks)} chunks, {total_tokens} tokens"
        )

        return ScrapeResponse(
            success=True,
            message="Scraping terminé avec succès",
            total_documents=len(documents),
            total_chunks=len(chunks),
            total_tokens=total_tokens,
            output_file=output_file,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data")
async def get_scraped_data():
    """
    Récupère les données scrapées depuis le fichier JSON

    Returns:
        Données scrapées avec métadonnées
    """
    try:
        data = get_exporter().load(settings.OUTPUT_FILE)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée scrapée trouvée. Lancez d'abord un scraping.",
        )
    except Exception as e:
        logger.error(f"Erreur lors de la lecture des données: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/stats")
async def get_data_stats():
    """
    Récupère les statistiques des données scrapées

    Returns:
        Statistiques sur les données
    """
    try:
        data = get_exporter().load(settings.OUTPUT_FILE)
        chunks = data.get("chunks", [])

        # Calculer les statistiques
        total_chunks = len(chunks)
        total_tokens = sum(chunk.get("token_count", 0) for chunk in chunks)
        total_chars = sum(len(chunk.get("text", "")) for chunk in chunks)

        # Compter les sources uniques
        unique_sources = len(
            set(chunk.get("source_url", "") for chunk in chunks)
        )

        return {
            "total_chunks": total_chunks,
            "total_tokens": total_tokens,
            "total_characters": total_chars,
            "unique_sources": unique_sources,
            "export_date": data.get("metadata", {}).get("export_date"),
            "average_chunk_size": (
                total_chars // total_chunks if total_chunks > 0 else 0
            ),
            "average_tokens_per_chunk": (
                total_tokens // total_chunks if total_chunks > 0 else 0
            ),
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée scrapée trouvée.",
        )
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
