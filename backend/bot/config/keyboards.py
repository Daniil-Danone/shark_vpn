from typing import List
from django.utils import timezone
from aiogram.types import KeyboardButton, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from apps.faq.models import FAQProblem, FAQTheme
from apps.tariffs.models import Tariff
from apps.configs.models import Config

from bot.config.callbacks import *

from config.environment import ITEMS_PER_PAGE


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="💵 Тарифы"),
        KeyboardButton(text="📝 Мои конфиги"),
        KeyboardButton(text="💰 Баланс"),
        KeyboardButton(text="👥 Реферальная система"),
        KeyboardButton(text="❓ Помощь 24/7"),
        KeyboardButton(text="🤝 Сотрудничество"),
        KeyboardButton(text="🔒 Конфиденциальность"),
    ]

    builder.row(buttons[0], buttons[1])
    builder.row(buttons[2], buttons[3])
    builder.row(buttons[4])
    builder.row(buttons[5])
    builder.row(buttons[6])

    return builder.as_markup(resize_keyboard=True)


def tariffs_keyboard(tariffs: List[Tariff], page: int = 0):
    builder = InlineKeyboardBuilder()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_tariffs = tariffs[start_idx:end_idx]

    for tariff in page_tariffs:
        builder.row(
            InlineKeyboardButton(text=f"{tariff.title} - {tariff.price} руб.", callback_data=TariffCallback(action="tariff", tariff_id=tariff.id).pack())
        )

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=TariffCallback(action="page", tariff_id=0, page=page-1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    pagination_buttons.append(
        InlineKeyboardButton(text=f"Страница {page + 1}", callback_data="ignore")
    )

    if end_idx < len(tariffs):
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=TariffCallback(action="page", tariff_id=0, page=page+1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    if len(tariffs) > ITEMS_PER_PAGE:
        builder.row(*pagination_buttons)

    return builder.as_markup()


def tariff_payment_keyboard(receipt_id: int, url: str, is_balance: bool):    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Оплатить по ссылке", url=url)
    )

    if is_balance:
        builder.row(
            InlineKeyboardButton(text="Списать с баланса", callback_data=PaymentCallback(action="balance", receipt_id=receipt_id).pack())
        )

    builder.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data=PaymentCallback(action="cancel", receipt_id=receipt_id).pack())
    )

    return builder.as_markup()


def cooperation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Google форма", url="https://example.org/")
    )

    builder.adjust(1)
    return builder.as_markup()


def configs_keyboard(configs: List[Config], page: int = 0):
    builder = InlineKeyboardBuilder()

    now = timezone.now()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_configs = configs[start_idx:end_idx]

    for config in page_configs:       
        builder.row(
            InlineKeyboardButton(text=f"{config.config_name}.ovpn", callback_data=ConfigCallback(action="config", config_id=config.id).pack())
        )

    builder.row(InlineKeyboardButton(text="🎬 Видео-Инструкция", callback_data=ConfigCallback(action="instruction", config_id=0).pack()))

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=ConfigCallback(action="page", config_id=0, page=page-1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    pagination_buttons.append(
        InlineKeyboardButton(text=f"Страница {page + 1}", callback_data="ignore")
    )

    if end_idx < len(configs):
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=ConfigCallback(action="page", config_id=0, page=page+1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )
    
    if len(configs) > ITEMS_PER_PAGE:
        builder.row(*pagination_buttons)

    return builder.as_markup()


def balance_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Пополнить", callback_data=BalanceCallback(action="cash_in").pack())
    )

    builder.add(
        InlineKeyboardButton(text="Вывести", callback_data=BalanceCallback(action="cash_out").pack())
    )

    builder.adjust(2)
    return builder.as_markup()


def cancel_operation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="❌ Отмена", callback_data=CancelBalanceOperationCallback().pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def cash_in_payment_keyboard(operation_id: int, url: str):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Пополнить", url=url)
    )

    builder.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data=OperationCallback(operation_id=operation_id, action="cancel").pack())
    )

    return builder.as_markup()


