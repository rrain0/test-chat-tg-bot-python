import os
from datetime import timedelta

from shared.utils.datetimes.duration_to_timedelta import duration_to_timedelta


BACKEND_API_URL: str = os.getenv("BACKEND_API_URL")

TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

TG_BOT_ACCESS_TOKEN_SECRET: str = os.getenv("TG_BOT_ACCESS_TOKEN_SECRET")
TG_BOT_ACCESS_TOKEN_LIFETIME: timedelta = duration_to_timedelta(os.getenv("TG_BOT_ACCESS_TOKEN_LIFETIME"))
