import re
import logging
import requests
from datetime import datetime as dt, timezone as tz
from asgiref.sync import async_to_sync
from celery import shared_task

from apps.mailing.services import MailService
from apps.users.service import UserService
from config.environment import BOT_TOKEN


mail_logger = logging.getLogger("[CELERY] ")


@shared_task
def check_uncompleted_mailings():
    uncompleted_mailings = async_to_sync(MailService.get_all_uncompleted)()
    if len(uncompleted_mailings) > 0:
        users = async_to_sync(UserService.get_users)()
        for mail in uncompleted_mailings:
            if mail.scheduled_time > dt.now(tz.utc):
                continue
            for user in users:
                send_mailings.apply_async(
                    args=[user.user_id, mail.content],
                    countdown=5,
                )
            else:
                async_to_sync(MailService.mark_mail_as_completed)(mail.id)


def clean_html(content):
    content = re.sub(r"<p>", "", content)  # Удаляем открывающие теги <p>
    content = re.sub(r"</p>", "\n", content)   # Заменяем </p> на перенос строки
    content = re.sub(r"&nbsp;", "", content)  # Заменяем &nbsp; на перенос строки
    content = re.sub(r"&lt;", "<", content)  # удаляем экранирование тегов, введенных вручную в поле
    content = re.sub(r"&gt;", ">", content)  # удаляем экранирование тегов, введенных вручную в поле
    content = re.sub(r"<br\s*/?>", "\n", content)  # удаляем неподдерживаемый тег <br></br>
    return content


@shared_task
def send_mailings(user_id: int, mail_text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": user_id,
        "text": clean_html(mail_text),
        "parse_mode": "HTML",
    }
    response = requests.post(url, json=data)
    mail_logger.info(
        "[SEND MAIL] To: %s, delivered: %s",
        user_id,
        response.status_code == 200,
    )
    if response.status_code != 200:
        mail_logger.error(
            "[SEND MAIL] Main to: %s was not delivered. Response status: %s, Response body: %s, Mail text: %s",
            user_id,
            response.status_code,
            response.json(),
            clean_html(mail_text),
        )
