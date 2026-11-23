from aiogram.filters import Command
from aiogram.types import Message, User
from aiogram import Router


router_hi = Router()


# /hi
@router_hi.message(Command("hi"))
async def on_hi_command(tg_msg: Message) -> None:
    tg_user: User = tg_msg.from_user
    await tg_msg.answer(
        f"Hello {tg_user.first_name}! I am your Python bot. How can I help you today?"
    )
