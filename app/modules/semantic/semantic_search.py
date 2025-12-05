"""Moteur de recherche sémantique basé sur TF-IDF et similarité cosinus"""

import re
import math
from collections import Counter
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class SemanticSearchEngine:
    """Moteur de recherche sémantique simple sans dépendance externe"""

    def __init__(self):
        """Initialise le moteur de recherche"""
        self.chunks: List[Dict] = []
        self.vecteurs_chunks: List[Counter] = []
        self.indexed = False

        # Mots importants pour le boost de score
        self.mots_forts = [
            "linux", "reconditionnement", "nird", "primtux", "tchap",
            "écologique", "libre", "inclusif", "durable", "obsolescence",
            "forge", "numérique", "responsable", "carnot", "établissement"
        ]

        # Stopwords français
        self.stopwords = {
            "le", "la", "les", "de", "du", "des", "un", "une", "et", "ou",
            "à", "au", "aux", "en", "dans", "sur", "pour", "par", "avec",
            "sans", "sous", "chez", "ce", "cette", "ces", "son", "sa", "ses",
            "mon", "ma", "mes", "ton", "ta", "tes", "je", "tu", "il", "elle",
            "nous", "vous", "ils", "elles", "qui", "que", "quoi", "dont", "où",
            "quand", "comment", "mais", "est", "sont", "pas", "plus", "très"
        }

    def nettoyer_et_vectoriser(self, texte: str) -> Counter:
        """
        Nettoie et vectorise un texte en bag-of-words

        Args:
            texte: Le texte à vectoriser

        Returns:
            Counter avec les fréquences des mots
        """
        texte = texte.lower()
        mots = re.findall(r'\w+', texte)

        # Filtrer les stopwords et mots courts
        mots = [
            m for m in mots
            if m not in self.stopwords and len(m) > 2
        ]

        return Counter(mots)

    def cosine_similarity(self, vec1: Counter, vec2: Counter) -> float:
        """
        Calcule la similarité cosinus entre deux vecteurs

        Args:
            vec1: Premier vecteur
            vec2: Second vecteur

        Returns:
            Score de similarité (0-1)
        """
        communs = set(vec1) & set(vec2)
        if not communs:
            return 0.0

        numerateur = sum(vec1[w] * vec2[w] for w in communs)
        denominateur = (
            math.sqrt(sum(v * v for v in vec1.values())) *
            math.sqrt(sum(v * v for v in vec2.values()))
        )

        return numerateur / denominateur if denominateur != 0 else 0.0

    def index_chunks(self, chunks: List[Dict]) -> None:
        """
        Indexe les chunks pour la recherche

        Args:
            chunks: Liste de chunks à indexer
        """
        logger.info(f"Indexation de {len(chunks)} chunks...")
        self.chunks = chunks

        # Pré-calculer les vecteurs de tous les chunks
        self.vecteurs_chunks = [
            self.nettoyer_et_vectoriser(chunk["text"])
            for chunk in chunks
        ]

        self.indexed = True
        logger.info(f"✅ {len(chunks)} chunks indexés")

    def search(
        self,
        question: str,
        top_k: int = 1,
        min_score: float = 0.12
    ) -> List[Dict]:
        """
        Recherche les chunks les plus pertinents pour une question

        Args:
            question: La question de l'utilisateur
            top_k: Nombre de résultats à retourner
            min_score: Score minimum de confiance

        Returns:
            Liste de résultats avec scores
        """
        if not self.indexed:
            raise ValueError("Aucun chunk indexé. Appelez index_chunks() d'abord.")

        question = question.strip()
        if not question:
            return []

        # Vectoriser la question
        vec_question = self.nettoyer_et_vectoriser(question)

        # Calculer les scores pour tous les chunks
        resultats = []

        for i, vec_chunk in enumerate(self.vecteurs_chunks):
            score = self.cosine_similarity(vec_question, vec_chunk)

            # Boost si mots-clés importants présents
            for mot in self.mots_forts:
                if mot in question.lower() and mot in self.chunks[i]["text"].lower():
                    score += 0.18

            if score > min_score:
                chunk = self.chunks[i].copy()
                texte = chunk["text"].strip()

                # Limiter la longueur du contexte
                if len(texte) > 600:
                    texte = texte[:600].rsplit(' ', 1)[0] + "..."

                resultats.append({
                    "chunk_id": chunk.get("chunk_id", i),
                    "text": texte,
                    "source_url": chunk.get("source_url", ""),
                    "source_title": chunk.get("source_title", ""),
                    "token_count": chunk.get("token_count", 0),
                    "score": round(score, 3)
                })

        # Trier par score décroissant
        resultats.sort(key=lambda x: x["score"], reverse=True)

        # Retourner top_k résultats
        return resultats[:top_k]

    def get_best_context(
        self,
        question: str,
        fallback_context: Optional[str] = None
    ) -> Tuple[str, float, Dict]:
        """
        Récupère le meilleur contexte pour une question

        Args:
            question: La question de l'utilisateur
            fallback_context: Contexte par défaut si rien trouvé

        Returns:
            Tuple (contexte, score, metadata)
        """
        resultats = self.search(question, top_k=1, min_score=0.12)

        if resultats:
            meilleur = resultats[0]
            return (
                meilleur["text"],
                meilleur["score"],
                {
                    "chunk_id": meilleur["chunk_id"],
                    "source_url": meilleur["source_url"],
                    "source_title": meilleur["source_title"]
                }
            )
        else:
            # Contexte par défaut
            if fallback_context is None:
                fallback_context = (
                    "La démarche NIRD promeut un numérique Inclusif, Responsable et "
                    "Durable dans les établissements scolaires via Linux, le "
                    "reconditionnement et les logiciels libres."
                )

            return (
                fallback_context,
                0.0,
                {
                    "chunk_id": -1,
                    "source_url": "https://nird.forge.apps.education.fr/",
                    "source_title": "Accueil"
                }
            )

    def get_stats(self) -> Dict:
        """Retourne les statistiques de l'index"""
        return {
            "total_chunks": len(self.chunks),
            "total_vectors": len(self.vecteurs_chunks),
            "indexed": self.indexed,
            "mots_forts_count": len(self.mots_forts)
        }
