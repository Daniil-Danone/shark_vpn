from aiogram import Dispatcher

from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from apps.users.service import UserService
from apps.configs.service import ConfigService
from apps.referals.service import ReferalService

from bot.config.scheduler import process_overdued_config

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *

from config.environment import REFERAL_BONUS, PARTNER_BONUS

from utils import openvpn
from utils.logger import bot_logger


async def process_start_message(
    message: Message, state: FSMContext
):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    partner_id = None

    user = await UserService.get_user(user_id=user_id)
    if not user:
        user = await UserService.create_user(
            user_id=user_id, full_name=full_name, username=username
        )

    try:
        partner_id = int(message.text.split(maxsplit=1)[1])
    except:
        pass

    if not partner_id:
        return await message.answer(
            text=messages.START_MESSAGE.format(full_name=full_name),
            reply_markup=keyboards.main_menu_keyboard()
        )
    
    if await ReferalService.get_partner_by_referal(referal_id=user_id):
        return await message.answer(
            text=messages.START_MESSAGE.format(full_name=full_name),
            reply_markup=keyboards.main_menu_keyboard()
        )

    try:
        partner = await UserService.get_user(user_id=partner_id)
        referal = await ReferalService.create_referal(
            partner=partner, referal=user
        )

        await UserService.accure_bonuses(
            user_id=referal.referal.user_id, amount=REFERAL_BONUS
        )

        await UserService.accure_bonuses(
            user_id=referal.partner.user_id, amount=PARTNER_BONUS
        )
        
    except Exception as e:
        bot_logger.error(f"[STARTUP] Failed to create referal: {e}")
        pass

    return await message.answer(
        text=messages.START_MESSAGE.format(full_name=full_name),
        reply_markup=keyboards.main_menu_keyboard()
    )


async def process_test_revoke_command(message: Message, state: FSMContext):
    await state.clear()
    configs = await ConfigService.get_user_configs(user_id=message.from_user.id)
    await process_overdued_config(overdue_config=configs[0])

    return await message.answer(text="test revoke")


def register_handlers_general(dp: Dispatcher):
    dp.message.register(
        process_start_message, CommandStart()
    )

    dp.message.register(
        process_test_revoke_command, Command("test_revoke")
    )
