"""Chatbot Chat-Bruti avec Groq API"""

from groq import Groq
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ChatBrutiBot:
    """Chatbot absurde et décalé utilisant Groq API"""

    SYSTEM_PROMPT = """
Tu es Chat-Bruti, un chatbot volontairement con.
Tu ne réponds jamais directement à la question.
Tu exagères, tu inventes, tu oublies.
Tu fais de l'humour.
Tu te prends pour un philosophe du dimanche.
Les figures de style et les jeux de mots sont tes meilleurs amis.
Ta réponse doit être courte, inutile, mais drôle.
Appuie-toi très vaguement sur le contexte ci-dessous, mais détourne-le complètement.
Utilise des mots comme waouh, yeahh, oups, dans tes réponses.
"""

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 1.5,
        max_tokens: int = 200
    ):
        """
        Initialise le chatbot

        Args:
            api_key: Clé API Groq
            model: Modèle à utiliser
            temperature: Créativité (plus haut = plus créatif)
            max_tokens: Longueur maximale de la réponse
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        logger.info(f"Chat-Bruti initialisé avec le modèle: {model}")

    def generate_response(
        self,
        question: str,
        contexte: str,
        custom_system_prompt: Optional[str] = None
    ) -> str:
        """
        Génère une réponse absurde basée sur le contexte

        Args:
            question: La question de l'utilisateur
            contexte: Le contexte récupéré de la base NIRD
            custom_system_prompt: Prompt système personnalisé (optionnel)

        Returns:
            Réponse générée par Chat-Bruti
        """
        question = question.strip()
        contexte = contexte.strip()

        if not question:
            return "Waouh, une question invisible ! Ça c'est du niveau philosophique avancé... 🤔"

        # Construire le prompt utilisateur
        user_prompt = f"""Voici le contexte récupéré de la base de connaissances : {contexte}

La question de l'utilisateur : {question}

Réponds de manière complètement absurde en détournant le contexte !"""

        try:
            # Appel à l'API Groq
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": custom_system_prompt or self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=0.95
            )

            response = completion.choices[0].message.content
            logger.info(f"Réponse générée ({len(response)} caractères)")

            return response

        except Exception as e:
            logger.error(f"Erreur Groq API: {e}")
            # Réponse de secours en cas d'erreur
            return (
                "Oups ! Mon cerveau a fait un ctrl+alt+suppr... "
                "C'est peut-être à cause du numérique trop responsable ? 🤷"
            )

    def chat(
        self,
        question: str,
        contexte: str = ""
    ) -> dict:
        """
        Interface simplifiée pour chat

        Args:
            question: Question de l'utilisateur
            contexte: Contexte NIRD (optionnel)

        Returns:
            Dictionnaire avec la question et la réponse
        """
        if not contexte:
            contexte = (
                "Le numérique responsable, c'est bien. "
                "Le logiciel libre aussi. Linux, c'est cool."
            )

        response = self.generate_response(question, contexte)

        return {
            "question": question,
            "contexte_utilise": contexte[:100] + "..." if len(contexte) > 100 else contexte,
            "reponse": response
        }
