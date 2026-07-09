from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.requests import ask_gateway

router = Router()

MAX_MESSAGES = 5

@router.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    history = data.get("history", [])
    
    import logging
    logging.info(f"History before request: {history}")
    
    history.append({"role": "user", "content": message.text})
    if len(history) > MAX_MESSAGES:
        history = history[-MAX_MESSAGES:]

    thinking = await message.reply("...")

    try:
        reply = await ask_gateway(history)
        history.append({"role": "assistant", "content": reply})
        await state.update_data(history=history)
        
        if not reply.strip():
            await thinking.edit_text("(empty response)")
        else:
            await thinking.edit_text(reply)
    except Exception as e:
        await thinking.edit_text(f"Error: {e}")


@router.message(F.text == "/clear")
async def handle_clear(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.reply("History cleared.")