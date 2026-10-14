from aiogram.types import Message

from api_model.api_tg_user import ApiTgUser


def get_tg_user(message: Message) -> ApiTgUser:
    return ApiTgUser(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
