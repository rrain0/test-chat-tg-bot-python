from aiogram.types import Message, User

from shared.backend.modules.tg_user.api_model.tg_user import BackApiTgUser


def get_telegram_user(telegram_msg: Message) -> BackApiTgUser:
    tg_user: User = telegram_msg.from_user
    return BackApiTgUser(
        id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
    )
