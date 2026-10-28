import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand

from commands.any_message import any_message_router
from commands.hi import hi_router
from commands.login import login_router
from commands.signup import signup_router
from commands.start import start_router
from commands.user_info import user_info_router
from services.env.env import TG_BOT_TOKEN

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



async def main() -> None:
    dp.include_routers(
        start_router,
        hi_router,
        user_info_router,
        login_router,
        signup_router,
        any_message_router,
    )
    # Настраиваем меню команд
    await set_main_menu(bot)
    # Запускаем опрос серверов Telegram (Long Polling)
    print("Bot is running... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
