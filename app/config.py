"""Configuration de l'application"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Paramètres de configuration de l'application"""

    # Scraping settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_TOKENS: int = 8000

    # Output settings
    OUTPUT_DIR: str = "data"
    OUTPUT_FILE: str = "scraped_data.json"

    # API settings
    API_TITLE: str = "NIRD Chatbot API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API pour le chatbot NIRD - Nuit de l'Info 2025"

    # Vector indexing settings (Module 2)
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_INDEX_NAME: str = "nird-chatbot"
    PINECONE_ENVIRONMENT: str = "us-east-1"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_DIMENSION: int = 384
    SEARCH_TOP_K: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
