from aiogram import Dispatcher

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *
from bot.config.sessions import bot

from apps.users.service import UserService
from apps.operations.service import OperationService

from utils import helpers, payment

from config.environment import ADMIN_CHAT_ID, ADMIN_PANEL_LINK


async def process_balance_message(
    message: Message, state: FSMContext
):
    await state.clear()
    user_id = message.from_user.id

    user = await UserService.get_user(user_id=user_id)

    return await message.answer(
        text=messages.BALANCE_MENU.format(
            balance=user.balance, earned=user.earned
        ),
        reply_markup=keyboards.balance_keyboard()
    )


async def process_balance_callback(
    callback_query: CallbackQuery,
    callback_data: BalanceCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id
    action = callback_data.action

    if action == "cash_in":
        await state.set_state(BalanceState.cash_in)
        await callback_query.message.edit_reply_markup(None)
        last_message = await callback_query.message.answer(
            text=messages.BALANCE_CASH_IN_AMOUNT,
            reply_markup=keyboards.cancel_operation_keyboard()
        )
        await state.update_data(message_id=last_message.message_id)

    elif action == "cash_out":
        await callback_query.message.edit_reply_markup(None)

        user = await UserService.get_user(user_id=user_id)
        if user.balance < 2000:
            return await callback_query.message.answer(
                text=messages.BALANCE_CASH_OUT_NOT_ENOUGH_BALANCE.format(balance=round(user.balance, 2))
            )
        
        await state.set_state(BalanceState.cash_out)
        
        last_message = await callback_query.message.answer(
            text=messages.BALANCE_CASH_OUT_AMOUNT,
            reply_markup=keyboards.cancel_operation_keyboard()
        )
        await state.update_data(message_id=last_message.message_id)


async def process_cash_in_amount_message(
    message: Message,
    state: FSMContext
):
    user_id = message.from_user.id
    user = await UserService.get_user(user_id=user_id)

    raw_amount = message.text
    amount = helpers.get_amount(raw_amount=raw_amount)

    data = await state.get_data()
    message_id: int = data.get("message_id")

    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=message_id, reply_markup=None
        )
    except:
        pass

    if not amount:
        last_message = await message.answer(
            text=messages.INVALID_AMOUNT,
            reply_markup=keyboards.cancel_operation_keyboard()
        )

        await state.update_data(message_id=last_message.message_id)
        return
    
    try:
        payment_id, payment_url = payment.init_payment(
            amount=amount, description="Пополнение баланса SharkVPN",
            client_fullname=message.from_user.full_name, client_email="Andrey6091495@mail.ru"
        )

    except RuntimeError as e:
        return await message.answer(
            text=messages.FAILED_TO_INIT_PAYMENT,
        )
    
    operation = await OperationService.create_operation(
        type="cash_in", method="card", amount=amount, user=user, payment_id=payment_id
    )
    
    await state.clear()
    operation_message = await message.answer(
        text=messages.CASH_IN_PAYMENT.format(amount=amount),
        reply_markup=keyboards.cash_in_payment_keyboard(operation_id=operation.id, url=payment_url)
    )

    


async def process_cash_out_amount_message(
    message: Message,
    state: FSMContext
):
    user_id = message.from_user.id
    raw_amount = message.text
    amount = helpers.get_amount(raw_amount=raw_amount)

    data = await state.get_data()
    message_id: int = data.get("message_id")

    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=message_id, reply_markup=None
        )
    except:
        pass

    if not amount:
        last_message = await message.answer(
            text=messages.INVALID_AMOUNT,
            reply_markup=keyboards.cancel_operation_keyboard()
        )

        await state.update_data(message_id=last_message.message_id)
        return
    
    await state.set_state(BalanceState.card)
    await state.update_data(amount=amount)
    last_message = await message.answer(
        text=messages.BALANCE_CASH_OUT_CARD.format(
            amount=amount
        )
    )
    await state.update_data(message_id=last_message.message_id)


async def process_cancel_operation_callback(
    callback_query: CallbackQuery,
    callback_data: CancelBalanceOperationCallback,
    state: FSMContext
):
    await state.clear()
    user_id = callback_query.from_user.id

    data = await state.get_data()
    message_id: int = data.get("message_id")

    try:
        await callback_query.message.edit_reply_markup(None)
    except:
        pass

    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=message_id, reply_markup=None
        )
    except:
        pass

    user = await UserService.get_user(user_id=user_id)

    await callback_query.message.answer(
        text=messages.OPERATION_CANCELLED
    )

    return await callback_query.message.answer(
        text=messages.BALANCE_MENU.format(
            balance=user.balance, earned=user.earned
        ),
        reply_markup=keyboards.balance_keyboard()
    )


