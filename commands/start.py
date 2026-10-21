from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router


start_router = Router()


# /start
@start_router.message(CommandStart())
async def start_command_handler(tg_msg: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await tg_msg.answer(
        f"Бот работает"
    )
