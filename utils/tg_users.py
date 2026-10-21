from aiogram.types import Message

from backend_api_model.back_api_tg_user import BackApiTgUser


def get_tg_user(tg_msg: Message) -> BackApiTgUser:
    return BackApiTgUser(
        id=tg_msg.from_user.id,
        username=tg_msg.from_user.username,
        first_name=tg_msg.from_user.first_name,
        last_name=tg_msg.from_user.last_name,
    )
