import os
from aiogram import Dispatcher

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *

from apps.configs.service import ConfigService

from config.environment import CONFIGS_DIR

from utils import helpers


async def process_configs_message(
    message: Message, state: FSMContext
):
    user_id = message.from_user.id

    configs = await ConfigService.get_user_configs(user_id=user_id)

    text = helpers.create_config_message(configs=configs)

    return await message.answer(
        text=text,
        reply_markup=keyboards.configs_keyboard(configs=configs)
    )


async def process_config_callback(
    callback_query: CallbackQuery,
    callback_data: ConfigCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    config_id = callback_data.config_id
    page = callback_data.page

    if action == "page":
        configs = await ConfigService.get_user_configs(user_id=user_id)
        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.configs_keyboard(configs=configs, page=page)
        )
    
    elif action == "config":
        config = await ConfigService.get_config(config_id=config_id)

        config_file = CONFIGS_DIR / config.config_name

        if not os.path.exists(config_file):
            return await callback_query.message.answer(
                text=messages.CONFIG_FILE_NOT_FOUND
            )
        
        date = helpers.form_date(date=config.expiring_at)
        
        return await callback_query.message.answer_document(
            document=FSInputFile(path=config_file, filename=config.config_name),
            caption=messages.CONFIG_FILE.format(
                config_name=config.config_name,
                expiring_at=date
            )
        )
        

def register_handlers_configs(dp: Dispatcher):
    dp.message.register(
        process_configs_message, lambda message: message.text == "📝 Мои конфиги"
    )

    dp.callback_query.register(
        process_config_callback, ConfigCallback.filter()
    )