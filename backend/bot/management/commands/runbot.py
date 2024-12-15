import asyncio
from bot.main import main
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Запуск Aiogram бота"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting bot..."))
        asyncio.run(main())
        self.stdout.write(self.style.SUCCESS("Bot has been started"))