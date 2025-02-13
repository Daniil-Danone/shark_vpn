from datetime import date
from django.utils import timezone
from typing import List, Optional
from babel.dates import format_date

from apps.users.models import User
from apps.configs.models import Config
from apps.referals.models import Referal

from config.environment import ITEMS_PER_PAGE
from bot.config import messages


def form_date(date: date):
    return format_date(date=date, format='d MMMM y', locale='ru')


def create_config_message(configs: List[Config], page: Optional[int] = 0) -> str:
    now = timezone.now()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_configs = configs[start_idx:end_idx]

    text = "<blockquote>📝 Мои конфиги</blockquote>\n\n"

    configs_str = []

    for config in page_configs:
        if config.expiring_at < now.date():
            continue

        date = form_date(date=config.expiring_at)

        configs_str.append(f"Конфиг: {config.config_name}.ovpn\nАктивен до: {date}")

    if len(configs_str) == 0:
        configs_str.append("У вас ещё нет конфигов")
     
    text += "\n\n".join(configs_str)
    return text


def create_referal_message(user: User, bot_username: str) -> str:
    referal_link = f"https://t.me/{bot_username}?start={user.user_id}"

    return messages.REFERAL_MESSAGE.format(
        referal_link=referal_link,
    )


def get_amount(raw_amount: str) -> float:
    try:
        raw_amount = raw_amount.replace(",", ".")
        return float(raw_amount)
    except:
        return None