async def process_operation_callback(
    callback_query: CallbackQuery,
    callback_data: OperationCallback,
    state: FSMContext
):
    await state.clear()
    user_id = callback_query.from_user.id

    action = callback_data.action
    operation_id = callback_data.operation_id

    user = await UserService.get_user(user_id=user_id)

    operation = await OperationService.get_operation(operation_id=operation_id)

    if action == "done":
        try:
            status, payment_method_id = payment.check_status(payment_id=operation.payment_id)
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
            
        await OperationService.update_operation(
            operation_id=operation_id, data={"status": "done"}
        )

        await UserService.accure_balance(
            user_id=user_id, amount=operation.amount
        )

        user = await UserService.get_user(user_id=user_id)

        await callback_query.message.edit_reply_markup(None)

        return callback_query.message.answer(
            text=messages.BALANCE_CASH_IN_SUCCESS.format(
                balance=user.balance
            )
        )
    
    elif action == "cancel":
        if operation.method == "card":
            try:
                payment.cancel_payment(payment_id=operation.payment_id)
            except RuntimeError:
                pass

        await OperationService.update_operation(
            operation_id=operation_id, data={"status": "cancel"}
        )

        return await callback_query.message.edit_reply_markup(None)


async def process_cash_out_card_message(
    message: Message,
    state: FSMContext
):
    user_id = message.from_user.id
    wallet_or_card = message.text

    data = await state.get_data()
    amount: float = data.get("amount")
    message_id: int = data.get("message_id")

    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=message_id, reply_markup=None
        )
    except:
        pass

    user = await UserService.get_user(user_id=user_id)

    operation = await OperationService.create_operation(
        type="cash_out", method="card", amount=amount, user=user, wallet=wallet_or_card
    )

    admin_message = messages.NEW_CASH_OUT_OPERATION_CARD.format(
        amount=amount, card=wallet_or_card, 
        user_info=f"{user.user_id} | {user.full_name}",
        admin_link=f"{ADMIN_PANEL_LINK}/operations/operation/{operation.id}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            reply_markup=keyboards.complete_cash_out_keyboard(operation_id=operation.id)
        )
    
    except:
        pass

    await state.clear()

    return await message.answer(
        text=messages.BALANCE_CASH_OUT_CREATED
    )


async def process_complete_cash_out_callback(
    callback_query: CallbackQuery,
    callback_data: CompleteCashOutCallback,
    state: FSMContext
):
    action = callback_data.action
    operation_id = callback_data.operation_id

    operation = await OperationService.get_operation(operation_id=operation_id)
    if not operation:
        return await callback_query.answer(
            text=messages.FAILED_TO_FOUND_OPERATION, show_alert=True
        )
    
    user = await UserService.get_user(user_id=operation.user.user_id)

    if action == "done":
        await OperationService.update_operation(operation_id=operation_id, data={"status": "done"})
        await UserService.writeoff_balance(user_id=user.user_id, amount=operation.amount)

        try:
            await bot.send_message(
                chat_id=user.user_id, 
                text=messages.CASH_OUT_OPERATION_DONE
            )
        except:
            pass

        return await callback_query.message.edit_text(
            text=f"{callback_query.message.html_text}\n\n✅ Оплачено!", reply_markup=None
        )

    elif action == "cancel":
        await OperationService.update_operation(operation_id=operation_id, data={"status": "cancel"})
        try:
            await bot.send_message(
                chat_id=user.user_id, 
                text=messages.CASH_OUT_OPERATION_CANCEL
            )
        except:
            pass

        return await callback_query.message.edit_text(
            text=f"{callback_query.message.html_text}\n\n❌ Операция отменена", reply_markup=None
        )


def register_handlers_balance(dp: Dispatcher):
    dp.message.register(
        process_balance_message, lambda message: message.text == "💰 Баланс"
    )

    dp.callback_query.register(
        process_balance_callback, BalanceCallback.filter()
    )

    dp.message.register(
        process_cash_in_amount_message, BalanceState.cash_in
    )

    dp.message.register(
        process_cash_out_amount_message, BalanceState.cash_out
    )

    dp.callback_query.register(
        process_cancel_operation_callback, CancelBalanceOperationCallback.filter()
    )

    dp.callback_query.register(
        process_operation_callback, OperationCallback.filter()
    )

    dp.message.register(
        process_cash_out_card_message, BalanceState.card
    )

    dp.callback_query.register(
        process_complete_cash_out_callback, CompleteCashOutCallback.filter()
    )