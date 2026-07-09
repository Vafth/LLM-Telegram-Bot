from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

from core.config import settings

router = APIRouter()


# ── Models ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    reply: str
    

# ── Ollama ────────────────────────────────────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    import logging
    logging.info(f"Sending to Ollama: {body.messages}")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(
                f"{settings.OLLAMA_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": body.messages,
                    "stream": False,
                },
            )
            resp.raise_for_status()
            logging.info(f"Ollama raw response: {resp.json()}")  # ← to jest kluczowe
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Ollama timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

    content = resp.json()["message"]["content"]
    logging.info(f"Extracted content: '{content}'")
    return ChatResponse(reply=content) 
