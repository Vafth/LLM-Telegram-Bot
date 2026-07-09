import httpx
from core.config import settings

async def ask_gateway(messages: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.GATEWAY_URL}/chat",
            json={"messages": messages},
        )
        response.raise_for_status()
        return response.json()["reply"]