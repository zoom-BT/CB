"""Module d'indexation combinant embeddings et Pinecone"""

from typing import List, Dict, Any, Optional
import logging

from .embedder import EmbeddingGenerator
from .pinecone_client import PineconeVectorStore

logger = logging.getLogger(__name__)


class VectorIndexer:
    """Classe orchestrant l'indexation vectorielle complète"""

    def __init__(
        self,
        pinecone_api_key: str,
        index_name: str = "nird-chatbot",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        embedding_dimension: int = 384,
    ):
        """
        Initialise l'indexeur vectoriel

        Args:
            pinecone_api_key: Clé API Pinecone
            index_name: Nom de l'index Pinecone
            embedding_model: Modèle sentence-transformers
            embedding_dimension: Dimension des embeddings
        """
        logger.info("Initialisation du VectorIndexer...")

        # Initialiser le générateur d'embeddings
        self.embedder = EmbeddingGenerator(model_name=embedding_model)

        # Vérifier que la dimension correspond
        actual_dim = self.embedder.get_embedding_dimension()
        if actual_dim != embedding_dimension:
            logger.warning(
                f"Dimension du modèle ({actual_dim}) != dimension attendue ({embedding_dimension})"
            )
            embedding_dimension = actual_dim

        # Initialiser le client Pinecone
        self.vector_store = PineconeVectorStore(
            api_key=pinecone_api_key,
            index_name=index_name,
            dimension=embedding_dimension,
        )

        logger.info("✅ VectorIndexer initialisé")

    def index_chunks(
        self,
        chunks: List[Dict[str, Any]],
        namespace: str = "",
        batch_size: int = 32,
    ) -> Dict[str, Any]:
        """
        Indexe des chunks dans Pinecone

        Args:
            chunks: Liste de chunks à indexer
            namespace: Namespace Pinecone
            batch_size: Taille des batches pour l'embedding

        Returns:
            Statistiques d'indexation
        """
        if not chunks:
            logger.warning("Aucun chunk à indexer")
            return {"indexed_count": 0}

        logger.info(f"Indexation de {len(chunks)} chunks...")

        # Extraire les textes
        texts = [chunk.get("text", "") for chunk in chunks]

        # Générer les embeddings
        logger.info("Génération des embeddings...")
        embeddings = self.embedder.generate_embeddings(
            texts, batch_size=batch_size, show_progress=True
        )

        # Insérer dans Pinecone
        logger.info("Insertion dans Pinecone...")
        result = self.vector_store.upsert_chunks(
            chunks=chunks, embeddings=embeddings, namespace=namespace
        )

        logger.info(f"✅ Indexation terminée: {result['upserted_count']} chunks")

        return result

    def search(
        self,
        query: str,
        top_k: int = 5,
        namespace: str = "",
        filter: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """
        Recherche des chunks similaires à une requête

        Args:
            query: Texte de la requête
            top_k: Nombre de résultats à retourner
            namespace: Namespace Pinecone
            filter: Filtres sur les métadonnées

        Returns:
            Liste de chunks similaires avec scores
        """
        if not query:
            logger.warning("Requête vide")
            return []

        logger.info(f"Recherche pour: '{query[:100]}...'")

        # Générer l'embedding de la requête
        query_embedding = self.embedder.generate_embedding(query)

        # Rechercher dans Pinecone
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            namespace=namespace,
            filter=filter,
        )

        logger.info(f"✅ Trouvé {len(results)} résultats")

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de l'index"""
        return self.vector_store.get_index_stats()

    def clear_index(self, namespace: str = ""):
        """Vide l'index (attention: opération destructive!)"""
        logger.warning("⚠️ Suppression de tous les vecteurs!")
        self.vector_store.delete_all(namespace=namespace)
