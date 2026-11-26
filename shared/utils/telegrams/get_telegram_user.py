from aiogram.types import Message, User

from shared.backend.modules.tg_user.api_model.tg_user import BackApiTgUser
from shared.utils.telegrams.telegram_user_wrapper import TelegramUserWrapper


def get_telegram_user(telegram_msg: Message) -> BackApiTgUser:
    return TelegramUserWrapper(telegram_msg.from_user)
