import os
from aiogram import Dispatcher

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.configs.service import ConfigService
from utils import helpers
from bot.config import messages
from bot.config import keyboards
from bot.config.states import *
from bot.config.callbacks import *

from apps.faq.service import FAQThemeService, FAQProblemService


async def process_faq_message(
    message: Message, state: FSMContext
):
    return await message.answer(
        text=messages.FAQ_MENU,
        reply_markup=keyboards.faq_keyboard()
    )


async def process_faq_callback(
    callback_query: CallbackQuery,
    callback_data: FAQCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action

    if action == "instruction":
        await callback_query.message.edit_reply_markup(None)
        return await callback_query.message.answer(
            text=messages.FAQ_INSTRUCTION
        )
    
    elif action == "problems":
        return await callback_query.message.answer(
            text=messages.FAQ_VPN_NOT_WORKING
        )

    elif action == "tech_support":
        await callback_query.message.edit_reply_markup(None)
        return await callback_query.message.answer(
            text=messages.FAQ_SUPPORT
        )
    
    elif action == "cash_outs":
        await callback_query.message.edit_reply_markup(None)
        return await callback_query.message.answer(
            text=messages.FAQ_CASHOUTS
        )
    
    elif action == "sub":
        configs = await ConfigService.get_user_configs(user_id=user_id)
        return await callback_query.message.edit_text(
            text=messages.FAQ_SUB,
            reply_markup=keyboards.configs_sub_keyboard(configs=configs)
        )
    

async def process_config_sub_callback(
    callback_query: CallbackQuery,
    callback_data: ConfigSubCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    config_id = callback_data.config_id
    page = callback_data.page

    if action == "page":
        configs = await ConfigService.get_user_configs(user_id=user_id)
        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.configs_sub_keyboard(configs=configs, page=page)
        )
    
    elif action == "config":
        config = await ConfigService.get_config(config_id=config_id)

        config_filename = f"{config.config_name}.ovpn"
        
        date = helpers.form_date(date=config.expiring_at)
        
        return await callback_query.message.edit_text(
            text=messages.CONFIG_FILE.format(
                config_name=config_filename,
                expiring_at=date,
                sub="✅ Активна" if config.is_sub else "❌ Неактивна"
            ),
            reply_markup=keyboards.cancel_sub(config_id=config_id) if config.is_sub else None
        )
    

async def process_config_sub_cancel_callback(
    callback_query: CallbackQuery,
    callback_data: ConfigCancelSubCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    if callback_data.action == "back":
        configs = await ConfigService.get_user_configs(user_id=user_id)
        return await callback_query.message.edit_text(
            text=messages.FAQ_SUB,
            reply_markup=keyboards.configs_sub_keyboard(configs=configs)
        )
    
    return await callback_query.message.edit_text(
        text=messages.CANCEL_SUB,
        reply_markup=keyboards.cancel_sub_confirm(config_id=callback_data.config_id)
    )


async def process_config_sub_cancel_confirm_callback(
    callback_query: CallbackQuery,
    callback_data: ConfigCancelSubConfirmCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    if callback_data.action == "back":
        configs = await ConfigService.get_user_configs(user_id=user_id)
        return await callback_query.message.edit_text(
            text=messages.FAQ_SUB,
            reply_markup=keyboards.configs_sub_keyboard(configs=configs)
        )
    
    config = await ConfigService.get_config(config_id=callback_data.config_id)
    await ConfigService.set_cancel_sub_config(config=config)

    await callback_query.message.delete()
    
    return await callback_query.message.answer(
        text=messages.SUB_CANCELLED.format(config_name=f"{config.config_name}.ovpn")
    )


async def process_theme_callback(
    callback_query: CallbackQuery,
    callback_data: ThemeCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    theme_id = callback_data.theme_id
    page = callback_data.page

    if action == "page":
        themes = await FAQThemeService.get_themes()

        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.themes_keyboard(themes=themes, page=page)
        )
    
    elif action == "theme":
        problems = await FAQProblemService.get_problems_by_theme(theme_id=theme_id)
        return await callback_query.message.edit_text(
            text=messages.FAQ_PROBLEMS,
            reply_markup=keyboards.problems_keyboard(problems=problems, theme_id=theme_id)
        )
    

async def process_problem_callback(
    callback_query: CallbackQuery,
    callback_data: ProblemCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    action = callback_data.action
    problem_id = callback_data.problem_id
    theme_id = callback_data.theme_id
    page = callback_data.page

    if action == "page":
        problems = await FAQProblemService.get_problems_by_theme(theme_id=theme_id)

        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.problems_keyboard(problems=problems, theme_id=theme_id, page=page)
        )
    
    elif action == "problem":
        problem = await FAQProblemService.get_problem(problem_id=problem_id)
        
        return await callback_query.message.edit_text(
            text=messages.FAQ_PROBLEM.format(
                question=problem.question, solution=problem.solution
            ),
            reply_markup=keyboards.problem_keyboard(theme_id=theme_id)
        )
    
    elif action == "back":
        themes = await FAQThemeService.get_themes()

        return await callback_query.message.edit_text(
            text=messages.FAQ_THEMES,
            reply_markup=keyboards.themes_keyboard(themes=themes, page=page)
        )
    

async def process_solution_callback(
    callback_query: CallbackQuery,
    callback_data: SolutionCallback,
    state: FSMContext
):
    user_id = callback_query.from_user.id

    theme_id = callback_data.theme_id

    problems = await FAQProblemService.get_problems_by_theme(theme_id=theme_id)

    return await callback_query.message.edit_text(
        text=messages.FAQ_PROBLEMS,
        reply_markup=keyboards.problems_keyboard(problems=problems, theme_id=theme_id)
    )
    

def register_handlers_faq(dp: Dispatcher):
    dp.message.register(
        process_faq_message, lambda message: message.text == "❓ Помощь 24/7"
    )

    dp.callback_query.register(
        process_faq_callback, FAQCallback.filter()
    )

    dp.callback_query.register(
        process_theme_callback, ThemeCallback.filter()
    )

    dp.callback_query.register(
        process_problem_callback, ProblemCallback.filter()
    )

    dp.callback_query.register(
        process_solution_callback, SolutionCallback.filter()
    )

    dp.callback_query.register(
        process_config_sub_callback, ConfigSubCallback.filter()
    )

    dp.callback_query.register(
        process_config_sub_cancel_callback, ConfigCancelSubCallback.filter()
    )

    dp.callback_query.register(
        process_config_sub_cancel_confirm_callback, ConfigCancelSubConfirmCallback.filter()
    )