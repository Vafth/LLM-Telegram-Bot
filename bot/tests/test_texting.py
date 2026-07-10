import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.types import Message, User, Chat

def make_message(text: str) -> MagicMock:
    message = MagicMock(spec=Message)
    message.text = text
    message.chat = MagicMock(spec=Chat)
    message.chat.id = 123
    message.from_user = MagicMock(spec=User)
    message.reply = AsyncMock(return_value=MagicMock(edit_text=AsyncMock()))
    return message

@patch("handlers.texting.ask_gateway")
async def test_handle_text_success(mock_ask):
    mock_ask.return_value = "Hello there!"

    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.base import StorageKey

    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=123, user_id=1)
    state = FSMContext(storage=storage, key=key)

    from handlers.texting import handle_text
    message = make_message("Hello")
    await handle_text(message, state)

    mock_ask.assert_called_once()
    message.reply.assert_called_once_with("...")

@patch("handlers.texting.ask_gateway")
async def test_handle_text_error(mock_ask):
    mock_ask.side_effect = Exception("gateway down")

    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.base import StorageKey

    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=123, user_id=1)
    state = FSMContext(storage=storage, key=key)

    from handlers.texting import handle_text
    message = make_message("Hello")
    await handle_text(message, state)

    thinking = message.reply.return_value
    thinking.edit_text.assert_called_once_with("Error: gateway down")