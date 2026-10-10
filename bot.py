from pydantic import BaseModel
import httpx
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

from env import TG_BOT_TOKEN, BACKEND_API_URL
from services.jwt_tg_user_service import create_tg_user_access_token
from utils.datetimes import now


async def post_to_backend(endpoint: str, access_token: str, payload: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        return await client.post(f"{BACKEND_API_URL}{endpoint}", json=payload, headers=headers)


class TgUser(BaseModel):
    id: int
    username: str | None
    first_name: str
    last_name: str | None

def get_tg_user(message: Message) -> TgUser:
    return TgUser(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )


# Настройка логирования для отслеживания работы бота
logging.basicConfig(level=logging.INFO, stream=sys.stdout)



bot = Bot(token=TG_BOT_TOKEN)
# Инициализируем диспетчер (главный роутер обновлений)
dp = Dispatcher()



async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/hi", description="Поприветствовать бота"),
        BotCommand(command="/user_info", description="Информация о пользователе"),
    ]
    await bot.set_my_commands(main_menu_commands)


# Хэндлер на команду /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await message.answer(
        f"Бот работает"
    )


# Хэндлер на команду /hi
@dp.message(Command('hi'))
async def command_hi_handler(message: Message) -> None:
    # html.bold автоматически экранирует спецсимволы в имени пользователя
    await message.answer(
        f"Hello {message.from_user.first_name}! I am your Python bot. How can I help you today?"
    )


# Хэндлер на команду /user_info
@dp.message(Command('user_info'))
async def command_user_info_handler(message: Message) -> None:
    await message.answer(
        f"User info\n"
        f"tg_user_id: {message.from_user.id}\n"
        f"tg_username: {message.from_user.username}\n"
        f"tg_first_name: {message.from_user.first_name}\n"
        f"tg_last_name: {message.from_user.last_name}\n"
        f"tg_chat_id: {message.chat.id}\n"
    )



# Хэндлер на любые текстовые сообщения (Эхо-функция)
# Используем магический фильтр F.text, чтобы реагировать только на текст
@dp.message(F.text)
async def echo_handler(message: Message) -> None:
    msg_text = message.text
    tg_user = get_tg_user(message)
    tg_user_tk = create_tg_user_access_token(
        user_id=tg_user.id,
        user_username=tg_user.username,
        user_first_name=tg_user.first_name,
        user_last_name=tg_user.last_name,
        created_at=now(),
    )
    await post_to_backend(
        "/tg_user/message",
        tg_user_tk,
        {msg_text: msg_text}
    )
    await message.answer(f"You said: {msg_text}")



async def main() -> None:
    # Настраиваем меню команд
    await set_main_menu(bot)
    # Запускаем опрос серверов Telegram (Long Polling)
    print("Bot is running... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
