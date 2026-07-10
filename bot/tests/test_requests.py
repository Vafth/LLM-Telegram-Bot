import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@patch("core.requests.httpx.AsyncClient")
async def ask_gateway_success(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"reply": "Hello there!"}
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__aenter__.return_value.post = AsyncMock(
        return_value=mock_response
    )

    from core.requests import ask_gateway
    result = await ask_gateway([{"role": "user", "content": "Hello"}])

    assert result == "Hello there!"

@patch("core.requests.httpx.AsyncClient")
async def test_ask_gateway_http_error(mock_client):
    import httpx
    mock_client.return_value.__aenter__.return_value.post = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "error", request=MagicMock(), response=MagicMock()
        )
    )

    from core.requests import ask_gateway
    with pytest.raises(httpx.HTTPStatusError):
        await ask_gateway([{"role": "user", "content": "Hello"}])