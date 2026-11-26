from aiogram.types import User


class TelegramUserWrapper:
    def __init__(self, telegram_user: User) -> None:
        self._user: User = telegram_user

    @property
    def id(self) -> int:
        return self._user.id

    @property
    def username(self) -> str:
        return self._user.username

    @property
    def first_name(self) -> str:
        return self._user.first_name

    @property
    def last_name(self) -> str:
        return self._user.last_name
