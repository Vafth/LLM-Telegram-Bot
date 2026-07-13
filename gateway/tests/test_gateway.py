import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "gateway"}


@patch("routers.gateway.settings")
@patch("routers.gateway.httpx.AsyncClient")
async def test_chat_success_ollama(mock_client, mock_settings):
    mock_settings.LLM_PROVIDER = "ollama"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "message": {"content": "Hello there!"}
    }
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__aenter__.return_value.post = AsyncMock(
        return_value=mock_response
    )

    response = client.post("/chat", json={"messages": [
        {"role": "user", "content": "Hello"}
    ]})

    assert response.status_code == 200
    assert response.json()["reply"] == "Hello there!"


@patch("routers.gateway.settings")
@patch("routers.gateway.httpx.AsyncClient")
async def test_chat_success_vllm(mock_client, mock_settings):
    mock_settings.LLM_PROVIDER = "vllm"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello there!"}}]
    }
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__aenter__.return_value.post = AsyncMock(
        return_value=mock_response
    )

    response = client.post("/chat", json={"messages": [
        {"role": "user", "content": "Hello"}
    ]})

    assert response.status_code == 200
    assert response.json()["reply"] == "Hello there!"


@patch("routers.gateway.httpx.AsyncClient")
async def test_chat_timeout(mock_client):
    import httpx
    mock_client.return_value.__aenter__.return_value.post = AsyncMock(
        side_effect=httpx.TimeoutException("timeout")
    )

    response = client.post("/chat", json={"messages": [
        {"role": "user", "content": "Hello"}
    ]})

    assert response.status_code == 504