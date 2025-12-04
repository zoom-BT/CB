"""Module de scraping web pour extraire le contenu des pages"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Classe pour scraper le contenu de pages web"""

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Initialise le scraper

        Args:
            headers: En-têtes HTTP personnalisés pour les requêtes
        """
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (NIRD Chatbot Scraper)"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_url(self, url: str) -> Dict[str, str]:
        """
        Scrape une URL unique et extrait son contenu

        Args:
            url: L'URL à scraper

        Returns:
            Dictionnaire contenant l'URL, le titre et le contenu texte
        """
        try:
            logger.info(f"Scraping URL: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Supprimer les scripts et styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Extraire le titre
            title = soup.find("title")
            title_text = title.get_text(strip=True) if title else "Sans titre"

            # Extraire le contenu principal
            # Priorité : main, article, body
            main_content = (
                soup.find("main")
                or soup.find("article")
                or soup.find("body")
            )

            if main_content:
                text = main_content.get_text(separator=" ", strip=True)
            else:
                text = soup.get_text(separator=" ", strip=True)

            # Nettoyer le texte (espaces multiples, lignes vides)
            text = " ".join(text.split())

            return {
                "url": url,
                "title": title_text,
                "content": text,
                "length": len(text),
            }

        except requests.RequestException as e:
            logger.error(f"Erreur lors du scraping de {url}: {e}")
            return {
                "url": url,
                "title": "Erreur",
                "content": "",
                "length": 0,
                "error": str(e),
            }

    def scrape_multiple_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Scrape plusieurs URLs

        Args:
            urls: Liste des URLs à scraper

        Returns:
            Liste de dictionnaires contenant les données scrapées
        """
        results = []
        for url in urls:
            result = self.scrape_url(url)
            if result["content"]:
                results.append(result)

        logger.info(f"Scraping terminé: {len(results)}/{len(urls)} URLs réussies")
        return results

    def scrape_sitemap(self, sitemap_url: str) -> List[Dict[str, str]]:
        """
        Scrape toutes les URLs d'un sitemap XML

        Args:
            sitemap_url: URL du sitemap

        Returns:
            Liste de dictionnaires contenant les données scrapées
        """
        try:
            response = self.session.get(sitemap_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            urls = [loc.text for loc in soup.find_all("loc")]

            logger.info(f"Sitemap trouvé: {len(urls)} URLs")
            return self.scrape_multiple_urls(urls)

        except Exception as e:
            logger.error(f"Erreur lors du parsing du sitemap: {e}")
            return []
