import httpx
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand

from commands.hi import hi_router
from commands.login import login_router
from commands.signup import signup_router
from commands.start import start_router
from commands.user_info import user_info_router
from env import TG_BOT_TOKEN, BACKEND_API_URL
from utils.datetimes import now
from utils.tg_users import get_tg_user



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
        BotCommand(command="/login", description="Залогиниться"),
        BotCommand(command="/signup", description="Зарегистрироваться"),
    ]
    await bot.set_my_commands(main_menu_commands)








async def post_to_backend(endpoint: str, access_token: str, payload: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        return await client.post(f"{BACKEND_API_URL}{endpoint}", json=payload, headers=headers)


# Хэндлер на любые текстовые сообщения (Эхо-функция)
# Используем магический фильтр F.text, чтобы реагировать только на текст
# @dp.message(F.text)
# async def echo_handler(message: Message) -> None:
#     msg_text = message.text
#     tg_user = get_tg_user(message)
#     tg_user_tk = create_tg_user_access_token(
#         user_id=tg_user.id,
#         user_username=tg_user.username,
#         user_first_name=tg_user.first_name,
#         user_last_name=tg_user.last_name,
#         created_at=now(),
#     )
#     await post_to_backend(
#         "/tg_user/message",
#         tg_user_tk,
#         {msg_text: msg_text}
#     )
#     await message.answer(f"You said: {msg_text}")










async def main() -> None:
    dp.include_routers(
        start_router,
        hi_router,
        user_info_router,
        login_router,
        signup_router,
    )
    # Настраиваем меню команд
    await set_main_menu(bot)
    # Запускаем опрос серверов Telegram (Long Polling)
    print("Bot is running... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
