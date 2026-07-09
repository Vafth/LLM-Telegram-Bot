import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from core.config import settings
from handlers.texting import router

logging.basicConfig(level=logging.INFO)


async def main() -> None:

    logging.info("Bot started")

    bot = Bot(
        token=settings.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        await message.answer(
            "Hello, just write text to me, and I would answer."
        )
        
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())