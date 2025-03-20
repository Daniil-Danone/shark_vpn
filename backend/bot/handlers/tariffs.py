from django.utils import timezone

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from apps.users.service import UserService
from apps.tariffs.service import TariffService, ReceiptService
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
        
        receipt = await ReceiptService.create_receipt(
            user=user, tariff=tariff, payment_id=payment_id
        )

        if user.balance >= tariff.price:
            receipt_message = await callback_query.message.edit_text(
                text=messages.TARIFF_PAYMENT_BALANCE.format(
                    title=tariff.title, price=tariff.price
                ),
                reply_markup=keyboards.tariff_payment_keyboard(
                    receipt_id=receipt.id, url=payment_url, is_balance=True
                )
            )

            await ReceiptService.set_message_id(receipt_id=receipt.id, message_id=receipt_message.message_id)
            return

        receipt_message = await callback_query.message.edit_text(
            text=messages.TARIFF_PAYMENT.format(
                title=tariff.title, price=tariff.price
            ),
            reply_markup=keyboards.tariff_payment_keyboard(
                receipt_id=receipt.id, url=payment_url, is_balance=False
            )
        )

        await ReceiptService.set_message_id(receipt_id=receipt.id, message_id=receipt_message.message_id)
        return


async def process_payment_callback(
    callback_query: CallbackQuery,
    callback_data: PaymentCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    receipt_id = callback_data.receipt_id

    user = await UserService.get_user(user_id=user_id)
    receipt = await ReceiptService.get_receipt(receipt_id=receipt_id)

    if action in ["done", "balance"]:
        if receipt.status in ["done", "balance"]:
            await callback_query.message.delete()
            return await callback_query.answer(
                text=messages.PAYMENT_ALREADY_DONE,
                show_alert=True
            )
        
        payment_method_id = None
        
        if action == "done":
            try:
                status, payment_method_id = payment.check_status(payment_id=receipt.payment_id)
                if not status:
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
            if user.balance < receipt.tariff.price:
                return await callback_query.answer(
                    text=messages.FAILED_TO_PAY_BALANCE
                )
            
            await UserService.writeoff_balance(user_id=user.user_id, amount=float(receipt.tariff.price))
            
        partner = await ReferalService.get_partner_by_referal(referal_id=user_id)
        if partner:
            await UserService.accure_bonuses(
                user_id=partner.user_id, 
                amount=receipt.tariff.partner_bonuses
            )

        await callback_query.message.delete()
            
        config_name = openvpn.generate_vpn_config()

        config = await ConfigService.create_config(
            user=user, tariff=receipt.tariff, receipt=receipt, config_name=config_name
        )
        
        await ConfigService.update_config(
            config_id=config.id, data={"payment_method_id": payment_method_id}
        )

        now = timezone.now()

        await ReceiptService.update_receipt(
            receipt_id=receipt_id, data={
                "status": action,
                "payed_at": now
            }
        )

        config_filename = f"{config_name}.ovpn"
        config_file = CONFIGS_DIR / f"{config_filename}"

        date = helpers.form_date(date=config.expiring_at)

        return await callback_query.message.answer_document(
            document=FSInputFile(path=config_file, filename=config_filename),
            caption=messages.TARIFF_PAYMENT_DONE.format(
                config_name=config_name,
                expiring_at=date
            )
        )
    
    elif action == "cancel":
        if receipt.status in ["done", "balance"]:
            await callback_query.message.delete()
            return await callback_query.answer(
                text=messages.PAYMENT_ALREADY_DONE,
                show_alert=True
            )
        
        try:
            payment.cancel_payment(
                payment_id=receipt.payment_id
            )
        except RuntimeError:
            pass

        now = timezone.now()

        await ReceiptService.update_receipt(
            receipt_id=receipt_id, data={
                "status": "cancel",
                "cancelled_at": now
            }
        )

        return await callback_query.message.delete()
    

async def process_retry_reccurent_payment_callback(
    callback_query: CallbackQuery,
    callback_data: RetryReccurentCallback,
    state: FSMContext
):
    config = await ConfigService.get_config(config_id=callback_data.config_id)

    payment_id = payment.init_recurrent_payment(
        amount=config.tariff.price,
        payment_method_id=config.payment_method_id,
        description=f"Оплата подписки {config.tariff.title}",
    )

    receipt = await ReceiptService.create_receipt(
        user=config.user, tariff=config.tariff,
        payment_id=payment_id
    )

    await ReceiptService.update_receipt(
        receipt_id=receipt.id, data={
            "is_reccurent": True,
            "config_id": config.id
        }
    )

    await callback_query.message.edit_reply_markup(None)

    return await callback_query.answer(
        text=messages.RECCURENT_PAYMENT_DONE
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