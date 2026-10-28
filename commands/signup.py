import os
import httpx
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from backend_api_model.back_api_tg_user_to_signup import BackApiTgUserToSignup
from backend_api_model.back_api_user_logged_in import BackApiUserLoggedIn
from backend_validators.validate_user_to_signup_login import validate_user_to_signup_login
from backend_validators.validate_user_to_signup_pwd import validate_user_to_signup_pwd
from services.env.env import BACKEND_API_URL
from utils.tg_users import get_tg_user



signup_router = Router()



class SignupStates(StatesGroup):
    waiting_for_login = State()  # Ожидаем ввод логина
    waiting_for_pwd = State()  # Ожидаем ввод пароля


# /signup
@signup_router.message(Command('signup'))
async def signup_command_handler(tg_msg: Message, state: FSMContext) -> None:
    # Переводим пользователя в состояние ожидания логина
    await state.set_state(SignupStates.waiting_for_login)
    await tg_msg.answer(
        "🔑 Введите логин.\n"
        "Длина логина должна быть в диапазоне от 1 до 30 символов.\n"
    )


@signup_router.message(SignupStates.waiting_for_login, F.text)
async def process_login(tg_msg: Message, state: FSMContext):
    login: str = tg_msg.text

    try:
        validate_user_to_signup_login(login)
    except:
        await tg_msg.answer(
            "❌ Некорректный формат.\n"
            "Длина логина должна быть в диапазоне от 8 до 30 символов.\n"
            "\n"
            "🔑 Введите логин:\n"
        )
        return

    # Сохраняем введенный логин во временное хранилище FSM (in-memory storage)
    await state.update_data(login=login)

    # Переводим в следующее состояние — ожидание пароля
    await state.set_state(SignupStates.waiting_for_pwd)
    await tg_msg.answer(
        "🔒 Введите пароль.\n"
        "Длина пароля должна быть в диапазоне от 8 до 100 символов.\n"
        "Пароль должен содержать цифры и не цифры.\n"
    )


@signup_router.message(SignupStates.waiting_for_pwd, F.text)
async def process_pwd(tg_msg: Message, state: FSMContext):
    pwd: str = tg_msg.text
    #await tg_msg.edit_text("●●●●●●●●●●●●")

    try:
        validate_user_to_signup_pwd(pwd)
    except:
        await tg_msg.answer(
            "❌ Некорректный формат.\n"
            "Длина пароля должна быть в диапазоне от 8 до 100 символов.\n"
            "Пароль должен содержать цифры и не цифры.\n"
            "\n"
            "🔒 Введите пароль:\n"
        )
        return

    # Достаем ранее сохраненные данные (там лежит наш login)
    state_data = await state.get_data()
    login: str = state_data.pop("login")

    # Сразу очищаем состояние, чтобы пользователь мог снова пользоваться ботом
    await state.set_state(None)

    # Отправляем сообщение-индикатор загрузки (пользователь поймет, что бот думает)
    status_msg = await tg_msg.answer("🔄 Вхожу в аккаунт...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_API_URL}/tg_user/login",
                json=BackApiTgUserToSignup(
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
                    f"✅ Вы успешно зарегистрировались!\n"
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
