from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from apscheduler.schedulers.asyncio import AsyncIOScheduler 

from config.environment import BOT_TOKEN


dispatcher = Dispatcher()

bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

asyncio_scheduler = AsyncIOScheduler()