from aiogram import Dispatcher

from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from apps.users.service import UserService
from apps.referals.service import ReferalService

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *


async def process_start_message(
    message: Message, state: FSMContext
):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    user = await UserService.get_user(user_id=user_id)
    if not user:
        user = await UserService.create_user(
            user_id=user_id, full_name=full_name, username=username
        )

    try:
        partner_id = int(message.text.split(maxsplit=1)[1])
        
        if not await ReferalService.get_referal(partner_id=partner_id, referal_id=user_id):
            partner = await UserService.get_user(user_id=partner_id)
            await ReferalService.create_referal(partner=partner, referal=user)
            await UserService.accure_referal_bonuses(referal=user)
            await UserService.accure_partner_bonuses(partner=partner)
    except:
        pass

    return await message.answer(
        text=messages.START_MESSAGE.format(full_name=full_name),
        reply_markup=keyboards.main_menu_keyboard()
    )


def register_handlers_general(dp: Dispatcher):
    dp.message.register(
        process_start_message, CommandStart()
    )
