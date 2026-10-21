import httpx
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from backend_api_model.back_api_tg_user_to_login import BackApiTgUserToLogin
from backend_api_model.back_api_user_logged_in import BackApiUserLoggedIn
from env import BACKEND_API_URL
from utils.tg_users import get_tg_user



login_router = Router()



class LoginStates(StatesGroup):
    waiting_for_login = State()  # Ожидаем ввод логина
    waiting_for_pwd = State()  # Ожидаем ввод пароля


# /login
@login_router.message(Command('login'))
async def login_command_handler(tg_msg: Message, state: FSMContext) -> None:
    # Переводим пользователя в состояние ожидания логина
    await state.set_state(LoginStates.waiting_for_login)
    await tg_msg.answer("🔑 Введите логин:")


@login_router.message(LoginStates.waiting_for_login, F.text)
async def process_login(tg_msg: Message, state: FSMContext):
    # Сохраняем введенный логин во временное хранилище FSM (in-memory storage)
    await state.update_data(login=tg_msg.text)

    # Переводим в следующее состояние — ожидание пароля
    await state.set_state(LoginStates.waiting_for_pwd)
    await tg_msg.answer("🔒 Введите пароль:")


@login_router.message(LoginStates.waiting_for_pwd, F.text)
async def process_pwd(tg_msg: Message, state: FSMContext):
    pwd: str = tg_msg.text
    #await tg_msg.edit_text("●●●●●●●●●●●●")

    # Достаем ранее сохраненные данные (там лежит наш login)
    user_data = await state.get_data()
    login: str = user_data.pop("login")

    # Сразу очищаем контекст, чтобы пользователь мог снова пользоваться ботом
    await state.set_state(None)

    # Отправляем сообщение-индикатор загрузки (пользователь поймет, что бот думает)
    status_msg = await tg_msg.answer("🔄 Вхожу в аккаунт...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_API_URL}/tg_user/login",
                json=BackApiTgUserToLogin(
                    login=login,
                    pwd=pwd,
                    tg_user=get_tg_user(tg_msg),
                ).model_dump(),
                timeout=10.0,
            )

            if response.status_code == 200:
                data = BackApiUserLoggedIn.model_validate(response.json())

                await state.update_data(access_token=data.access_token)
                await status_msg.edit_text(
                    f"✅ Вы успешно авторизовались!\n"
                    f"user_login: {data.user.login}"
                    f"user_id: {data.user.id}\n"
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
