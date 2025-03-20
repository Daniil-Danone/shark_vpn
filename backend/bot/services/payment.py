from typing import Dict, Optional
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from apps.tariffs.models import Receipt
from apps.users.service import UserService
from apps.operations.models import Operation
from apps.configs.service import ConfigService
from apps.tariffs.service import ReceiptService
from apps.referals.service import ReferalService
from apps.operations.service import OperationService

from bot.config import messages, keyboards

from config.environment import BOT_TOKEN, CONFIGS_DIR

from utils import openvpn, helpers
from utils.logger import bot_logger


async def send_receipt_confirm(receipt: Receipt, payment_object: Dict):
    try:
        user = await UserService.get_user(user_id=receipt.user.user_id)

        now = timezone.now()
        await ReceiptService.update_receipt(
            receipt_id=receipt.id, data={"status": "done", "payed_at": now}
        )

        bot = Bot(
            token=BOT_TOKEN, 
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, link_preview_is_disabled=True
            )
        )

        if receipt.is_reccurent:
            duration_type = receipt.tariff.duration_type
            duration_value = receipt.tariff.duration_value

            if duration_type == "days":
                expiring_at = now + relativedelta(days=duration_value)
            elif duration_type == "weeks":
                expiring_at = now + relativedelta(weeks=duration_value)
            elif duration_type == "months":
                expiring_at = now + relativedelta(months=duration_value)
            elif duration_type == "years":
                expiring_at = now + relativedelta(years=duration_value)

            await ConfigService.update_config(
                config_id=receipt.config_id,
                data={
                    "expiring_at": expiring_at,
                    "status": "enable",
                    "active": "connected"
                }
            )

            config = await ConfigService.get_config(config_id=receipt.config_id)

            await bot.send_message(
                chat_id=user.user_id, 
                text=messages.RECCURENT_PAYMENT_DONE.format(
                    config_name=f"{config.config_name}.ovpn",
                    expiring_at=helpers.form_date(config.expiring_at)
                )
            )
            return

        partner = await ReferalService.get_partner_by_referal(referal_id=receipt.user.user_id)
        if partner:
            await UserService.accure_bonuses(
                user_id=partner.user_id, 
                amount=receipt.tariff.partner_bonuses
            )

        try:
            await bot.edit_message_reply_markup(
                chat_id=user.user_id,
                message_id=receipt.message_id,
                reply_markup=None
            )
        except Exception as e:
            bot_logger.error(f"[PAYMENT] Failed to delete message keyboard: {e}")
        
        try:
            await bot.delete_message(
                chat_id=user.user_id,
                message_id=receipt.message_id
            )
        except Exception as e:
            bot_logger.error(f"[PAYMENT] Failed to delete message: {e}")
        
        payment_method_id = None
        payment_method: Optional[Dict[str, str]] = payment_object.get("payment_method", None)
        if payment_method:
            payment_method_id: str = payment_method.get("id")

        config_name = openvpn.generate_vpn_config()

        config = await ConfigService.create_config(
            user=user, tariff=receipt.tariff, receipt=receipt, config_name=config_name
        )

        if payment_method_id:
            await ConfigService.update_config(config_id=config.id, data={"payment_method_id": payment_method_id})

        config_filename = f"{config_name}.ovpn"
        config_file = CONFIGS_DIR / f"{config_filename}"

        date = helpers.form_date(date=config.expiring_at)

        await bot.send_document(
            chat_id=user.user_id,
            document=FSInputFile(path=config_file, filename=config_filename),
            caption=messages.TARIFF_PAYMENT_DONE.format(
                config_name=config_name,
                expiring_at=date
            )
        )
    except Exception as e:
        bot_logger.error(f"[PAYMENT] Error: {e}")
    finally:
        await bot.session.close()


async def send_operation_confirm(operation: Operation, payment_object: Dict):
    try:
        bot = Bot(
            token=BOT_TOKEN, 
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, link_preview_is_disabled=True
            )
        )

        await OperationService.update_operation(
            operation_id=operation.id, data={"status": "done"}
        )

        await UserService.accure_balance(
            user_id=operation.user.user_id, amount=operation.amount
        )

        user = await UserService.get_user(user_id=operation.user.user_id)

        await bot.send_message(
            chat_id=operation.user.user_id,
            text=messages.BALANCE_CASH_IN_SUCCESS.format(
                balance=user.balance
            )
        )

    except Exception as e:
        bot_logger.error(f"[PAYMENT][SEND CONFIRM OPERATION] Error: {e}")
    finally:
        await bot.session.close()


async def send_confirm(payment_id: str, payment_object: Dict):
    try:
        receipt = await ReceiptService.get_receipt_by_payment_id(payment_id=payment_id)
        operation = await OperationService.get_operation_by_payment_id(payment_id=payment_id)

        if receipt:
            await send_receipt_confirm(receipt=receipt, payment_object=payment_object)
        elif operation:
            await send_operation_confirm(operation=operation, payment_object=payment_object)

    except Exception as e:
        bot_logger.error(f"[PAYMENT][SEND CONFIRM] Error: {e}")


async def send_receipt_cancel(receipt: Receipt):
    try:
        user = await UserService.get_user(user_id=receipt.user.user_id)

        now = timezone.now()

        await ReceiptService.update_receipt(
            receipt_id=receipt.id, data={"status": "cancel", "cancelled_at": now}
        )

        bot = Bot(
            token=BOT_TOKEN, 
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, link_preview_is_disabled=True
            )
        )

        if receipt.is_reccurent:
            config = await ConfigService.get_config(config_id=receipt.config_id)

            await bot.send_message(
                chat_id=user.user_id, 
                text=messages.RECCURENT_PAYMENT_FAILED.format(
                    config_name=f"{config.config_name}.ovpn"
                ),
                reply_markup=keyboards.retry_reccurent_payment_keyboard(config_id=config.id)
            )
            return

        await bot.send_message(
            chat_id=user.user_id, text=messages.TARIFF_PAYMENT_CANCELED
        )
    except Exception as e:
        bot_logger.error(f"[PAYMENT][SEND CANCEL RECEIPT] Error: {e}")
    finally:
        await bot.session.close()


async def send_operation_cancel(operation: Operation):
    try:
        bot = Bot(
            token=BOT_TOKEN, 
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, link_preview_is_disabled=True
            )
        )

        await OperationService.update_operation(
            operation_id=operation.id, data={"status": "cancel"}
        )

        await bot.send_message(
            chat_id=operation.user.user_id,
            text=messages.OPERATION_CANCELLED
        )

    except Exception as e:
        bot_logger.error(f"[PAYMENT][SEND CANCEL OPERATION] Error: {e}")
    finally:
        await bot.session.close()

async def send_cancel(payment_id: str):
    try:
        receipt = await ReceiptService.get_receipt_by_payment_id(payment_id=payment_id)
        operation = await OperationService.get_operation_by_payment_id(payment_id=payment_id)
        
        if receipt:
            await send_receipt_cancel(receipt=receipt)
        elif operation:
            await send_operation_cancel(operation=operation)
    except Exception as e:
        bot_logger.error(f"[PAYMENT][SEND CANCEL] Error: {e}")