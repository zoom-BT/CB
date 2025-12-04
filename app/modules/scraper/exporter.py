"""Module d'export des données au format JSON"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JSONExporter:
    """Classe pour exporter les données en JSON"""

    def __init__(self, output_dir: str = "data"):
        """
        Initialise l'exporter

        Args:
            output_dir: Répertoire de sortie
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export(
        self,
        data: List[Dict],
        filename: str = "scraped_data.json",
        include_metadata: bool = True,
    ) -> str:
        """
        Exporte les données au format JSON

        Args:
            data: Données à exporter
            filename: Nom du fichier de sortie
            include_metadata: Inclure les métadonnées d'export

        Returns:
            Chemin du fichier créé
        """
        output_path = self.output_dir / filename

        export_data = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "total_chunks": len(data),
                "total_tokens": sum(
                    chunk.get("token_count", 0) for chunk in data
                ),
            }
            if include_metadata
            else {},
            "chunks": data,
        }

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Données exportées vers {output_path}")
            logger.info(
                f"Total: {len(data)} chunks, "
                f"{export_data['metadata'].get('total_tokens', 0)} tokens"
            )

            return str(output_path)

        except Exception as e:
            logger.error(f"Erreur lors de l'export: {e}")
            raise

    def load(self, filename: str = "scraped_data.json") -> Dict:
        """
        Charge un fichier JSON exporté

        Args:
            filename: Nom du fichier à charger

        Returns:
            Données chargées
        """
        input_path = self.output_dir / filename

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            logger.info(f"Données chargées depuis {input_path}")
            return data

        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}")
            raise
