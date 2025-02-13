from aiogram import Dispatcher

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

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