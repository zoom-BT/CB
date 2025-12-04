"""Tests d'intégration pour l'API FastAPI"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Tests pour les endpoints de l'API"""

    def test_root_endpoint(self):
        """Test de l'endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint(self):
        """Test de l'endpoint de santé"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["module"] == "scraper"

    @patch("app.main.scraper.scrape_multiple_urls")
    @patch("app.main.chunker.chunk_documents")
    @patch("app.main.exporter.export")
    def test_scrape_endpoint(
        self, mock_export, mock_chunk, mock_scrape
    ):
        """Test de l'endpoint de scraping"""
        # Mock des réponses
        mock_scrape.return_value = [
            {
                "url": "https://example.com",
                "title": "Test",
                "content": "Test content for NIRD",
            }
        ]

        mock_chunk.return_value = [
            {
                "chunk_id": 0,
                "text": "Test content for NIRD",
                "token_count": 10,
                "source_url": "https://example.com",
            }
        ]

        mock_export.return_value = "data/scraped_data.json"

        # Requête de scraping
        response = client.post(
            "/scrape",
            json={"urls": ["https://example.com"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total_documents"] == 1
        assert data["total_chunks"] == 1
        assert "output_file" in data

    def test_scrape_endpoint_invalid_url(self):
        """Test du scraping avec une URL invalide"""
        response = client.post(
            "/scrape",
            json={"urls": ["not-a-valid-url"]},
        )

        assert response.status_code == 422  # Validation error

    @patch("app.main.exporter.load")
    def test_get_data_endpoint(self, mock_load):
        """Test de l'endpoint de récupération des données"""
        mock_load.return_value = {
            "metadata": {"total_chunks": 1},
            "chunks": [{"chunk_id": 0, "text": "Test"}],
        }

        response = client.get("/data")
        assert response.status_code == 200
        data = response.json()
        assert "chunks" in data

    @patch("app.main.exporter.load")
    def test_get_data_stats_endpoint(self, mock_load):
        """Test de l'endpoint des statistiques"""
        mock_load.return_value = {
            "metadata": {"export_date": "2025-12-04T00:00:00"},
            "chunks": [
                {
                    "chunk_id": 0,
                    "text": "Test content",
                    "length": 12,
                    "token_count": 5,
                    "source_url": "https://example.com",
                }
            ],
        }

        response = client.get("/data/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_chunks"] == 1
        assert data["total_tokens"] == 5
        assert data["unique_sources"] == 1

    def test_get_data_not_found(self):
        """Test de récupération sans données disponibles"""
        response = client.get("/data/stats")
        # Devrait retourner 404 si pas de données
        assert response.status_code in [404, 500]