def faq_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Инструкция по установке", callback_data=FAQCallback(action="instruction").pack())
    )

    builder.add(
        InlineKeyboardButton(text="VPN не работает", callback_data=FAQCallback(action="problems").pack())
    )

    builder.add(
        InlineKeyboardButton(text="Подписки", callback_data=FAQCallback(action="sub").pack())
    )

    builder.add(
        InlineKeyboardButton(text="Чат поддержки", callback_data=FAQCallback(action="tech_support").pack())
    )

    builder.add(
        InlineKeyboardButton(text="Выплаты", callback_data=FAQCallback(action="cash_outs").pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def configs_sub_keyboard(configs: List[Config], page: int = 0):
    builder = InlineKeyboardBuilder()

    now = timezone.now()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_configs = configs[start_idx:end_idx]

    for config in page_configs:
        if config.expiring_at < now.date():
            continue
        
        builder.row(
            InlineKeyboardButton(text=f"{config.config_name}.ovpn", callback_data=ConfigSubCallback(action="config", config_id=config.id).pack())
        )

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=ConfigSubCallback(action="page", config_id=0, page=page-1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    pagination_buttons.append(
        InlineKeyboardButton(text=f"Страница {page + 1}", callback_data="ignore")
    )

    if end_idx < len(configs):
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=ConfigSubCallback(action="page", config_id=0, page=page+1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )
    
    if len(configs) > ITEMS_PER_PAGE:
        builder.row(*pagination_buttons)

    return builder.as_markup()


def retry_reccurent_payment_keyboard(config_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Оплатить", callback_data=RetryReccurentCallback(config_id=config_id).pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def restore_sub(config_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Включить подписку", callback_data=RestoreSubCallback(action="restore", config_id=config_id).pack())
    )

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data=RestoreSubCallback(action="back", config_id=config_id).pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def cancel_sub(config_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Отменить подписку", callback_data=ConfigCancelSubCallback(action="cancel", config_id=config_id).pack())
    )

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data=ConfigCancelSubCallback(action="back", config_id=config_id).pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def cancel_sub_confirm(config_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Да, отменить подписку", callback_data=ConfigCancelSubConfirmCallback(action="cancel", config_id=config_id).pack())
    )

    builder.add(
        InlineKeyboardButton(text="Нет, не отменять", callback_data=ConfigCancelSubConfirmCallback(action="back", config_id=config_id).pack())
    )

    builder.adjust(1)
    return builder.as_markup()


def themes_keyboard(themes: List[FAQTheme], page: int = 0):
    builder = InlineKeyboardBuilder()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_themes = themes[start_idx:end_idx]

    for theme in page_themes:
        builder.row(
            InlineKeyboardButton(text=theme.title, callback_data=ThemeCallback(action="theme", theme_id=theme.id).pack())
        )

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=ThemeCallback(action="page", theme_id=0, page=page-1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    pagination_buttons.append(
        InlineKeyboardButton(text=f"Страница {page + 1}", callback_data="ignore")
    )

    if end_idx < len(themes):
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=ThemeCallback(action="page", theme_id=0, page=page+1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )
    
    if len(themes) > ITEMS_PER_PAGE:
        builder.row(*pagination_buttons)

    return builder.as_markup()


def problems_keyboard(problems: List[FAQProblem], theme_id: int, page: int = 0):
    builder = InlineKeyboardBuilder()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_problems = problems[start_idx:end_idx]

    for problem in page_problems:
        builder.row(
            InlineKeyboardButton(text=problem.question, callback_data=ProblemCallback(action="problem", theme_id=theme_id, problem_id=problem.id).pack())
        )

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=ProblemCallback(action="page", theme_id=theme_id, problem_id=0, page=page-1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )

    pagination_buttons.append(
        InlineKeyboardButton(text=f"Страница {page + 1}", callback_data="ignore")
    )

    if end_idx < len(problems):
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=ProblemCallback(action="page", theme_id=theme_id, problem_id=0, page=page+1).pack())
        )
    else:
        pagination_buttons.append(
            InlineKeyboardButton(text=" ", callback_data="ignore")
        )
    
    if len(problems) > ITEMS_PER_PAGE:
        builder.row(*pagination_buttons)

    builder.row(
        InlineKeyboardButton(text="⬅️ Назад к темам", callback_data=ProblemCallback(action="back", theme_id=theme_id, problem_id=0).pack())
    )

    return builder.as_markup()


def problem_keyboard(theme_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="⬅️ Назад к проблемам", callback_data=SolutionCallback(theme_id=theme_id).pack())
    )

    return builder.as_markup()


def complete_cash_out_keyboard(operation_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="✅ Оплачено!", callback_data=CompleteCashOutCallback(action="done", operation_id=operation_id).pack())
    )

    builder.add(
        InlineKeyboardButton(text="❌ Отменить операцию", callback_data=CompleteCashOutCallback(action="cancel", operation_id=operation_id).pack())
    )

    return builder.as_markup()
