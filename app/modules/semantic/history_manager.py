"""Gestionnaire d'historique des recherches"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class HistoryManager:
    """Gestionnaire pour sauvegarder l'historique des recherches"""

    def __init__(self, history_file: str = "data/historique_recherches.json"):
        """
        Initialise le gestionnaire d'historique

        Args:
            history_file: Chemin du fichier d'historique
        """
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(exist_ok=True)

        # Initialiser le fichier s'il n'existe pas
        if not self.history_file.exists():
            self._init_history_file()

    def _init_history_file(self):
        """Crée le fichier d'historique avec une structure initiale"""
        initial_data = {
            "metadata": {
                "api_name": "NIRD Semantic Search",
                "lancement": datetime.now().isoformat(),
                "total_recherches": 0
            },
            "recherches": []
        }

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Fichier d'historique créé: {self.history_file}")

    def save_search(self, search_data: Dict) -> None:
        """
        Sauvegarde une recherche dans l'historique

        Args:
            search_data: Données de la recherche à sauvegarder
        """
        try:
            with open(self.history_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)

                # Ajouter la recherche
                data["recherches"].append(search_data)
                data["metadata"]["total_recherches"] += 1
                data["metadata"]["derniere_mise_a_jour"] = datetime.now().isoformat()

                # Réécrire le fichier
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.truncate()

        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")

    def get_history(self, limit: Optional[int] = None) -> Dict:
        """
        Récupère l'historique des recherches

        Args:
            limit: Nombre maximum de recherches à retourner

        Returns:
            Dictionnaire avec métadonnées et recherches
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if limit:
                data["recherches"] = data["recherches"][-limit:]

            return data

        except Exception as e:
            logger.error(f"Erreur lors de la lecture: {e}")
            return {"metadata": {}, "recherches": []}

    def get_stats(self) -> Dict:
        """Récupère les statistiques de l'historique"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "total_recherches": data["metadata"].get("total_recherches", 0),
                "lancement": data["metadata"].get("lancement", ""),
                "derniere_mise_a_jour": data["metadata"].get("derniere_mise_a_jour", ""),
                "fichier": str(self.history_file)
            }

        except Exception as e:
            logger.error(f"Erreur lors de la lecture des stats: {e}")
            return {}

    def clear_history(self) -> None:
        """Vide l'historique (réinitialise le fichier)"""
        logger.warning("⚠️ Réinitialisation de l'historique")
        self._init_history_file()
