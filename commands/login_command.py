import httpx
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pydantic import BaseModel
from aiogram import Router

from api_model.api_tg_user import ApiTgUser
from api_model.api_user import ApiUser
from env import BACKEND_API_URL
from utils.tg_users import get_tg_user



login_router = Router()



class LoginStates(StatesGroup):
    waiting_for_login = State()  # Ожидаем ввод логина
    waiting_for_pwd = State()  # Ожидаем ввод пароля

class ApiTgUserLogin(BaseModel):
    login: str
    pwd: str
    tg_user: ApiTgUser

class ApiUserLoggedIn(BaseModel):
    access_token: str
    user: ApiUser


# /login
@login_router.message(Command('login'))
async def command_login_handler(message: Message, state: FSMContext) -> None:
    # Переводим пользователя в состояние ожидания логина
    await state.set_state(LoginStates.waiting_for_login)
    await message.answer("🔑 Введите логин:")


@login_router.message(LoginStates.waiting_for_login, F.text)
async def process_login(message: Message, state: FSMContext):
    # Сохраняем введенный логин во временное хранилище FSM (in-memory storage)
    await state.update_data(login=message.text)

    # Переводим в следующее состояние — ожидание пароля
    await state.set_state(LoginStates.waiting_for_pwd)
    await message.answer("🔒 Введите пароль:")


@login_router.message(LoginStates.waiting_for_pwd, F.text)
async def process_pwd(message: Message, state: FSMContext):
    pwd = message.text
    #await message.edit_text("●●●●●●●●●●●●")

    # Достаем ранее сохраненные данные (там лежит наш login)
    user_data = await state.get_data()
    login = user_data.get("login")

    # Сразу очищаем состояние, чтобы пользователь мог снова пользоваться ботом
    await state.clear()

    # Отправляем сообщение-индикатор загрузки (пользователь поймет, что бот думает)
    status_msg = await message.answer("🔄 Вхожу в аккаунт...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_API_URL}/tg_user/login",
                json=ApiTgUserLogin(
                    login=login,
                    pwd=pwd,
                    tg_user=get_tg_user(message),
                ).model_dump(),
                timeout=10.0,
            )

            if response.status_code == 200:
                data = ApiUserLoggedIn.model_validate(response.json())

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
                    "Попробуйте снова: /login\n"
                    "Или зарегистрируйтесь: /signup"
                )

    except Exception as e:
        print(f"Ошибка бэкенда: {e}")
        await status_msg.edit_text("⚠️ Ошибка сервера. Не удалось выполнить вход.")
