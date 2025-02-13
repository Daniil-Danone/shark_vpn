from aiogram import Dispatcher

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from apps.users.service import UserService
from apps.tariffs.service import TariffService
from apps.configs.service import ConfigService
from apps.referals.service import ReferalService

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *

from config.environment import CONFIGS_DIR

from utils import helpers, openvpn, payment


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

        try:
            payment_id, payment_url = payment.init_payment(
                amount=tariff.price, description=tariff.title,
                client_fullname=callback_query.from_user.full_name, client_email="it@ledokol.it"
            )

        except RuntimeError as e:
            return await callback_query.answer(
                text=messages.FAILED_TO_INIT_PAYMENT,
                show_alert=True
            )
        
        config = await ConfigService.create_config(
            user=user, tariff=tariff, payment_id=payment_id
        )

        if user.balance >= tariff.price:
            return await callback_query.message.edit_text(
                text=messages.TARIFF_PAYMENT_BALANCE.format(
                    title=tariff.title, price=tariff.price
                ),
                reply_markup=keyboards.tariff_payment_keyboard(
                    config_id=config.id, url=payment_url, is_balance=True
                )
            )

        return await callback_query.message.edit_text(
            text=messages.TARIFF_PAYMENT.format(
                title=tariff.title, price=tariff.price
            ),
            reply_markup=keyboards.tariff_payment_keyboard(
                config_id=config.id, url=payment_url, is_balance=False
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

    user = await UserService.get_user(user_id=user_id)
    config = await ConfigService.get_config(config_id=config_id)

    if action in ["done", "balance"]:
        if action == "done":
            try:
                if not payment.check_status(payment_id=config.payment_id):
                    return await callback_query.answer(
                        text=messages.PAYMENT_NOT_CONFIRMED,
                        show_alert=True
                    )
            except RuntimeError:
                return await callback_query.answer(
                    text=messages.FAILED_TO_CHECK_PAYMENT,
                    show_alert=True
                )
        
        elif action == "balance":
            if user.balance < config.tariff.price:
                return await callback_query.answer(
                    text=messages.FAILED_TO_PAY_BALANCE
                )
            
            await UserService.writeoff_balance(user=user, amount=float(config.tariff.price))
            
        partner = await ReferalService.get_partner_by_referal(referal_id=user_id)
        if partner:
            await UserService.accure_bonuses(partner=partner, amount=config.tariff.partner_bonuses)
            
        config_name = openvpn.generate_vpn_config()

        config_filename = f"{config_name}.ovpn"
        config_file = CONFIGS_DIR / f"{config_filename}"

        upd_config = await ConfigService.update_config(
            config_id=config_id, payment_status="done", config_name=config_name
        )

        date = helpers.form_date(date=upd_config.expiring_at)

        return await callback_query.message.answer_document(
            document=FSInputFile(path=config_file, filename=config_filename),
            caption=messages.TARIFF_PAYMENT_DONE.format(
                config_name=config_name,
                expiring_at=date
            )
        )
    
    elif action == "cancel":
        try:
            payment.cancel_payment(
                payment_id=config.payment_id
            )
        except RuntimeError:
            pass

        await ConfigService.update_config(
            config_id=config_id, payment_status="cancel"
        )

        return await callback_query.message.delete()


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