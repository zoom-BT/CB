"""Tests unitaires pour le module de scraping"""

import pytest
from unittest.mock import Mock, patch
from app.modules.scraper import WebScraper, TextChunker, JSONExporter
import json
from pathlib import Path


class TestWebScraper:
    """Tests pour la classe WebScraper"""

    def test_scraper_initialization(self):
        """Test l'initialisation du scraper"""
        scraper = WebScraper()
        assert scraper.headers is not None
        assert "User-Agent" in scraper.headers

    @patch("app.modules.scraper.scraper.requests.Session.get")
    def test_scrape_url_success(self, mock_get):
        """Test le scraping d'une URL avec succès"""
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <head><title>Test Page</title></head>
            <body>
                <main>
                    <h1>Titre principal</h1>
                    <p>Contenu de test pour NIRD.</p>
                </main>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = WebScraper()
        result = scraper.scrape_url("https://example.com")

        assert result["url"] == "https://example.com"
        assert result["title"] == "Test Page"
        assert "Contenu de test" in result["content"]
        assert result["length"] > 0

    @patch("app.modules.scraper.scraper.requests.Session.get")
    def test_scrape_url_error(self, mock_get):
        """Test le scraping avec une erreur réseau"""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")

        scraper = WebScraper()
        result = scraper.scrape_url("https://example.com")

        assert result["url"] == "https://example.com"
        assert result["title"] == "Erreur"
        assert result["content"] == ""
        assert "error" in result

    @patch("app.modules.scraper.scraper.requests.Session.get")
    def test_scrape_multiple_urls(self, mock_get):
        """Test le scraping de plusieurs URLs"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body><p>Test content</p></body></html>"
        mock_get.return_value = mock_response

        scraper = WebScraper()
        urls = ["https://example.com/page1", "https://example.com/page2"]
        results = scraper.scrape_multiple_urls(urls)

        assert len(results) == 2
        assert all("content" in r for r in results)


class TestTextChunker:
    """Tests pour la classe TextChunker"""

    def test_chunker_initialization(self):
        """Test l'initialisation du chunker"""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        assert chunker.chunk_size == 100
        assert chunker.chunk_overlap == 20
        assert chunker.encoding is not None

    def test_count_tokens(self):
        """Test le comptage des tokens"""
        chunker = TextChunker()
        text = "Ceci est un test pour le chatbot NIRD."
        token_count = chunker.count_tokens(text)

        assert token_count > 0
        assert isinstance(token_count, int)

    def test_tokenize(self):
        """Test la tokenization"""
        chunker = TextChunker()
        text = "Test NIRD"
        tokens = chunker.tokenize(text)

        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(t, int) for t in tokens)

    def test_chunk_text(self):
        """Test le découpage d'un texte en chunks"""
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)
        text = (
            "Le projet NIRD vise à promouvoir un numérique libre et responsable. "
            "Les établissements scolaires peuvent réduire leur dépendance aux Big Tech. "
            "Le logiciel libre est une solution pour lutter contre l'obsolescence programmée."
        )

        chunks = chunker.chunk_text(text, metadata={"source": "test"})

        assert len(chunks) > 0
        assert all("text" in chunk for chunk in chunks)
        assert all("token_count" in chunk for chunk in chunks)
        assert all("tokens" in chunk for chunk in chunks)
        assert all(chunk["source"] == "test" for chunk in chunks)

    def test_chunk_documents(self):
        """Test le découpage de plusieurs documents"""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        documents = [
            {
                "url": "https://example.com/page1",
                "title": "Page 1",
                "content": "Contenu de la première page sur NIRD." * 10,
            },
            {
                "url": "https://example.com/page2",
                "title": "Page 2",
                "content": "Contenu de la seconde page sur NIRD." * 10,
            },
        ]

        chunks = chunker.chunk_documents(documents)

        assert len(chunks) > 0
        assert all("source_url" in chunk for chunk in chunks)
        assert all("source_title" in chunk for chunk in chunks)


class TestJSONExporter:
    """Tests pour la classe JSONExporter"""

    def test_exporter_initialization(self, tmp_path):
        """Test l'initialisation de l'exporter"""
        exporter = JSONExporter(output_dir=str(tmp_path))
        assert exporter.output_dir.exists()

    def test_export_and_load(self, tmp_path):
        """Test l'export et le chargement de données"""
        exporter = JSONExporter(output_dir=str(tmp_path))

        test_data = [
            {
                "chunk_id": 0,
                "text": "Test chunk NIRD",
                "token_count": 5,
                "source_url": "https://example.com",
            }
        ]

        # Export
        output_file = exporter.export(
            test_data, filename="test_export.json"
        )
        assert Path(output_file).exists()

        # Load
        loaded_data = exporter.load(filename="test_export.json")
        assert "metadata" in loaded_data
        assert "chunks" in loaded_data
        assert len(loaded_data["chunks"]) == 1
        assert loaded_data["chunks"][0]["text"] == "Test chunk NIRD"

    def test_export_with_metadata(self, tmp_path):
        """Test l'export avec métadonnées"""
        exporter = JSONExporter(output_dir=str(tmp_path))

        test_data = [
            {"chunk_id": 0, "text": "Chunk 1", "token_count": 10},
            {"chunk_id": 1, "text": "Chunk 2", "token_count": 15},
        ]

        output_file = exporter.export(
            test_data, filename="test_meta.json", include_metadata=True
        )

        with open(output_file, "r") as f:
            data = json.load(f)

        assert data["metadata"]["total_chunks"] == 2
        assert data["metadata"]["total_tokens"] == 25
        assert "export_date" in data["metadata"]

    def test_load_nonexistent_file(self, tmp_path):
        """Test le chargement d'un fichier inexistant"""
        exporter = JSONExporter(output_dir=str(tmp_path))

        with pytest.raises(Exception):
            exporter.load(filename="nonexistent.json")
