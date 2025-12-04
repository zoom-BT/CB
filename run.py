"""Script de lancement cross-platform pour l'API NIRD"""

import sys
import subprocess
from pathlib import Path


def main():
    """Lance l'API FastAPI de manière cross-platform"""
    print("🚀 Démarrage de l'API NIRD Chatbot...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")

    try:
        # Vérifier que les dépendances sont installées
        try:
            import fastapi
            import uvicorn
        except ImportError:
            print("❌ Erreur: Dépendances manquantes!")
            print("Installez-les avec: pip install -r requirements.txt")
            sys.exit(1)

        # Lancer uvicorn
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\n✅ Serveur arrêté proprement")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
