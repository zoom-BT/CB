"""Module de découpage (chunking) du texte et tokenization"""

import tiktoken
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """Classe pour découper le texte en chunks et gérer la tokenization"""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base",
    ):
        """
        Initialise le chunker

        Args:
            chunk_size: Taille des chunks en caractères
            chunk_overlap: Chevauchement entre chunks
            encoding_name: Nom de l'encodage tiktoken (cl100k_base pour GPT-4/Gemini)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialiser l'encodeur tiktoken
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception as e:
            logger.warning(f"Erreur chargement encodage {encoding_name}: {e}")
            self.encoding = tiktoken.get_encoding("cl100k_base")

        # Initialiser le text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def count_tokens(self, text: str) -> int:
        """
        Compte le nombre de tokens dans un texte

        Args:
            text: Le texte à analyser

        Returns:
            Nombre de tokens
        """
        return len(self.encoding.encode(text))

    def tokenize(self, text: str) -> List[int]:
        """
        Convertit un texte en tokens

        Args:
            text: Le texte à tokenizer

        Returns:
            Liste des tokens (IDs)
        """
        return self.encoding.encode(text)

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Découpe un texte en chunks avec métadonnées

        Args:
            text: Le texte à découper
            metadata: Métadonnées à ajouter à chaque chunk

        Returns:
            Liste de dictionnaires contenant les chunks et leurs métadonnées
        """
        if not text:
            return []

        metadata = metadata or {}
        chunks = self.splitter.split_text(text)

        result = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "chunk_id": i,
                "text": chunk,
                "token_count": self.count_tokens(chunk),
                **metadata,
            }
            result.append(chunk_data)

        logger.info(f"Texte découpé en {len(result)} chunks")
        return result

    def chunk_documents(
        self, documents: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Découpe plusieurs documents en chunks

        Args:
            documents: Liste de documents avec 'content', 'url', 'title'

        Returns:
            Liste de tous les chunks avec métadonnées
        """
        all_chunks = []

        for doc in documents:
            if not doc.get("content"):
                continue

            metadata = {
                "source_url": doc.get("url", ""),
                "source_title": doc.get("title", ""),
            }

            chunks = self.chunk_text(doc["content"], metadata)
            all_chunks.extend(chunks)

        logger.info(
            f"Total de {len(all_chunks)} chunks créés depuis {len(documents)} documents"
        )
        return all_chunks
