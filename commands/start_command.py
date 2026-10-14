from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router


start_router = Router()


# /start
@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await message.answer(
        f"Бот работает"
    )
