from aiogram import Dispatcher

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *



async def process_cooperation_message(
    message: Message, state: FSMContext
):
    return await message.answer(
        text=messages.COOPERATION_MESSAGE
    )


def register_handlers_cooperation(dp: Dispatcher):
    dp.message.register(
        process_cooperation_message, lambda message: message.text == "🤝 Сотрудничество"
    )