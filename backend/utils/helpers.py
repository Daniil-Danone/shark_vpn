from datetime import date
from typing import List
from babel.dates import format_date

from apps.users.models import User
from apps.configs.models import Config
from apps.referals.models import Referal

from bot.config import messages


def form_date(date: date):
    return format_date(date=date, format='d MMMM y', locale='ru')


def create_config_message(configs: List[Config]) -> str:
    text = "<blockquote>📝 Мои конфиги</blockquote>\n\n"

    configs_str = []

    for config in configs:
        date = form_date(date=config.expiring_at.date())
        time = config.expiring_at.strftime("%H:%M")

        configs_str.append(f"Конфиг: {config.config_name}\nАктивен до: {date} {time}")

    if len(configs_str) == 0:
        configs_str.append("У вас ещё нет конфигов")
     
    text += "\n\n".join(configs_str)
    return text


def create_referal_message(user: User, bot_username: str, referals: List[Referal]) -> str:
    referal_link = f"https://t.me/{bot_username}?start={user.user_id}"

    referals_str = []

    for referal in referals:
        date = form_date(referal.invited_at.date())
        time = referal.invited_at.strftime("%H:%M")

        referals_str.append(
            f"• {referal.referal.full_name} - {date} {time}"
        )
    
    if len(referals_str) == 0:
        referals_str.append("• пусто")

    return messages.REFERAL_MESSAGE.format(
        referal_link=referal_link,
        earned=user.earned,
        referals_count=len(referals),
        referals="\n".join(referals_str)
    )


def get_amount(raw_amount: str) -> float:
    try:
        raw_amount = raw_amount.replace(",", ".")
        return float(raw_amount)
    except:
        return None