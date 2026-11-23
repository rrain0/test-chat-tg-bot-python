from uuid import uuid7

import httpx
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config.env import BACKEND_API_URL
from shared.backend.modules.msg.api_model.msg_text import BackApiMsgText
from shared.backend.modules.session.tg_bot.jwt_access.create_tg_bot_access_token import create_tg_bot_access_token
from shared.utils.datetimes.now import now
from shared.utils.telegrams.get_telegram_user import get_telegram_user

router_any_message = Router()



# Хэндлер на любые текстовые сообщения (Эхо-функция)
# Используем магический фильтр F.text, чтобы реагировать только на текст
@router_any_message.message(F.text)
async def on_any_message(
        telegram_msg: Message,
        back_http_client: httpx.AsyncClient,
        state: FSMContext,
):
    access_token_str, access_token = create_tg_bot_access_token(
        id=uuid7(),
        created_at=now(),
        tg_user_id=get_telegram_user(telegram_msg).id,
        tg_user_username=get_telegram_user(telegram_msg).username,
    )

    msg_text: str = telegram_msg.text

    response = await back_http_client.post(
        f"{BACKEND_API_URL}/msg",
        headers={"Authorization": f"Bearer {access_token_str}"},
        json=BackApiMsgText(msg_text=msg_text).model_dump(),
    )

    if response.status_code == 200:
        await telegram_msg.answer("✅ Сообщение успешно отправлено")
        return

    if response.status_code == 401:
        await telegram_msg.answer(
            "⚠️ Ошибка: Вход не выполнен\n"
            "Войти: /login\n"
            "Зарегистрироваться: /signup\n"
        )
        return

    await telegram_msg.answer("❌ unexpected error")
