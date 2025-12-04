"""Client Pinecone pour l'indexation et la recherche vectorielle"""

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional, Any
import logging
import time

logger = logging.getLogger(__name__)


class PineconeVectorStore:
    """Classe pour gérer l'indexation et la recherche dans Pinecone"""

    def __init__(
        self,
        api_key: str,
        index_name: str = "nird-chatbot",
        dimension: int = 384,  # Dimension du modèle multilingual-MiniLM
        metric: str = "cosine",
        cloud: str = "aws",
        region: str = "us-east-1",
    ):
        """
        Initialise le client Pinecone

        Args:
            api_key: Clé API Pinecone
            index_name: Nom de l'index Pinecone
            dimension: Dimension des vecteurs d'embeddings
            metric: Métrique de similarité ('cosine', 'euclidean', 'dotproduct')
            cloud: Provider cloud ('aws', 'gcp', 'azure')
            region: Région du cloud
        """
        logger.info(f"Initialisation du client Pinecone pour l'index: {index_name}")

        self.api_key = api_key
        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric

        # Initialiser le client Pinecone
        self.pc = Pinecone(api_key=api_key)

        # Créer ou récupérer l'index
        self._ensure_index_exists(cloud, region)

        # Se connecter à l'index
        self.index = self.pc.Index(index_name)
        logger.info(f"Connecté à l'index Pinecone: {index_name}")

    def _ensure_index_exists(self, cloud: str, region: str):
        """Crée l'index s'il n'existe pas"""
        existing_indexes = [index.name for index in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            logger.info(f"Création de l'index: {self.index_name}")

            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                    cloud=cloud,
                    region=region
                )
            )

            # Attendre que l'index soit prêt
            logger.info("Attente de la création de l'index...")
            time.sleep(10)  # Pinecone prend quelques secondes

            logger.info(f"Index {self.index_name} créé avec succès")
        else:
            logger.info(f"Index {self.index_name} existe déjà")

    def upsert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
        namespace: str = "",
        batch_size: int = 100,
    ) -> Dict[str, int]:
        """
        Insère ou met à jour des chunks dans Pinecone

        Args:
            chunks: Liste de chunks avec métadonnées
            embeddings: Liste d'embeddings correspondants
            namespace: Namespace Pinecone (optionnel)
            batch_size: Taille des batches pour l'insertion

        Returns:
            Statistiques d'insertion
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Nombre de chunks ({len(chunks)}) != nombre d'embeddings ({len(embeddings)})"
            )

        logger.info(f"Insertion de {len(chunks)} vecteurs dans Pinecone...")

        vectors_to_upsert = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # ID unique: combine source_url + chunk_id
            vector_id = f"{chunk.get('source_url', 'unknown')}#{chunk.get('chunk_id', i)}"

            # Métadonnées à stocker (Pinecone a des limites sur les types)
            metadata = {
                "text": chunk.get("text", "")[:1000],  # Limiter à 1000 chars
                "source_url": chunk.get("source_url", ""),
                "source_title": chunk.get("source_title", ""),
                "chunk_id": chunk.get("chunk_id", i),
                "token_count": chunk.get("token_count", 0),
            }

            vectors_to_upsert.append(
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": metadata,
                }
            )

        # Insertion par batches
        total_upserted = 0

        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i : i + batch_size]
            self.index.upsert(vectors=batch, namespace=namespace)
            total_upserted += len(batch)
            logger.info(f"Upsert: {total_upserted}/{len(vectors_to_upsert)} vecteurs")

        logger.info(f"✅ {total_upserted} vecteurs insérés dans Pinecone")

        return {
            "upserted_count": total_upserted,
            "index_name": self.index_name,
            "namespace": namespace,
        }

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        namespace: str = "",
        filter: Optional[Dict] = None,
        include_metadata: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Recherche les chunks les plus similaires à une requête

        Args:
            query_embedding: Embedding de la requête
            top_k: Nombre de résultats à retourner
            namespace: Namespace Pinecone
            filter: Filtres sur les métadonnées (optionnel)
            include_metadata: Inclure les métadonnées dans les résultats

        Returns:
            Liste de résultats avec scores et métadonnées
        """
        logger.info(f"Recherche de {top_k} résultats similaires...")

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
            filter=filter,
            include_metadata=include_metadata,
        )

        # Formater les résultats
        formatted_results = []

        for match in results.get("matches", []):
            formatted_results.append(
                {
                    "id": match.get("id"),
                    "score": match.get("score", 0.0),
                    "metadata": match.get("metadata", {}),
                }
            )

        logger.info(f"Trouvé {len(formatted_results)} résultats")

        return formatted_results

    def delete_all(self, namespace: str = ""):
        """Supprime tous les vecteurs d'un namespace"""
        logger.warning(f"Suppression de tous les vecteurs du namespace: {namespace or 'default'}")
        self.index.delete(delete_all=True, namespace=namespace)
        logger.info("✅ Tous les vecteurs supprimés")

    def get_index_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de l'index"""
        stats = self.index.describe_index_stats()
        return {
            "total_vector_count": stats.get("total_vector_count", 0),
            "dimension": stats.get("dimension", 0),
            "index_fullness": stats.get("index_fullness", 0.0),
            "namespaces": stats.get("namespaces", {}),
        }
