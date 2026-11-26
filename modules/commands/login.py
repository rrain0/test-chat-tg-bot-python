import httpx
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from shared.backend.modules.tg_user.api_model.to_login import BackApiTgUserToLogin
from shared.backend.modules.user.api_model.logged_in import BackApiUserLoggedIn
from core.config.env import BACKEND_API_URL
from shared.utils.telegrams.get_telegram_user import get_telegram_user



router_login = Router()



class LoginStates(StatesGroup):
    waiting_for_login = State()  # Ожидаем ввод логина
    waiting_for_pwd = State()  # Ожидаем ввод пароля


# /login
@router_login.message(Command("login"))
async def on_login_command(telegram_msg: Message, state: FSMContext) -> None:
    # Transition the user to the login-awaiting state
    await state.set_state(LoginStates.waiting_for_login)
    await telegram_msg.answer("🔑 Введите логин:")


@router_login.message(LoginStates.waiting_for_login, F.text)
async def process_login(telegram_msg: Message, state: FSMContext):
    # Save the entered login into FSM (in-memory storage) temp storage
    await state.update_data(login=telegram_msg.text)

    # Transition to the next state - waiting for a password
    await state.set_state(LoginStates.waiting_for_pwd)
    await telegram_msg.answer("🔒 Введите пароль:")


@router_login.message(LoginStates.waiting_for_pwd, F.text)
async def process_pwd(
        telegram_msg: Message,
        state: FSMContext,
        back_http_client: httpx.AsyncClient,
):
    pwd: str = telegram_msg.text
    #await tg_msg.edit_text("●●●●●●●●●●●●")

    # Retrieve previously saved data (the login)
    user_data = await state.get_data()
    login: str = user_data.pop("login")

    # Clear the context immediately for the user be able to use bot again
    await state.set_state(None)

    # Send status message to show user the bot is processing data
    status_msg = await telegram_msg.answer("⏳⏳⏳ Вхожу в аккаунт...")

    try:
        response = await back_http_client.post(
            f"{BACKEND_API_URL}/tg_user/login",
            json=BackApiTgUserToLogin(
                login=login,
                pwd=pwd,
                tg_user=get_telegram_user(telegram_msg),
            ).model_dump(),
            timeout=10.0,
        )

        if response.status_code == 200:
            data = BackApiUserLoggedIn.model_validate(response.json())

            await state.update_data(access_token=data.access_token)
            await status_msg.edit_text(
                f"✅ Вы успешно авторизовались!\n"
                f"user_id: {data.user.id}\n"
                f"user_username: {data.user.username}\n"
                f"tg_user_id: {get_telegram_user(telegram_msg).id}\n"
                f"tg_user_username: {get_telegram_user(telegram_msg).username}\n"
                f"access_token: {data.access_token}\n"
            )
        else:
            # Если бэкенд вернул 401 Unauthorized или 400
            await status_msg.edit_text(
                "❌ Неверный логин или пароль.\n"
                "Войти: /login\n"
                "Зарегистрироваться: /signup\n"
            )

    except Exception as e:
        print(f"Ошибка бэкенда: {e}")
        await status_msg.edit_text("⚠️ Ошибка сервера. Не удалось выполнить вход.")
