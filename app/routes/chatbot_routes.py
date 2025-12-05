"""Routes API pour le chatbot Chat-Bruti (Module 3)"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.config import settings
from app.modules.chatbot import ChatBrutiBot

logger = logging.getLogger(__name__)

# Créer le router
router = APIRouter(prefix="/chatbot", tags=["Chat-Bruti"])

# Instance globale du chatbot
chatbot: Optional[ChatBrutiBot] = None


# Modèles Pydantic
class ChatRequest(BaseModel):
    """Requête pour le chatbot"""
    contexte: str
    question: str

    class Config:
        extra = "ignore"


class ChatResponse(BaseModel):
    """Réponse du chatbot"""
    response: str


def get_chatbot() -> ChatBrutiBot:
    """Récupère ou initialise le chatbot"""
    global chatbot

    if chatbot is None:
        if not settings.GROQ_API_KEY:
            raise HTTPException(
                status_code=500,
                detail=(
                    "GROQ_API_KEY non configurée. "
                    "Obtenez une clé gratuite sur https://console.groq.com/keys "
                    "et ajoutez-la dans le fichier .env"
                )
            )

        logger.info("Initialisation de Chat-Bruti...")
        chatbot = ChatBrutiBot(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=settings.CHATBOT_TEMPERATURE,
            max_tokens=settings.CHATBOT_MAX_TOKENS
        )

    return chatbot


@router.get("/")
async def chatbot_root():
    """Info sur le chatbot"""
    return {
        "name": "Chat-Bruti",
        "description": "Chatbot volontairement absurde et décalé",
        "model": settings.GROQ_MODEL,
        "temperature": settings.CHATBOT_TEMPERATURE,
        "personality": "Philosophe du dimanche qui détourne tout",
        "status": "ready"
    }


@router.post("/ask", response_model=ChatResponse)
async def ask_chatbruti(payload: ChatRequest):
    """
    Pose une question au chatbot Chat-Bruti

    Le chatbot utilise le contexte fourni pour générer une réponse
    absurde et décalée.
    """
    try:
        contexte = payload.contexte.strip()
        question = payload.question.strip()

        if not question:
            raise HTTPException(status_code=400, detail="Question vide")

        # Récupérer le chatbot
        bot = get_chatbot()

        # Générer la réponse
        answer = bot.generate_response(
            question=question,
            contexte=contexte
        )

        return ChatResponse(response=answer)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la génération de réponse: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur: {str(e)}"
        )


@router.post("/chat")
async def simple_chat(question: str, contexte: str = ""):
    """
    Interface simplifiée pour discuter avec Chat-Bruti

    Args:
        question: La question à poser
        contexte: Contexte optionnel
    """
    try:
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question vide")

        bot = get_chatbot()
        result = bot.chat(question=question, contexte=contexte)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))
