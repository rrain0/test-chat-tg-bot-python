from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


user_info_router = Router()


# /user_info
@user_info_router.message(Command('user_info'))
async def user_info_command_handler(tg_msg: Message) -> None:
    await tg_msg.answer(
        f"User info\n"
        f"tg_user_id: {tg_msg.from_user.id}\n"
        f"tg_username: {tg_msg.from_user.username}\n"
        f"tg_first_name: {tg_msg.from_user.first_name}\n"
        f"tg_last_name: {tg_msg.from_user.last_name}\n"
        f"tg_chat_id: {tg_msg.chat.id}\n"
    )
