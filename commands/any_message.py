import httpx
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from env import BACKEND_API_URL



any_message_router = Router()



async def post_to_backend(endpoint: str, access_token: str, payload: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        return await client.post(f"{BACKEND_API_URL}{endpoint}", json=payload, headers=headers)



# Хэндлер на любые текстовые сообщения (Эхо-функция)
# Используем магический фильтр F.text, чтобы реагировать только на текст
@any_message_router.message(F.text)
async def send_message(message: Message, state: FSMContext) -> None:
    access_token = (await state.get_data()).get("access_token")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_API_URL}{"/tg_user/message"}",
            json={"message_text": message.text},
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code == 200:
            await message.answer("✅ Сообщение успешно отправлено")
            return

        if response.status_code == 401:
            await message.answer(
                "❌ Ошибка: Вход не выполнен\n"
                "Войти: /login\n"
                "Зарегистрироваться: /signup\n"
            )
            return

        await message.answer("❌ unexpected error")



