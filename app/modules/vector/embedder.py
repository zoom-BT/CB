"""Génération d'embeddings avec Sentence Transformers"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Classe pour générer des embeddings à partir de texte"""

    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        device: str = None,
    ):
        """
        Initialise le générateur d'embeddings

        Args:
            model_name: Nom du modèle sentence-transformers
                       Par défaut: modèle multilingue (FR/EN) rapide et léger
            device: Device à utiliser ('cpu', 'cuda', 'mps'). None = auto-détection
        """
        logger.info(f"Chargement du modèle d'embeddings: {model_name}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(
            f"Modèle chargé. Dimension des embeddings: {self.embedding_dim}"
        )

    def generate_embedding(self, text: str) -> List[float]:
        """
        Génère un embedding pour un texte unique

        Args:
            text: Le texte à encoder

        Returns:
            Vecteur d'embedding (liste de float)
        """
        if not text:
            return [0.0] * self.embedding_dim

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,  # Normaliser pour calcul cosinus
        )
        return embedding.tolist()

    def generate_embeddings(
        self, texts: List[str], batch_size: int = 32, show_progress: bool = False
    ) -> List[List[float]]:
        """
        Génère des embeddings pour plusieurs textes (batch)

        Args:
            texts: Liste de textes à encoder
            batch_size: Taille des batches pour le traitement
            show_progress: Afficher une barre de progression

        Returns:
            Liste de vecteurs d'embeddings
        """
        if not texts:
            return []

        logger.info(f"Génération de {len(texts)} embeddings...")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=show_progress,
        )

        logger.info(f"Embeddings générés: {embeddings.shape}")
        return embeddings.tolist()

    def compute_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """
        Calcule la similarité cosinus entre deux embeddings

        Args:
            embedding1: Premier embedding
            embedding2: Second embedding

        Returns:
            Score de similarité (0-1, 1 = très similaire)
        """
        # Les embeddings sont déjà normalisés, donc similarité = produit scalaire
        return float(np.dot(embedding1, embedding2))

    def get_embedding_dimension(self) -> int:
        """Retourne la dimension des embeddings"""
        return self.embedding_dim
