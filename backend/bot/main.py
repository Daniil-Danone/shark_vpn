import asyncio
from bot.handlers.general import register_handlers_general
from bot.handlers.tariffs import register_handlers_tariffs
from bot.handlers.confident import register_handlers_confident
from bot.handlers.cooperation import register_handlers_cooperation
from bot.handlers.configs import register_handlers_configs
from bot.handlers.referals import register_handlers_referal
from bot.handlers.balance import register_handlers_balance
from bot.handlers.faq import register_handlers_faq

from bot.config import webapp, scheduler
from bot.config.sessions import dispatcher, bot, asyncio_scheduler

from utils.logger import bot_logger


async def main():
    bot_logger.debug("[STARTUP] Register handlers...")

    register_handlers_general(dp=dispatcher)
    register_handlers_tariffs(dp=dispatcher)
    register_handlers_confident(dp=dispatcher)
    register_handlers_cooperation(dp=dispatcher)
    register_handlers_configs(dp=dispatcher)
    register_handlers_referal(dp=dispatcher)
    register_handlers_balance(dp=dispatcher)
    register_handlers_faq(dp=dispatcher)

    bot_logger.debug("[STARTUP] Handlers registered successfully")

    bot_logger.debug("[STARTUP] Starting scheduler...")

    try:
        await asyncio.sleep(1)
        asyncio_scheduler.start()
        await scheduler.setup_scheduler_jobs()
    except Exception as e:
        bot_logger.error(f"[STARTUP] Failed to start scheduler: {e}")
        return
    
    bot_logger.debug("[STARTUP] Scheduler started successfully")
    
    bot_logger.debug("[STARTUP] Starting web application...")

    try:
        await webapp.start_server()
    except Exception as e:
        bot_logger.error(f"[STARTUP] Failed to start web application: {e}")
    
    bot_logger.debug("[STARTUP] Web application started successfully")

    bot_logger.debug("[STARTUP] Starting bot...")
    try:
        await dispatcher.start_polling(bot)
        bot_logger.debug("[STARTUP] Bot started successfully")
    except Exception as e:
        bot_logger.error(f"[STARTUP] Error during polling: {e}")
    finally:
        await bot.session.close()
