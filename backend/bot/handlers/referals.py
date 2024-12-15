from aiogram import Dispatcher

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *
from bot.config.sessions import bot

from apps.users.service import UserService
from apps.referals.service import ReferalService

from utils import helpers

async def process_referal_message(
    message: Message, state: FSMContext
):
    user_id = message.from_user.id

    user = await UserService.get_user(user_id=user_id)
    referals = await ReferalService.get_referals(partner_id=user_id)

    bot_info = await bot.get_me()
    
    return await message.answer(
        text=helpers.create_referal_message(
            user=user, bot_username=bot_info.username, referals=referals 
        )
    )


def register_handlers_referal(dp: Dispatcher):
    dp.message.register(
        process_referal_message, lambda message: message.text == "👥 Реферальная система"
    )