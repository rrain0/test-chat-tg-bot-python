from aiogram.types import Message

from backend_api_model.back_api_tg_user import BackApiTgUser


def get_tg_user(message: Message) -> BackApiTgUser:
    return BackApiTgUser(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
