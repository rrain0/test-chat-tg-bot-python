from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


hi_router = Router()


# /hi
@hi_router.message(Command('hi'))
async def hi_command_handler(tg_msg: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await tg_msg.answer(
        f"Hello {tg_msg.from_user.first_name}! I am your Python bot. How can I help you today?"
    )
