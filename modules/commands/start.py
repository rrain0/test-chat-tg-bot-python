from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router


router_start = Router()


# /start
@router_start.message(CommandStart())
async def start_command_handler(tg_msg: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await tg_msg.answer("Бот работает")
