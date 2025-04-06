import os
from aiogram import Dispatcher

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.config import messages
from bot.config import keyboards
from bot.config.constants import instruction_video_filename
from bot.config.states import *
from bot.config.callbacks import *

from apps.configs.service import ConfigService
from config import settings

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
        return await callback_query.message.edit_text(
            text=helpers.create_config_message(configs=configs, page=page),
            reply_markup=keyboards.configs_keyboard(configs=configs, page=page)
        )
    
    elif action == "config":
        config = await ConfigService.get_config(config_id=config_id)

        config_filename = f"{config.config_name}.ovpn"
        config_path = CONFIGS_DIR / config_filename

        if not os.path.exists(config_path):
            return await callback_query.message.answer(
                text=messages.CONFIG_FILE_NOT_FOUND
            )
        
        date = helpers.form_date(date=config.expiring_at)
        
        return await callback_query.message.answer_document(
            document=FSInputFile(path=config_path, filename=config_filename),
            caption=messages.CONFIG_FILE.format(
                config_name=config_filename,
                expiring_at=date,
                sub="✅ Активна" if config.is_sub else "❌ Неактивна"
            )
        )

    elif action == "instruction":
        video_path = os.path.join(settings.MEDIA_ROOT, instruction_video_filename)

        if not os.path.exists(video_path):
            return await callback_query.message.answer(f"⚠️ Видео не найдено")

        video_file = FSInputFile(video_path)

        try:
            await callback_query.message.answer_video(
                video=video_file,
                caption="Вот инструкция 🎥"
            )

        except Exception as e:
            await callback_query.message.answer(f"❌ Произошла ошибка при отправке видео")
        

def register_handlers_configs(dp: Dispatcher):
    dp.message.register(
        process_configs_message, lambda message: message.text == "📝 Мои конфиги"
    )

    dp.callback_query.register(
        process_config_callback, ConfigCallback.filter()
    )