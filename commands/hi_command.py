from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


hi_router = Router()


# /hi
@hi_router.message(Command('hi'))
async def command_hi_handler(message: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await message.answer(
        f"Hello {message.from_user.first_name}! I am your Python bot. How can I help you today?"
    )
