import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import httpx

from modules.commands.any_message import router_any_message
from modules.commands.hi import router_hi
from modules.commands.login import router_login
from modules.commands.signup import router_signup
from modules.commands.start import router_start
from modules.commands.user_info import router_user_info
from core.config.env import TELEGRAM_BOT_TOKEN
from core.config.env import BACKEND_API_URL

# Настройка логирования для отслеживания работы бота
logging.basicConfig(level=logging.INFO, stream=sys.stdout)



# 1. Функция, которая управляет жизненным циклом (Lifespan)
async def on_startup(dispatcher: Dispatcher):
    logging.info("Инициализация httpx.AsyncClient...")

    # Создаем один клиент на всё время работы бота
    # Настраиваем базовый URL и заголовки, чтобы не дублировать их в запросах
    #headers = {"X-Bot-Token": API_SECRET_TOKEN}
    back_http_client = httpx.AsyncClient(
        base_url=BACKEND_API_URL,
        #headers=headers,
        timeout=10.0,
    )

    # Сохраняем клиент в workflow_data диспетчера, чтобы он был доступен в хэндлерах
    dispatcher["back_http_client"] = back_http_client


async def on_shutdown(dispatcher: Dispatcher):
    logging.info("Закрытие httpx.AsyncClient...")

    # Достаем клиент и правильно его закрываем
    back_http_client: httpx.AsyncClient = dispatcher["back_http_client"]
    await back_http_client.aclose()



bot = Bot(token=TELEGRAM_BOT_TOKEN)
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



async def main():
    # Регистрируем роутеры
    dp.include_routers(
        router_start,
        router_hi,
        router_user_info,
        router_login,
        router_signup,
        router_any_message,
    )

    # Регистрируем функции старта и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Настраиваем меню команд
    await set_main_menu(bot)

    # Запускаем опрос серверов Telegram (Long Polling)
    print("Bot is running... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
