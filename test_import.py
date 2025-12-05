"""Test rapide des imports pour identifier les problèmes"""

print("Test 1: Import de FastAPI...")
from fastapi import FastAPI
print("✅ FastAPI OK")

print("\nTest 2: Import de config...")
from app.config import settings
print(f"✅ Config OK - GROQ_API_KEY: {'configurée' if settings.GROQ_API_KEY else 'NON configurée'}")

print("\nTest 3: Import des modules scraper...")
from app.modules.scraper import WebScraper, TextChunker, JSONExporter
print("✅ Scraper OK")

print("\nTest 4: Import semantic_routes...")
from app.routes import semantic_routes
print("✅ semantic_routes OK")

print("\nTest 5: Import chatbot_routes...")
from app.routes import chatbot_routes
print("✅ chatbot_routes OK")

print("\nTest 6: Import de l'app principale...")
from app.main import app
print("✅ main.py OK")

print("\n✅ TOUS LES IMPORTS FONCTIONNENT !")
print("\nSi ce script fonctionne mais pas l'API, le problème vient d'ailleurs.")
