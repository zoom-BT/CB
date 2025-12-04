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

    class Config:
        env_file = ".env"


settings = Settings()
