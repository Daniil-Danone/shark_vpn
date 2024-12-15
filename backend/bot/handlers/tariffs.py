from aiogram import Dispatcher

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from apps.users.service import UserService
from apps.tariffs.service import TariffService
from apps.configs.service import ConfigService

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *

from utils import helpers


async def process_tariff_message(
    message: Message, state: FSMContext
):
    tariffs = await TariffService.get_tariffs()

    return await message.answer(
        text=messages.TARIFFS_MENU,
        reply_markup=keyboards.tariffs_keyboard(tariffs=tariffs)
    )


async def process_tariff_callback(
    callback_query: CallbackQuery,
    callback_data: TariffCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id
    
    action = callback_data.action
    page = callback_data.page
    tariff_id = callback_data.tariff_id

    if action == "page":
        tariffs = await TariffService.get_tariffs()
        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.tariffs_keyboard(
                tariffs=tariffs, page=page
            )
        )
    
    elif action == "tariff":
        user = await UserService.get_user(user_id=user_id)
        tariff = await TariffService.get_tariff(tariff_id=tariff_id)
        
        config = await ConfigService.create_config(
            user=user, tariff=tariff
        )

        return await callback_query.message.edit_text(
            text=messages.TARIFF_PAYMENT.format(
                title=tariff.title, price=tariff.price
            ),
            reply_markup=keyboards.tariff_payment_keyboard(
                config_id=config.id, url="https://example.org/"
            )
        )


async def process_payment_callback(
    callback_query: CallbackQuery,
    callback_data: PaymentCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    config_id = callback_data.config_id

    if action == "done":
        config = await ConfigService.update_config(
            config_id=config_id, status="done"
        )

        date = helpers.form_date(date=config.expiring_at.date())
        time = config.expiring_at.strftime("%H:%M")

        return await callback_query.message.edit_text(
            text=messages.TARIFF_PAYMENT_DONE.format(
                config_name="test.config",
                expiring_at=f"{date} {time}"
            )
        )
    
    elif action == "cancel":
        await ConfigService.update_config(
            config_id=config_id, status="cancel"
        )

        return await callback_query.message.edit_text(
            text=messages.TARIFF_PAYMENT_CANCELED
        )


def register_handlers_tariffs(dp: Dispatcher):
    dp.message.register(
        process_tariff_message, lambda message: message.text == "💵 Тарифы"
    )

    dp.callback_query.register(
        process_tariff_callback, TariffCallback.filter()
    )

    dp.callback_query.register(
        process_payment_callback, PaymentCallback.filter()
    )