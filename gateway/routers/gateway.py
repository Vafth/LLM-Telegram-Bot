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
    

# ── Helpers ───────────────────────────────────────────────────────────────────

async def _ask_ollama(client: httpx.AsyncClient, messages: list[dict]) -> str:
    resp = await client.post(
        f"{settings.OLLAMA_URL}/api/chat",
        json={
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
        },
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


async def _ask_vllm(client: httpx.AsyncClient, messages: list[dict]) -> str:
    resp = await client.post(
        f"{settings.VLLM_URL}/v1/chat/completions",
        json={
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
        },
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    import logging
    logging.info(f"Sending to {settings.LLM_PROVIDER}: {body.messages}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            if settings.LLM_PROVIDER == "vllm":
                content = await _ask_vllm(client, body.messages)
            else:
                content = await _ask_ollama(client, body.messages)
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="LLM timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    return ChatResponse(reply=content)
